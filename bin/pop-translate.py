#!/usr/bin/env python

import csv

en_po = open('app/translations/en/LC_MESSAGES/messages.po', 'w')
es_po = open('app/translations/es/LC_MESSAGES/messages.po', 'w')

comment = "# DO NOT EDIT - edit translations.csv instead\n\nmsgid \"\"\nmsgstr \"\"\n\n"
en_po.write(comment)
es_po.write(comment)

with open('translations.csv', newline="\n") as csvfile:
  next(csvfile)  # skip headers
  csvreader = csv.reader(csvfile)
  for row in csvreader:
      if len(row) < 5:
        next
      msgid = row[2]
      en_txt = row[4]
      try:
        es_txt = row[5]
      except:
        es_txt = en_txt

      en_po.write("msgid \"%s\"\n" %(msgid))
      es_po.write("msgid \"%s\"\n" %(msgid))
      en_po.write("msgstr \"%s\"\n\n" %(en_txt.encode('unicode_escape').decode('utf-8')))
      es_po.write("msgstr \"%s\"\n\n" %(es_txt.encode('unicode_escape').decode('utf-8')))
