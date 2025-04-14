from transformers import pipeline

qa_pipeline = pipeline("question-answering")

def answer_question(context, question, context_type="General Users"):
    prompt_context = f"You are answering on behalf of a {context_type}. Use appropriate tone and detail.\n\nTranscript:\n{context}"
    result = qa_pipeline(question=question, context=prompt_context)
    return result['answer']
