#tests effecienccy of the model
import pandas as pd
from datasets import load_metric
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import matplotlib.pyplot as plt

# Load test dataset
test_file_path = "testmedaddy.csv"  # Path to your test CSV file
test_data = pd.read_csv(test_file_path, names=["manipuri", "english"])

# Load the fine-tuned model and tokenizer
model_path = "./fine_tuned_model"  # Path to the fine-tuned model
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Initialize metrics
bleu_metric = load_metric("sacrebleu")
accuracy_metric = {"correct": 0, "total": 0}

# Prepare lists to store results for plotting
sentence_indices = []
accuracies = []

# Function to calculate accuracy
def calculate_accuracy(predictions, references):
    correct = sum([1 for pred, ref in zip(predictions, references) if pred.strip() == ref.strip()])
    total = len(references)
    return correct, total

# Evaluate the model
print("Evaluating the model...")
predictions = []
references = []

for index, row in test_data.iterrows():
    manipuri_text = row["manipuri"]
    reference_translation = row["english"]

    # Tokenize and generate translation
    inputs = tokenizer(manipuri_text, return_tensors="pt", max_length=128, truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=128, num_beams=4)
    predicted_translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Store predictions and references for evaluation
    predictions.append(predicted_translation)
    references.append(reference_translation)

    # Update accuracy metrics
    correct, total = calculate_accuracy([predicted_translation], [reference_translation])
    accuracy_metric["correct"] += correct
    accuracy_metric["total"] += total

    # Store accuracy for plotting
    sentence_indices.append(index)
    accuracies.append(accuracy_metric["correct"] / accuracy_metric["total"])

    print(f"Processed sentence {index + 1}/{len(test_data)}")

# Calculate BLEU score
bleu_score = bleu_metric.compute(predictions=predictions, references=[[ref] for ref in references])

# Calculate overall accuracy
overall_accuracy = accuracy_metric["correct"] / accuracy_metric["total"]

# Print results
print(f"BLEU Score: {bleu_score['score']:.2f}")
print(f"Overall Accuracy: {overall_accuracy:.2f}")

# Plot accuracy over test data
plt.figure(figsize=(10, 6))
plt.plot(sentence_indices, accuracies, label="Accuracy", color="blue")
plt.xlabel("Sentence Index")
plt.ylabel("Accuracy")
plt.title("Model Performance on Test Data")
plt.legend()
plt.grid()
plt.savefig("model_performance.png")
plt.show()