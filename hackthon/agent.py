import asyncio
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from hindsight_client_api.exceptions import NotFoundException
from groq import Groq

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BANK_ID = "devops-incidents-bank"
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

def process_incident(user_query: str):
    return asyncio.run(_process_incident(user_query))


async def _process_incident(user_query: str):
    hindsight = Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=os.getenv("HINDSIGHT_API_KEY")
    )
    try:
        try:
            recall_results = await hindsight.arecall(bank_id=BANK_ID, query=user_query)
        except NotFoundException:
            await hindsight.acreate_bank(BANK_ID)
            recall_results = await hindsight.arecall(bank_id=BANK_ID, query=user_query)

        recalled_memories = [item.text for item in getattr(recall_results, 'results', [])]
        memory_context = "\n".join(recalled_memories) if recalled_memories else "No prior history found."

        system_prompt = f"""You are an Incident Response & Site Reliability Engineering (SRE) AI Agent.

        === RECALLED HINDSIGHT MEMORIES ===
        {memory_context}
        ===================================

        Instructions:
        - If recalled memories match the issue, give a concise, step-by-step fix based on past resolutions.
        - If no relevant memory exists, provide a standard troubleshooting guide.
        """

        chat_completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )

        response_text = chat_completion.choices[0].message.content

        await hindsight.aretain(
            bank_id=BANK_ID,
            content=f"User Query: {user_query}\nAgent Fix Suggested: {response_text}"
        )

        return response_text, memory_context
    finally:
        await hindsight.aclose()