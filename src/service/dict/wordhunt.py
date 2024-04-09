# -*- coding:utf-8 -*-
import os
import re
import requests

from bs4 import Tag

from ..base import *

wordhunt_url_base = u'https://wooordhunt.ru/word/'

@register([u'WordHunt', u'WordHunt'])
class Wordhunt(WebService):

    def __init__(self):
        super().__init__()

    def _get_url(self):
        return wordhunt_url_base 

    def _get_from_api(self):
        data = self.get_response(u'{0}{1}'.format(self._get_url(), self.quote_word))
        soup = parse_html(data)
        result = {
            'meaning': '',
            'example': '',
            'word_form': '',
            'image': '',
        }

        url = f'https://dictionary.skyeng.ru/api/v2/search-word-exact?images=1980x1080&word={self.quote_word}'
        web = requests.get(url)
        if web.status_code == 200:
        	res = web.json()
        array = res["meanings"]
        
        for image in array:
            resolution = list(image["images"].keys())[0]
            print(f'<img src="{image["images"][resolution]["url"]}"/>')
            
        meaning = soup.find('div', class_='t_inline_en')
        result['meaning'] = meaning

        examples = soup.find_all('p', class_='ex_o')
        if examples:
            result['example'] = '<ul>'
            for example in examples[0:3]:
                result['example'] += f'<li>{example.get_text()}</li>'
            result['example'] += '</ul>'

        word_forms = soup.find_all('div', class_='word_form_block')
        if word_forms:
            for form in word_forms:
                result['word_form'] += f'{form.get_text()}'
        return self.cache_this(result)

    @with_styles(need_wrap_css=True, cssfile='_cambridge.css')
    def _css(self, val):
        return val

    @export('MEANING')
    def fld_meaning(self):
        val = self._get_field('meaning')
        if val == None or val == '':
            return ''
        return self._css(val)
    
    @export('EXAMPLE')
    def fld_example(self):
        val = self._get_field('example')
        if val == None or val == '':
            return ''
        return self._css(val)

    @export('WORDFORM')
    def fld_wordform(self):
        val = self._get_field('word_form')
        if val == None or val == '':
            return ''
        return self._css(val)
        
    @export('IMAGE')
    def fld_image(self):
        val = self._get_field('image')
        if val == None or val == '':
            return ''
        return self._css(val)
