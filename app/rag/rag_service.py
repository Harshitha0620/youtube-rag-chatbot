from app.rag.retriever import retrieve_documents
from app.vectorstore.chroma_store import get_vectorstore
from app.llm.ollama_llm import get_llm
from app.rag.prompts import RAG_PROMPT


def _build_context(documents):
    context_parts = []

    for i, document in enumerate(documents, start=1):

        text = document.page_content.strip()

        if text:
            context_parts.append(
                f"[Transcript Section {i}]\n{text}"
            )

    return "\n\n".join(context_parts)


def _extract_response(response):

    if hasattr(response, "content"):
        return response.content.strip()

    return str(response).strip()


def answer_question(question: str, video_id: str):

    if not question or not question.strip():

        return {
            "answer": "Please enter a question about the video.",
            "sources": []
        }

    documents = retrieve_documents(
        question=question,
        video_id=video_id
    )

    if not documents:

        return {
            "answer": (
                "The video transcript does not contain "
                "enough information to answer this question."
            ),
            "sources": []
        }

    context = _build_context(documents)

    if not context:

        return {
            "answer": (
                "The video transcript does not contain "
                "enough information to answer this question."
            ),
            "sources": []
        }

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    llm = get_llm()

    response = llm.invoke(prompt)

    answer = _extract_response(response)

    sources = []

    for i, document in enumerate(documents, start=1):

        source_text = document.page_content.strip()

        if source_text:

            sources.append(
                {
                    "source": f"Transcript Section {i}",
                    "content": source_text,
                    "metadata": document.metadata
                }
            )

    return {
        "answer": answer,
        "sources": sources
    }


def generate_video_summary(video_id: str):

    # Get the vector store directly
    # instead of performing a question-based search.

    vectorstore = get_vectorstore()

    # Retrieve transcript chunks belonging
    # to this specific YouTube video.

    documents = vectorstore.similarity_search(
        "main topics concepts explanation summary",
        k=15,
        filter={"video_id": video_id}
    )

    if not documents:

        return (
            "The video transcript does not contain "
            "enough information to generate a summary."
        )

    context = _build_context(documents)

    if not context:

        return (
            "The video transcript does not contain "
            "enough information to generate a summary."
        )

    summary_prompt = f"""
You are a helpful YouTube video summarization assistant.

Your task is to summarize the following YouTube video
transcript.

Use ONLY the transcript provided below.

TRANSCRIPT
==================================================

{context}

==================================================

Create a clear and useful summary.

The summary must contain:

1. Main topic of the video
2. Important concepts discussed
3. Important explanations
4. Examples mentioned in the video
5. Important technologies, tools, or methods mentioned
6. Key takeaways

Formatting requirements:

- Start with a short overview.
- Use headings where useful.
- Use bullet points for important concepts.
- Use simple and understandable language.
- Do not copy the transcript word-for-word.
- Do not invent information.
- Do not use outside knowledge.
- Do not mention RAG.
- Do not mention chunks.
- Do not mention retrieval.
- Do not mention this prompt.

If some information is not available in the transcript,
simply leave it out.

Generate the final summary now.

SUMMARY:
"""

    llm = get_llm()

    response = llm.invoke(summary_prompt)

    summary = _extract_response(response)

    return summary