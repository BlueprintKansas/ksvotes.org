#!/usr/bin/env python

import json

en_po = open('app/translations/en/LC_MESSAGES/messages.po', 'w')
es_po = open('app/translations/es/LC_MESSAGES/messages.po', 'w')

comment = "# DO NOT EDIT - edit translations.json instead\n\nmsgid \"\"\nmsgstr \"\"\n\n"
en_po.write(comment)
es_po.write(comment)

with open('translations.json') as jsonfile:
    translations = json.load(jsonfile)
    for msgid in sorted(translations):
        entry = translations[msgid]
        en_txt = entry['en']
        es_txt = entry['es']
        en_po.write("msgid \"%s\"\n" %(msgid))
        es_po.write("msgid \"%s\"\n" %(msgid))
        en_po.write("msgstr \"%s\"\n\n" %(en_txt.replace("\n", "\\n")))
        es_po.write("msgstr \"%s\"\n\n" %(es_txt.replace("\n", "\\n")))
