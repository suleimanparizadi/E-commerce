from apps.assistant.models.faq import FAQ

class AssistantSelector:

    def get_active_faqs():

        return FAQ.objects.filter(is_active=True)