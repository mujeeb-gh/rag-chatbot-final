import os
import pandas as pd
from dotenv import load_dotenv
from datasets import load_dataset, Dataset, Features, Sequence, Value
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)
from ragas import evaluate

load_dotenv()

openai_api_key=os.environ['OPENAI_API_KEY']

# rag_bge_large = load_dataset("csv", data_files="app/evaluations/eval_data/rag_bge_large_question_context_answer_csv-min.csv")
# rag_bge_large_finetuned = load_dataset("csv", data_files="app/evaluations/eval_data/rag_bge_large_finetuned_question_context_answer_csv-min.csv")

rag_bge_large = pd.read_csv('app/evaluations/eval_data/rag_bge_large_question_context_answer_csv-min.csv')
rag_bge_large_finetuned = pd.read_csv("app/evaluations/eval_data/rag_bge_large_finetuned_question_context_answer_csv-min.csv")


rag_bge_large.rename(columns={'context': 'contexts'}, inplace=True)
rag_bge_large_finetuned.rename(columns={'context': 'contexts'}, inplace=True)



rag_bge_large = Dataset.from_dict(rag_bge_large)
result_rag_bge_large = evaluate(
    dataset=rag_bge_large,
    metrics=[
        context_precision,
        faithfulness,
        answer_relevancy,
        context_recall,
    ],
)

rag_bge_large_finetuned = Dataset.from_dict(rag_bge_large_finetuned)
result_rag_bge_large_finetuned = evaluate(
    dataset=rag_bge_large_finetuned,
    metrics=[
        context_precision,
        faithfulness,
        answer_relevancy,
        context_recall,
    ],
)

rag_bge_large_df = result_rag_bge_large.to_pandas()
rag_bge_large_finetuned_df = result_rag_bge_large_finetuned.to_pandas()

rag_bge_large_df.to_csv("app/evaluations/eval_data/rag_bge_large_result.csv", index=False)
rag_bge_large_finetuned_df.to_csv("app/evaluations/eval_data/rag_bge_large_finetuned_result.csv", index=False)

