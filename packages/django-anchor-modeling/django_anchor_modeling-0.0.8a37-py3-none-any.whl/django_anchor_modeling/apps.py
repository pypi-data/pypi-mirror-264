from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import class_prepared, post_migrate


def historized_setup(sender, **kwargs):
    if hasattr(sender, "historized_setup"):
        sender.historized_setup()


class DjangoAnchorModelingApp(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_anchor_modeling"

    def ready(self):
        from django_anchor_modeling import signals

        # for knot subclasses
        if getattr(
            settings,
            "DJANGO_ANCHOR_MODELING_AUTO_POPULATE_CHOICES_FOR_KNOT_SUBCLASSES",
            False,
        ):
            post_migrate.connect(signals.populate_choices, sender=self)

        # for automating the static attributes so no more .value
        # see https://chat.openai.com/share/04bc7b85-f358-41eb-bd99-112b997ad764
        from django.apps import apps

        from .models import TransactionBackedAnchorNoBusinessId

        # Adjust the import path as necessary
        from .utils import attach_attribute_descriptors

        # Iterate over all models in all apps
        for model in apps.get_models():
            # Check if the model inherits from TransactionBackedAnchorNoBusinessId
            if issubclass(model, TransactionBackedAnchorNoBusinessId):
                # this makes it such that we no longer need to do anchor.attribute.value
                # just anchor.attribute directly
                attach_attribute_descriptors(model)

    def __init__(self, *args, **kwargs):
        class_prepared.connect(historized_setup)
        super().__init__(*args, **kwargs)
