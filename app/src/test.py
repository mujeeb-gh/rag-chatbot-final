# import evaluate
# bleu = evaluate.load("bleu")
# sacrebleu = evaluate.load("sacrebleu")
# rouge = evaluate.load("rouge")
# wer = evaluate.load("wer")
# import json
# from typing import List, Dict
# from nltk.translate.bleu_score import corpus_bleu

# rag_pred = ["To construct a benchmark dataset for early rumor detection (ERD), gather as many early relevant posts as possible from fact-checking websites, focusing on claims. A novel ERD model based on Neural Hawkes Processes can guide a generic rumor detection model to make timely, accurate, and stable predictions by constructing a detection stability distribution over expected future predictions based on prior and current predictions. This allows for an optimal time point to be fixed for detection without delay."]
# llm_pred = ["For constructing a benchmark dataset, consider diversity, representativeness, and time-sensitivity. Incorporate various social media platforms, rumor types, and linguistic styles. A novel model based on Neural Hawkes processes can enhance rumor detection by modeling the temporal dependencies among micro-events, capturing crucial patterns for early rumor detection, and thus improving accuracy and timeliness."]
# refs = [["The optimal approach for constructing a benchmark dataset for early rumor detection is to gather early relevant posts from fact-checking websites to capture the actual early-stage information. Additionally, a novel model based on Neural Hawkes processes, \"HEARD\", can improve the accuracy and timeliness of rumor detection by guiding generic rumor detection models to make timely and stable predictions."]]

# rag_sacrebleu_score = sacrebleu.compute(predictions=rag_pred, references=refs)
# llm_sacrebleu_score = sacrebleu.compute(predictions=llm_pred, references=refs)

# print(f"RAG BLEU: {rag_sacrebleu_score}\nLLM BLEU: {llm_sacrebleu_score}")

from pprint import pprint as print

# rel = [{'doc': 'predictive models especially when formula is an essential '
#          'differentiating part of a task conclusion future work we proposed an '
#          'adaptation of an nlp technique liu et al 2017 from the field of '
#          'machine comprehension to the area of mathematical educational data '
#          'mining we enrich the content representation by parsing mathematical '
#          'formulas into syntax trees and embedding them with neural networks '
#          'our experiments validate the approach using publicly available '
#          'datasets and show that incorporating syntactic information can '
#          'improve performance in predicting the difficulty of an exercise '
#          'these results suggest that the method may be of interest for '
#          'personalised learning solutions we',
#   'metadata': {'title': 'structural information in mathematical formulas for '
#                         'exercise difficulty prediction a comparison of nlp '
#                         'representations',
#                'url': 'https://aclanthology.org/2022.bea-1.14'},
#   'score': 0.2975524663925171},
#  {'doc': 'monitoring validation loss with the patience of 3 epochs results we '
#          'compare data representations to investigate whether adding syntactic '
#          'sequences improves classification performance performance was '
#          'evaluated using 10fold stratified crossvalidation roc auc and is '
#          'shown in table 1 regarding the baselines majority and random '
#          'baselines produce roc auc of 05 on a single run and the best results '
#          'of logistic regression models trained on the length of input '
#          'sequences are 057 for math on descriptions and 066 for deepmind on '
#          'formula respectively regarding other possible neural approaches to '
#          'feature engineering using word2vec algorithm mikolov et al 2013 to '
#          'produce pretrained',
#   'metadata': {'title': 'structural information in mathematical formulas for '
#                         'exercise difficulty prediction a comparison of nlp '
#                         'representations',
#                'url': 'https://aclanthology.org/2022.bea-1.14'},
#   'score': 0.3195769786834717},
#  {'doc': 'using reinforcement learning wang and jin 2019 adversarial learning '
#          'wang et al 2021b wang et al 2020b and also the multimodel structure '
#          'to handle the unknown entities in question answering wang et al 2018 '
#          'wang et al 2020a coreference understanding wang et al 2021a is also '
#          'another research direction in designing questionanswering systems '
#          'conclusion in this paper we introduce a novel mrpqa knowledge based '
#          'question answering system which can leverage information from mrps '
#          'to train our model we use a marginalized probability objective '
#          'function experimental results show that our model achieve strong '
#          'performance on popular kbqa datasets',
#   'metadata': {'title': 'a new concept of knowledge based question answering '
#                         'kbqa system for multihop reasoning',
#                'url': 'https://aclanthology.org/2022.naacl-main.294'},
#   'score': 0.3206987977027893}]

# url = [result['metadata']['url'] for result in rel]

# context = []
# for result in rel:
#   context.append(f'{result["doc"]}=={result["metadata"]["url"]}')
  
# print(context)
  
# from .chroma import search
# q = 'What is Retrieval Augmented Generation'
# results = search("What is Retrieval Augmented Generation", 3)
# if results:
#     for result in results:
#         print(result)
# else:
#     print("No relevant documents found.")

# import os
# from .settings import MODELS_DIR
# from sentence_transformers import SentenceTransformer
# import numpy as np

# model = SentenceTransformer(os.path.join(MODELS_DIR, 'bge-large_finetuned'))
# embeddings: np.ndarray = model.encode(sentences=q, device='cpu', show_progress_bar=True)
# # print(embeddings)

import re

def extract_intent(text):
    """
    Extracts the intent from the given text.
    
    Args:
        text (str): The text to search for an intent.
    
    Returns:
        str: The extracted intent ('open-ended', 'query', 'out of scope') if found, otherwise None.
    """
    # Define the regex pattern to match any of the intents
    pattern = r'\b(open-ended|query|out of scope)\b'
    
    # Search for the pattern in the input text (case insensitive)
    match = re.search(pattern, text, re.IGNORECASE)
    
    # Return the matched intent if found, else None
    if match:
        return match.group(1).lower()
    else:
        return None

# Example usage:
response = "This is an open-ended question, so it should be classified as such."
print(extract_intent(response))  # Output: "open-ended"

response = "Please classify this query as a question."
print(extract_intent(response))  # Output: "query"

response = "I am sorry, but this request is out of scope for me to handle."
print(extract_intent(response))  # Output: "out of scope"

response = "This is a completely unrelated response."
print(extract_intent(response))  # Output: None
