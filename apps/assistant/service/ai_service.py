from huggingface_hub import InferenceClient
import os

PROMPT_PATH = os.path.join(os.path.dirname(__file__), '../prompts/faq_system.txt')
client = InferenceClient(token=os.getenv('HF_API_TOKEN'))

with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read()


def build_prompt(question, faqs):
    faq_text = "\n".join([f"سوال: {faq.question}\nجواب: {faq.answer}" for faq in faqs])
    return f"{SYSTEM_PROMPT}\n\nاطلاعات فروشگاه:\n{faq_text}\n\nسوال مشتری: {question}\nپاسخ:"



def ask_ai(question, faqs):
    prompt = build_prompt(question, faqs)
    response = client.text_generation(
        prompt,
        model="Qwen/Qwen2.5-7B-Instruct",
        max_new_tokens=300,
    )

    return response
