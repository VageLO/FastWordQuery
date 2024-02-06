# -*- coding:utf-8 -*-
import os
import re

from bs4 import Tag

from ..base import *

wordhunt_url_base = u'https://wooordhunt.ru/word/'


class Wordhunt(WebService):

    def __init__(self):
        super().__init__()

    def _get_url(self):
        return wordhunt_url_base 

    def _get_from_api(self):
        data = self.get_response(u'{0}{1}'.format(self._get_url(), self.quote_word))
        soup = parse_html(data)
        result = {
            'example': '',
            'word_form': '',
        }
       
        element = soup.find('div', class_='')
        if element:

            elements = element.find_all('div', class_='entry-body__el')
            header_found = False
            for element in elements:
                    senses = element.find_all('div', class_='pos-body')

                    span_posgram = element.find('div', class_='posgram')
                    pos_gram = (span_posgram.get_text() if span_posgram else '')

        return self.cache_this(result)

    @with_styles(need_wrap_css=True, cssfile='_cambridge.css')
    def _css(self, val):
        return val

    @export('EXAMPLE')
    def fld_example(self):
        return self._fld_img('image')

    @export('WORDFORM')
    def fld_wordform(self):
        val = self._get_field('word_form')
        if val == None or val == '':
            return ''
        return self._css(val)
