"""
COUCHE 3 — Fine-tuning QLoRA (GPU local)
Entraîne Mistral-7B-Instruct sur tes données carbone validées.
À utiliser quand tu as 200+ exemples annotés dans data/finetune_dataset.jsonl
"""

import os
import json
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer
from dotenv import load_dotenv
import torch

load_dotenv()

# ─── Config ──────────────────────────────────────────────────────────────────

BASE_MODEL = os.getenv("BASE_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
OUTPUT_DIR = os.getenv("FINETUNED_MODEL_PATH", "./models/greenia-xai-lora")
DATASET_PATH = "./data/finetune_dataset.jsonl"


def load_dataset_from_jsonl(path: str) -> Dataset:
    """
    Charge le dataset depuis un fichier JSONL.
    Format attendu par ligne :
    {
      "instruction": "Traduis ce JSON en plan narratif...",
      "input": "{...json couche2...}",
      "output": "## 🌱 Synthèse..."
    }
    """
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line.strip()))
    return Dataset.from_list(records)


def format_prompt(example: dict) -> dict:
    """Formate chaque exemple au format Mistral Instruct."""
    prompt = (
        f"<s>[INST] {example['instruction']}\n\n"
        f"Données JSON :\n{example['input']} [/INST] "
        f"{example['output']}</s>"
    )
    return {"text": prompt}


def finetune():
    print(f"🔧 Chargement du modèle de base : {BASE_MODEL}")

    # ── Quantization 4-bit (QLoRA) ────────────────────────────────────────────
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # ── LoRA : on n'entraîne que ~1% des paramètres ───────────────────────────
    lora_config = LoraConfig(
        r=16,                       # Rang matrice LoRA (16 = bon compromis)
        lora_alpha=32,              # Scaling (2x r)
        target_modules=[            # Couches d'attention ciblées (Mistral)
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    # → Affiche ~1% des paramètres entraînables

    # ── Dataset ───────────────────────────────────────────────────────────────
    print(f"📂 Chargement dataset : {DATASET_PATH}")
    raw_dataset = load_dataset_from_jsonl(DATASET_PATH)
    dataset = raw_dataset.map(format_prompt)
    train_val = dataset.train_test_split(test_size=0.1, seed=42)

    print(f"✅ {len(train_val['train'])} exemples d'entraînement")
    print(f"✅ {len(train_val['test'])} exemples de validation")

    # ── Arguments d'entraînement ──────────────────────────────────────────────
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=2,      # Adapter selon ta VRAM
        gradient_accumulation_steps=4,       # Simule batch_size=8
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
        save_strategy="epoch",
        evaluation_strategy="epoch",
        load_best_model_at_end=True,
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        report_to="none",                   # Désactiver wandb si non installé
    )

    # ── Trainer ───────────────────────────────────────────────────────────────
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_val["train"],
        eval_dataset=train_val["test"],
        dataset_text_field="text",
        tokenizer=tokenizer,
        max_seq_length=1024,
        packing=False,
    )

    print("🚀 Lancement du fine-tuning...")
    trainer.train()

    print(f"💾 Sauvegarde du modèle fine-tuné dans : {OUTPUT_DIR}")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("✅ Fine-tuning terminé.")


# ─── Inférence avec le modèle fine-tuné ──────────────────────────────────────

def infer_with_finetuned(json_payload: dict) -> str:
    """
    Utilise le modèle fine-tuné local au lieu de l'API Gemini.
    À utiliser en production hors-cloud.
    """
    from peft import PeftModel

    model_path = os.getenv("FINETUNED_MODEL_PATH", "./models/greenia-xai-lora")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        load_in_4bit=True,
        device_map="auto",
    )
    model = PeftModel.from_pretrained(base_model, model_path)
    model.eval()

    instruction = "Traduis ce JSON d'optimisation carbone en plan d'action narratif structuré en 3 sections."
    prompt = (
        f"<s>[INST] {instruction}\n\n"
        f"Données JSON :\n{json.dumps(json_payload, indent=2, ensure_ascii=False)} [/INST]"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.1,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True).split("[/INST]")[-1].strip()


if __name__ == "__main__":
    finetune()
