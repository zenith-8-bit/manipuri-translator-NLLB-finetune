import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments

# 1. Load the CSV file
file_path = "manipuri_english.csv"  # Replace with your file path
data = pd.read_csv(file_path, names=["manipuri", "english"])

# 2. Create a Hugging Face Dataset
dataset = Dataset.from_pandas(data)

# 3. Preprocess the Data
model_name = "facebook/nllb-200-distilled-600M"  # Pretrained NLLB model
tokenizer = AutoTokenizer.from_pretrained(model_name)

def preprocess_function(examples):
    inputs = examples["manipuri"]
    targets = examples["english"]
    model_inputs = tokenizer(inputs, text_target=targets, max_length=128, truncation=True)
    return model_inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# 4. Load the Pretrained Model
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# 5. Define Training Arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./results",          # Output directory
    evaluation_strategy="epoch",    # Evaluate every epoch
    learning_rate=2e-5,             # Learning rate
    per_device_train_batch_size=16, # Batch size
    per_device_eval_batch_size=16,
    weight_decay=0.01,              # Weight decay
    save_total_limit=3,             # Limit for saved checkpoints
    num_train_epochs=3,             # Number of epochs
    predict_with_generate=True,     # For translation task
    logging_dir='./logs',           # Logging directory
    logging_steps=10,
)

# 6. Initialize Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
)

# 7. Train the Model
trainer.train()

# 8. Save the Fine-tuned Model
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")