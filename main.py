import os
import json
from deep_translator import DeepL
with open('en_US.json') as json_file:
    data = json.load(json_file)
    line = 1
    keys = len(data.keys())
    for field in data.keys():
        data[field] = DeepL(api_key=os.environ.get('DEEPL_API_KEY'), source='en', target='ro').translate(data[field])
        print(f'Translating line {line} of {keys}')
        line += 1
    print('Translation finished!')
with open('ro.json', 'w') as fp:
    json.dump(data, fp, indent=4)