import requests
import json 
from bs4 import BeautifulSoup

def example_list(soup, div_info, span_info):
    try:
        dataset = soup.find('div', div_info)
        examples = dataset.find_all('span', span_info)
    except AttributeError:
        return None

    if len(examples) <= 0:
        return None

    li = '' 
    for example in examples:
        child_elements = [str(child) for child in example.children]
        text = ''.join(child_elements)
        li += f'<li>{text.strip()}</li>'

    return f'<ul>{li}</ul>'

def definition(soup, tab):
    try:
        data_tab = soup.find('div', tab)
        div = data_tab.find('div', { 'class': 'def ddef_d db' })
    except AttributeError:
        return None

    child_elements = [str(child) for child in div.children]
    definition = ''.join(child_elements)

    return definition

def main(word):
    word = word.lower().replace(' ', '%20')
    url = f'https://dictionary.cambridge.org/dictionary/english/{word}'
        
    headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    } 

    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    examples = example_list(soup, {'id': 'dataset-example'}, {'class': 'deg'})
    meaning = definition(soup,  {'data-tab': 'ds-cacd'})

    if examples is None:
        examples = example_list(soup, {'class': 'pr dictionary'}, {'class': 'eg deg'})

    if meaning is None:
        meaning = definition(soup, {'class': 'pr dictionary'})

    results = {
        'meaning': meaning,
        'examples': examples,
    }
    
    return results

if __name__ == "__main__":
    words = ['jog', 'evocation', 'evocative', 'evoked set', 'evocative of something', 'evoke', 'stamp', 'relive', 'remind', 'resonant', 'commit', 'annal', 'hooky']

    file = open('log.log', 'w')

    for word in words:
        res = main(word)
        file.write(str(json.dumps(res, indent=4)))
