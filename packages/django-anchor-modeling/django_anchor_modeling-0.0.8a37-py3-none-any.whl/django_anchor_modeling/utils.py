from django_anchor_modeling import constants
from django_anchor_modeling.exceptions import SentinelUserDoesNotExist


def get_knot_choice_value(instance: object):
    """
    Given any instance of a model, return the knot choice value
    format is

    APP__CLASS
    """
    app_label = instance._meta.app_label
    class_name = instance.__class__.__name__

    return f"{app_label}__{class_name}"


# utils.py or a similar module
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

SENTINEL_NULL_USER_ID = getattr(
    settings, "SENTINEL_NULL_USER_ID", constants.SENTINEL_NULL_USER_ID
)


def get_sentinel_user():
    sentinel_user, _ = User.objects.get_or_create(pk=SENTINEL_NULL_USER_ID)
    return sentinel_user


def get_sentinel_user_id():
    if User.objects.filter(pk=SENTINEL_NULL_USER_ID).exists():
        return SENTINEL_NULL_USER_ID
    else:
        raise SentinelUserDoesNotExist()


class AttributeValueDescriptor:
    def __init__(self, related_name):
        self.related_name = related_name

    def __get__(self, instance, owner):
        if instance is None:
            # Access through the class, not an instance
            return self
        try:
            # Dynamically get the related model and return its value
            related_object = getattr(instance, self.related_name)
            return related_object.value
        except AttributeError:
            # Handle the case where the relation does not exist
            return None


def attach_attribute_descriptors(anchor_class):
    for field in anchor_class._meta.get_fields():
        if hasattr(field, "is_attribute") and field.is_attribute:
            # Assuming your related_name pattern here, adjust as needed
            descriptor = AttributeValueDescriptor(field.name)
            setattr(anchor_class, field.name, descriptor)
