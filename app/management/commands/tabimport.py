from django.core.management.base import BaseCommand
from app.models import Word, Language, Definition
import pandas as pd
import re

# Read the .tab file into a DataFrame

class Command(BaseCommand):
    help = 'Import tab file'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        filepath = str(options['filepath'])

        df = pd.read_csv(filepath, delimiter='\t')

        definitions = []
        words = []
        batchsize = 10000

        lang = "pl"
        pl, created = Language.objects.get_or_create(
            name="Polish", abb=lang
        )

        currRootForm = ""
        currRootObject = None
        rootExists = False
        heldRows = []

        for row in df.itertuples():
            form = row.form
            lemma = row.lemma
            lemma = lemma.split(':')[0]

            if lemma != currRootForm:
                if rootExists:
                    for heldrow in heldRows:
                        w = Word(word_text=heldrow.form, lang=pl, tag=heldrow.tag,
                                wtype=heldrow.desc, abb=heldrow.abb, 
                                root=currRootObject)
                        words.append(w)
                    heldRows = []
                    currRootForm = lemma
                    rootExists = False
                    if len(words) > batchsize:
                        Word.objects.bulk_create(words)
                        words = []
                else:
                    heldRows = []
                    currRootForm = lemma
                    rootExists = False

            # root
            if form == lemma:
                # 2nd "root"
                if rootExists:
                    w = Word(word_text=form, lang=pl, tag=row.tag,
                             wtype=row.desc, abb=row.abb, 
                             root=currRootObject)
                    words.append(w)
                # 1st root
                else:
                    currRootObject = Word(word_text=form, lang=pl, tag=row.tag,
                                        wtype=row.desc, abb=row.abb, root=None)
                    currRootObject.save()
                    definitions.append(Definition(word=currRootObject, user=None))
                rootExists = True
            else:
                heldRows.append(row)
        if words:
            Word.objects.bulk_create(words)
        Definition.objects.bulk_create(definitions)

# python manage.py tabimport "data/sgjp-20240929.tab"