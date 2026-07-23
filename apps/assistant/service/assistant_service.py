import os
import json
from openai import OpenAI
from apps.products.selectors.product import ProductSelector

client = OpenAI(
    base_url="https://api.gapgpt.app/v1",
    api_key="sk-i47v4afdOiN04pmSoKyLdexpFeLCsmWv3g5CJFlS67bCL54Z"
)

PROMPT_PATH = os.path.join(os.path.dirname(__file__), '../prompts/main_prompt.txt')

with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read()


def handle_search(filters, user_message, previous_messages):
    products = ProductSelector.filter_product(**filters)

    if not products.exists():
        return "متأسفم، هیچ محصولی با این مشخصات پیدا نشد. لطفاً مشخصات دیگری را امتحان کنید."

    product_list = []
    for p in products[:5]:
        product_list.append(f"{p.brand} {p.name}: RAM:{p.ram}GB, GPU:{p.gpu}, Price:{p.price:,} Rial")

    product_text = "\n".join(product_list)

    messages = previous_messages + [
        {"role": "assistant", "content": '{"action": "search"}'},
        {"role": "user", "content": f"Search results:\n{product_text}\n\nIntroduce these products to the customer in Farsi based on their request: {user_message}"}
    ]

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        max_tokens=400,
    )

    return response.choices[0].message.content


def chat(user_message, faqs):
    faq_text = "\n".join([f"Q: {faq.question}\nA: {faq.answer}" for faq in faqs])

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Store Information:\n{faq_text}\n\nCustomer: {user_message}"}
    ]

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
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