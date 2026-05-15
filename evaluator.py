import os
from dotenv import load_dotenv
from deepeval.metrics import HallucinationMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval import evaluate

load_dotenv()

hallucination_metric = HallucinationMetric(threshold=0.5)
relevancy_metric = AnswerRelevancyMetric(threshold=0.7)

test_cases = [
    LLMTestCase(
        input="What is the difference between RAG and Fine-tuning?",
        actual_output="RAG retrieves live data from a database, while fine-tuning updates the internal weights of the model.",
        # CHANGE THIS LINE: from retrieval_context to context
        context=["RAG stands for Retrieval-Augmented Generation...", "Fine-tuning is the process of training a model further..."],
        expected_output="RAG uses external data at inference time; fine-tuning modifies the model's parameters."
    )
]

if __name__ == "__main__":
    evaluate(test_cases, [hallucination_metric, relevancy_metric])