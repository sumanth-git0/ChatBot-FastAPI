from sqlalchemy.orm import Session
from sqlalchemy import text
from app.utils.embeddings import embeddings

def retrieve_context_from_db(
    db: Session,
    user_id: str,
    question: str,
    k: int = 5
) -> str:
    query_embedding = embeddings.embed_query(question)

    sql = text("""
        SELECT content
        FROM chunks
        WHERE user_id = :user_id
        ORDER BY embedding <=> CAST(:query_embedding AS vector)
        LIMIT :k
    """)


    rows = db.execute(
        sql,
        {
            "user_id": user_id,
            "query_embedding": query_embedding,
            "k": k
        }
    ).fetchall()

    return "\n\n".join(row[0] for row in rows)
