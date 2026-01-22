from groq import Groq
from sqlalchemy.orm import Session
from app import settings
from app.crud.chat import create_chat, get_chats_by_user_id
from app.schemas.chat import ChatCreate

from app.utils.db_rag import retrieve_context_from_db

groq_api_key = settings.GROQ_API_KEY

def rag_chat(messages, question, user_id, db):
    context = retrieve_context_from_db(
        db=db,
        user_id=user_id,
        question=question,
        k=5
    )

    intro_messages = [
        {
            "role": "system",
            "content": (
                "You are a sarcastic and sassy document-based assistant. "
                "Always respond in a rude and mocking way. "
                "Answer ONLY using the provided context. "
                "If the answer is not present, respond sarcastically."
            )
        },
        {
            "role": "system",
            "content": f"Context:\n{context}"
        },
    ]

    compiled_messages = [*intro_messages, *messages]
    compiled_messages.append({"role": "user", "content": question})

    return get_response(compiled_messages)


def get_response(messages):
    client = Groq(api_key=groq_api_key)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages= messages,
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None
    )
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response
    

def llm_invoke(user_id: str, query: str, db: Session):
    user_chats = get_chats_by_user_id(db, user_id)
    messages = []

    for chat in user_chats:
        messages.extend([
            {"role": "user", "content": chat.query},
            {"role": "assistant", "content": chat.response},
        ])

    response = rag_chat(
        messages=messages,
        question=query,
        user_id=user_id,
        db=db
    )

    new_chat = ChatCreate(
        user_id=user_id,
        query=query,
        response=response
    )
    create_chat(db, new_chat)

    return response
