from flask import g, current_app
import os
import requests
import json
import newrelic.agent
from formfiller import FormFiller
import base64
from wand.image import Image

class FormFillerService():

  FORMS = {
    '/vr/en': {
      'definitions': 'form-defs/VREN.json',
      'base': 'https://s3.amazonaws.com/ksvotes-v2/FEDVRENNVRIS-v2.png',
    },
    '/vr/es': {
      'definitions': 'form-defs/VRES.json',
      'base': 'https://s3.amazonaws.com/ksvotes-v2/FEDVRENNVRIS_SP-v2.png',
    },
    '/av/ksav1/en': {
      'definitions': 'form-defs/KSAV1.json',
      'base': 'https://s3.amazonaws.com/ksvotes-v2/AV1M.png',
    },
    '/av/ksav2/en': {
      'definitions': 'form-defs/KSAV2.json',
      'base': 'https://s3.amazonaws.com/ksvotes-v2/AV2.png',
    },
    '/av/ksav1/es': {
      'definitions': 'form-defs/AV1M_SP.json',
      'base': 'https://s3.amazonaws.com/ksvotes-v2/AV1M_SP.png',
    },
    '/av/ksav2/es': {
      'definitions': 'form-defs/AV2_SP.json',
      'base': 'https://s3.amazonaws.com/ksvotes-v2/AV2_SP.png',
    },
  }

  DEFINITIONS = {}
  IMAGES = {}

  def __init__(self, payload, form_name):
    self.payload = payload
    self.form_name = form_name
    self.debug = os.getenv('FORM_DEBUG')

    self.__set_filler()

  def __get_or_load_definitions(self):
    if self.form_name not in self.DEFINITIONS or self.debug:
      def_file = os.path.join(current_app.root_path, self.FORMS[self.form_name]['definitions'])
      current_app.logger.info("{} loading {} form defs from {}".format(self.payload['uuid'], self.form_name, def_file))

      with open(def_file) as f:
        self.DEFINITIONS[self.form_name] = json.load(f)

    return self.DEFINITIONS[self.form_name]

  def __get_or_load_image(self):
    if self.form_name not in self.IMAGES or self.debug:
      url = self.FORMS[self.form_name]['base']
      current_app.logger.info("{} loading {} image from {}".format(self.payload['uuid'], self.form_name, url))
      img = requests.get(url)
      self.IMAGES[self.form_name] = { 'bytes': img.content, 'format': img.headers['content-type'] }

    return self.IMAGES[self.form_name]

  def __set_filler(self):
    defs = self.__get_or_load_definitions()
    img = self.__get_or_load_image()
    base_image = Image(blob=img['bytes'], format=img['format'])
    self.filler = FormFiller(payload=self.payload, image=base_image, form=defs, font='Helvetica', font_color='blue')

  def as_image(self):
    return 'data:image/png;base64,' + self.as_base64()

  def as_base64(self):
    return self.filler.as_base64().decode()
