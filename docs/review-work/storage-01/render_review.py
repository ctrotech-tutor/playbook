"""Generate a readable review manuscript from the sole authored contract source."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
data=json.loads((P/'contract-source.json').read_text());u=data['units'][0]
parts=['# '+u['title'],'**Unreleased technical-review manuscript. Not added to production coverage counts or independently approved.**','Reviewed: '+u['review_date']+'. '+u['review_method']+'.',u['introduction'],'## Objectives']
parts += ['- '+x for x in u['objectives']]
parts += ['## Prerequisites']+['- '+x for x in u['prerequisites']]+['## Terms']+['- **'+k+':** '+v for k,v in u['terms'].items()]
for section in u['shared_sections']:
 parts+=['## '+section['title'],section['text'],'Sources: '+', '.join('<'+x+'>' for x in section['sources'])]
for m in u['members']:
 parts+=['## '+m['name'],'`'+m['signature']+'`',m['meaning'],'### Inputs and conversions',m['inputs_and_conversions'],'### Return value and defaults',m['returns_and_defaults'],'### Algorithm and branches']
 parts += [f'{i}. '+x for i,x in enumerate(m['algorithm'],1)]
 parts+=['### Errors and restrictions',m['errors_and_restrictions'],'### Effects and ordering',m['effects_and_ordering'],'```javascript\n'+m['code']+'\n```',m['explanation'],'Sources: '+', '.join('<'+x+'>' for x in dict.fromkeys(m['sources']))]
parts+=['## Exercise',u['exercise']['question'],'### Explained answer',u['exercise']['answer'],'```html\n'+u['exercise']['html']+'\n```','```javascript\n'+u['exercise']['code']+'\n```','```javascript\n'+u['exercise']['usage_code']+'\n```',u['exercise']['implementation_notes'],'## Compatibility and continuing assessment',u['compatibility'],'## Still open']+['- '+x for x in u['still_open']]
text='\n\n'.join(parts)+'\n';assert '\u2014' not in text;(P/'storage-behavior-review.md').write_text(text)
print('Generated review manuscript:',len(text.split()),'words')
