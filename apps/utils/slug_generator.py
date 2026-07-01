from django.utils.text import slugify
import uuid


def generate_unique_slug(instance, name_field='name', slug_field='slug'):
    """
    Generate a unique slug for any model.
    If slug exists, appends a short UUID.
    """
    slug = slugify(getattr(instance, name_field), allow_unicode=True)
    model_class = instance.__class__
    
    queryset = model_class.objects.filter(**{slug_field: slug})
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    
    if queryset.exists():
        slug = f"{slug}-{uuid.uuid4().hex[:6]}"
    
    return slug