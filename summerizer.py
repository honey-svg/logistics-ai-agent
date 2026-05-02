from app.llm.client import generate_response

def summarize(history):
    text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

    messages = [
        {
            "role": "system",
            "content": "Summarize user details and intent in 1-2 lines."
        },
        {
            "role": "user",
            "content": text
        }
    ]

    return generate_response(messages)
