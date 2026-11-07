#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
ap=argparse.ArgumentParser(description='Korjaa yhden albumin tiedot albums.json-tiedostossa.')
ap.add_argument('patch'); ap.add_argument('--data',default='albums.json'); a=ap.parse_args()
dp=Path(a.data); data=json.loads(dp.read_text(encoding='utf-8')); patch=json.loads(Path(a.patch).read_text(encoding='utf-8'))
artist=str(patch.get('artist','')).strip(); album=str(patch.get('album','')).strip(); key=f'{artist}|{album}'
rows=[x for x in data.get('albums',[]) if x.get('artist')==artist and x.get('title')==album]
if not artist or not album or not rows: sys.exit('Virhe: artistia ja albumia vastaavaa tietuetta ei löytynyt.')
if 'tracks' in patch:
 t=patch['tracks']
 if not isinstance(t,list) or not all(isinstance(x,str) and x.strip() for x in t): sys.exit('Virhe: tracks ei ole kelvollinen lista.')
 data.setdefault('tracks',{})[key]=[x.strip() for x in t]
if 'info' in patch:
 if not isinstance(patch['info'],dict): sys.exit('Virhe: info ei ole JSON-objekti.')
 target=data.setdefault('info',{}).setdefault(key,{})
 for k,v in patch['info'].items(): target.pop(k,None) if v is None else target.__setitem__(k,v)
if 'albumFields' in patch:
 if not isinstance(patch['albumFields'],dict): sys.exit('Virhe: albumFields ei ole JSON-objekti.')
 rows[0].update(patch['albumFields'])
Path(str(dp)+'.bak').write_text(dp.read_text(encoding='utf-8'),encoding='utf-8')
dp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Korjattu:',key)
