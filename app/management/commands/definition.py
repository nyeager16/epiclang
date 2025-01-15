from django.core.management.base import BaseCommand
from app.models import Word, Definition

class Command(BaseCommand):
    help = 'Add Definitions to Table'

    def handle(self, *args, **options):
        batchsize = 10000
        definitions = []
        for word in Word.objects.all():
            definition = Definition(user=None, word=word, definition_text="")
            definitions.append(definition)
            if len(definitions) > batchsize:
                Definition.objects.bulk_create(definitions)
                definitions = []
        if definitions:
            Definition.objects.bulk_create(definitions)

# python manage.py definition