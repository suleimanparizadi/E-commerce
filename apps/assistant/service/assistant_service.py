import os
import json
from openai import OpenAI
from apps.products.selectors.product import ProductSelector
from apps.products.api.serializer.product_serializer import ProductListSerializer



client = OpenAI(
    base_url="https://api.gapgpt.app/v1",
    api_key=os.getenv('GAPGPT_API_TOKEN')
)

PROMPT_PATH = os.path.join(os.path.dirname(__file__), '../prompts/main_prompt.txt')

with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read()



    
def handle_search(filters, user_message, previous_messages):
    products = ProductSelector.filter_product(**filters)

    if not products.exists():
        return {"message": "متأسفم، هیچ محصولی با این مشخصات پیدا نشد.", "products": []}

    serializer = ProductListSerializer(products[:5], many=True)

    product_text = json.dumps(serializer.data, ensure_ascii=False)

    messages = previous_messages + [
        {"role": "assistant", "content": '{"action": "search"}'},
        {"role": "user", "content": f"Search results (JSON):\n{product_text}\n\nIntroduce these products to the customer in Farsi based on their request: {user_message}"}
    ]

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        max_tokens=400,
    )

    return {
        "message": response.choices[0].message.content,
        "products": serializer.data,
    }


def chat(user_message, faqs):
    faq_text = "\n".join([f"Q: {faq.question}\nA: {faq.answer}" for faq in faqs])

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Store Information:\n{faq_text}\n\nCustomer: {user_message}"}
    ]

    response = client.chat.completions.create(
        model="qwen3-235b-a22b-instruct-2507",
        messages=messages,
        max_tokens=300,
    )

    ai_response = response.choices[0].message.content

    try:
        parsed = json.loads(ai_response)
        if parsed.get("action") == "search":
            return handle_search(parsed['filters'], user_message, messages)
    except (json.JSONDecodeError, KeyError):
        pass

    return ai_response




