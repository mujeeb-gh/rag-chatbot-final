import pandas as pd
import json

# Load the JSON data from the file
with open("app/evaluations/eval_data/question_answer_pairs-min.json", "r") as f:
    prev_data = json.load(f)

# # Create a list of dictionaries to store the data for the pandas DataFrame
# data_list = []
# for item in data:
#     data_list.append({"question": item["question"], "context": item["context"], "answer": item["answer"]})

# # Create a pandas DataFrame from the list of dictionaries
# df = pd.DataFrame(data_list)

# # Save the DataFrame to a CSV file
# df.to_csv("app/evaluations/eval_data/question_context_answer_csv-min.csv", index=False)  # Replace "paraphrase_data.csv" with your desired filename

# print("Data successfully converted to CSV!")

# Assuming you have the previous JSON data loaded (from previous execution or separate file)
# as a list of dictionaries called `previous_data`

# Load the new JSON data from the file
with open("app/evaluations/eval_data/rag_bge_large_response_qa.json", "r") as f:
    new_data = json.load(f)

# Combine the context from previous data with the new questions and answers
combined_data = []
for item in new_data:
    # Assuming "context" is always present in previous_data for each question
    context = [data["context"] for data in prev_data if data["question"] == item["question"]]
    ground_truth = [data["answer"] for data in prev_data if data["question"] == item["question"]]
    # If context is not always present, handle the missing context case here
    if context:
        item["context"] = context[0]  # Use the first available context (modify if needed)
        item["ground_truth"] = ground_truth[0]  # Use the first available context (modify if needed)
    combined_data.append({"question": item["question"], "context": [item["context"]], "answer": item["answer"], "ground_truth": item["ground_truth"]})

# Create a pandas DataFrame from the combined data
df = pd.DataFrame(combined_data)

# Save the DataFrame to a CSV file
df.to_csv("app/evaluations/eval_data/rag_bge_large_finetuned_question_context_answer_csv-min.csv", index=False)  # Replace "combined_data.csv" with your desired filename



print("Data successfully converted to CSV!")
