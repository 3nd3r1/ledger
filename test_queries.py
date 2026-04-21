from llm_provider import create_llm, invoke_llm
from rag_pipeline import RAGPipeline
from vector_store import VectorStore


TEST_CASES = [
    {
        "question": "Which region has the best sales performance?",
        "truth": "The top sales regions are: 1. West $725,457.82, 2. East $678,781.24, 3. Central $501,239.89",
    },
    {
        "question": "Which product category generates the most revenue?",
        "truth": "Technology generates the most revenue at $836,154.03, followed by Furniture $741,999.80 and Office Supplies $719,047.03",
    },
]


JUDGE_PROMPT = """\
You are evaluating a RAG that answers questions about a sales dataset.

Question: {question}

Truth (computed before): {truth}

RAG Answer: {rag_answer}

Reply with:
SCORE: <integer 1-5>
EXPLANATION: <one sentence>
"""


def judge(question: str, truth: str, rag_answer: str) -> str:
    llm = create_llm()
    prompt = JUDGE_PROMPT.format(
        question=question,
        truth=truth,
        rag_answer=rag_answer,
    )

    return invoke_llm(llm, prompt)


def run_tests():
    store = VectorStore()
    rag = RAGPipeline(store)

    for i, tc in enumerate(TEST_CASES, 1):
        print(f"Test case {i}/{len(TEST_CASES)}")
        print(f"Question: {tc['question']}")
        print(f"Truth: {tc['truth']}")

        rag_answer = rag.query(tc["question"])
        print(f"RAG: {str(rag_answer)}")

        result = judge(
            question=tc["question"], truth=tc["truth"], rag_answer=str(rag_answer)
        )
        print(f"Judge: {result}")
        print()
