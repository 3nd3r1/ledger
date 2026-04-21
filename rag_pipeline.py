from langchain_core.prompts import PromptTemplate

from llm_provider import create_llm, invoke_llm
from vector_store import VectorStore


SYSTEM_PROMPT = """You are a data analyst assistant.
You answer questions about the Superstore dataset.
Use only the provided context to answer.
If the context doesn't contain enough information, say that there is not enough information.
Always cite specific data."""

RAG_TEMPLATE = PromptTemplate.from_template(
    SYSTEM_PROMPT + "\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer based on the context above:"
)


class RAGPipeline:
    def __init__(
        self,
        vector_store: VectorStore,
        top_k: int = 10,
    ):
        self._store = vector_store
        self._top_k = top_k

        self._llm = create_llm()

    def retrieve(self, query: str) -> list[dict]:
        return self._store.search(query, n_results=self._top_k)

    def query(self, question: str) -> str:
        docs = self.retrieve(question)
        if not docs:
            return "No relevant documents found."

        context = "\n\n".join(f"{doc['text']}" for doc in docs)
        prompt = RAG_TEMPLATE.format(context=context, question=question)
        return invoke_llm(self._llm, prompt)
