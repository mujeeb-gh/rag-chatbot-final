# BLEU
import json
from typing import List, Dict


import evaluate
from evaluate import load
exact_match_metric = load("exact_match")
bleu = evaluate.load("bleu")
rouge = evaluate.load('rouge')
bertscore = load("bertscore")



def compute_bleu_score(predictions_file: str, references_file: str) -> float:
    """
    Compute BLEU score between predicted answers and reference answers.
    
    Args:
    - predictions_file (str): Path to the JSON file containing predicted answers.
    - references_file (str): Path to the JSON file containing reference answers.
    
    Returns:
    - float: BLEU score.
    """
    # Load predictions and references from JSON files
    with open(predictions_file, 'r') as f_pred, open(references_file, 'r') as f_ref:
        predictions_data = json.load(f_pred)
        references_data = json.load(f_ref)
    
    # Extract answers from JSON data
    predictions = [entry['answer'] for entry in predictions_data]
    references = [[entry['answer']] for entry in references_data]
    
    # Compute BLEU score
    bleu_score = bleu.compute(predictions=predictions, references=references)
    
    return bleu_score
  
  
def compute_rouge(predictions_file: str, references_file: str) -> float:
        # Load predictions and references from JSON files
    with open(predictions_file, 'r') as f_pred, open(references_file, 'r') as f_ref:
        predictions_data = json.load(f_pred)
        references_data = json.load(f_ref)
    
    # Extract answers from JSON data
    predictions = [entry['answer'] for entry in predictions_data]
    references = [entry['answer'] for entry in references_data]
    
    # Compute BLEU score
    rouge_score = rouge.compute(predictions=predictions, references=references)
    
    return rouge_score
  
def compute_bertscore(predictions_file: str, references_file: str) -> float:
        # Load predictions and references from JSON files
    with open(predictions_file, 'r') as f_pred, open(references_file, 'r') as f_ref:
        predictions_data = json.load(f_pred)
        references_data = json.load(f_ref)
    
    # Extract answers from JSON data
    predictions = [entry['answer'] for entry in predictions_data]
    references = [entry['answer'] for entry in references_data]
    
    # Compute BLEU score
    bertscore_score = bertscore.compute(predictions=predictions, references=references, lang="en")
    
    return bertscore_score
  
  

# Example usage
llm_predictions_file = 'app/evaluations/eval_data/llm_response_qa-min.json'
rag_predictions_file = 'app/evaluations/eval_data/rag_response_qa-min.json'

references_file = 'app/evaluations/eval_data/question_answer_pairs-min.json'


llm_bleu_score = compute_bleu_score(llm_predictions_file, references_file)
rag_bleu_score = compute_bleu_score(rag_predictions_file, references_file)

print(f"LLM BLEU score: {llm_bleu_score['bleu']}")
print(f"RAG BLEU score: {rag_bleu_score['bleu']}\n")

llm_rouge_score = compute_rouge(llm_predictions_file, references_file)
rag_rouge_score = compute_rouge(rag_predictions_file, references_file)

print(f"LLM ROUGE score: {llm_rouge_score}")
print(f"RAG ROUGE score: {rag_rouge_score}\n")

llm_bertscore_score = compute_rouge(llm_predictions_file, references_file)
rag_bertscore_score = compute_rouge(rag_predictions_file, references_file)

print(f"LLM BERTSCORE score: {llm_bertscore_score}")
print(f"RAG BERTSCORE score: {rag_bertscore_score}\n")