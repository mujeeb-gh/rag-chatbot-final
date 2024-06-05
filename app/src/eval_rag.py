# import sys
# sys.path.append('app/src')

from astra import astra_rag_eval
from llm import groq_chat, CHAT_MODEL
from chroma import search_eval
from typing import Any


LLM_ANSWER_GEN_TEMPLATE = """\
Generate one brief and informative answer to the following question: {question}. \
  The answer should be concise, relevant, and not exceed 60 words in length.
"""

import json

import json
from tqdm import tqdm
import time

def generate_responses_llm(questions_file: str, output_file: str, model: CHAT_MODEL="mixtral-8x7b-32768", batch_size: int = 30, delay_between_batches: int = 10):
    """
    Generate responses using the LLM for each question in the input file and save them to the output file.
    """
    responses = []  # Dictionary to store question-response pairs
    
    with open(questions_file, 'r') as f_questions:
        data = json.load(f_questions)
        questions = data["question"]
        num_questions = len(questions)
        
        for i in tqdm(range(0, num_questions, batch_size), desc="Generating responses", total=num_questions // batch_size):
            batch_questions = questions[i:i+batch_size]
            for question in batch_questions:
                # Generate response using LLM
                answer = groq_chat(
                    message=question,
                    preamble=LLM_ANSWER_GEN_TEMPLATE,  # Use a short prompt template
                    model=model,
                ).choices[0].message.content
                responses.append({"question": question, "answer": answer})  # Store question-response pair in dictionary
            
            # Introduce delay between batches
            time.sleep(delay_between_batches)
    
    # Save responses to JSON file
    with open(output_file, 'w') as f_output:
        json.dump(responses, f_output, indent=4)


import json
from typing import Any
from tqdm import tqdm
import time

def generate_responses_rag(questions_file: str, output_file: str, model: CHAT_MODEL="mixtral-8x7b-32768", batch_size: int = 30, delay_between_batches: int = 10):
    """
    Generate responses using the LLM for each question in the input file and save them to the output file.
    """
    responses = []  # List to store question-response pairs
    
    with open(questions_file, 'r') as f_questions:
        data = json.load(f_questions)
        num_questions = len(data)
        
        for i in tqdm(range(0, num_questions, batch_size), desc="Generating responses", total=num_questions // batch_size):
            batch_data = data[i:i+batch_size]
            for idx, item in enumerate(batch_data):
                question = item["question"]
                print(question)
                context = search_eval(query=question, k=3, model_name_or_path="models/bge-large_finetuned")
                
                # Generate response using LLM
                if not context:
                    answer = "I'm sorry, I don't have any information on that. Feel free to ask me anything else."
                else:
                    answer = astra_rag_eval(
                        prompt=question,
                        context=[result["doc"] for result in context]
                    )
                
                responses.append({"question": question, "answer": answer})  # Store question-response pair in list
                print(f"{i+idx+1} questions answered")
            
            # Introduce delay between batches
            time.sleep(delay_between_batches)
    
    # Save responses to JSON file
    with open(output_file, 'w') as f_output:
        json.dump(responses, f_output, indent=4)

      
generate_responses_rag(questions_file='app/evaluations/eval_data/question_answer_pairs-min.json', output_file='app/evaluations/eval_data/rag_bge_large_finetuned_response_qa.json')
