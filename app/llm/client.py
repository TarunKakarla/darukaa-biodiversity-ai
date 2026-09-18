import json
import os

from openai import OpenAI
from app.llm.prompt import build_prompt


def call_llm(
    metrics,
    chains,
    retrieved,
    user_question=None,
    requested_intervention=None,
):
    client = OpenAI(
        base_url=os.getenv(
            "LLM_BASE_URL",
            "http://localhost:8080/v1"
        ),
        api_key=os.getenv(
            "LLM_API_KEY",
            "lm-studio"
        )
    )

    model = os.getenv(
        "LLM_MODEL",
        "local-model"
    )

    prompt = build_prompt(
        metrics,
        chains,
        retrieved,
        user_question=user_question,
        requested_intervention=requested_intervention,
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ],
        temperature=0.1,
        response_format={
            "type": "json_object"
        },
    )

    content = response.choices[0].message.content

    print("\n========== LLM RESPONSE ==========")
    print(content)
    print("==================================\n")

    if not content:
        raise RuntimeError("LLM returned an empty response.")

    content = content.strip()

    # Remove Markdown JSON fences if the model adds them
    if content.startswith("```json"):
        content = content[len("```json"):].strip()

    if content.startswith("```"):
        content = content[len("```"):].strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError as exc:
        print("\n========== CLEANED RESPONSE ==========")
        print(content)
        print("=======================================\n")

        raise RuntimeError(
            "LLM returned invalid JSON after cleaning the response."
        ) from exc