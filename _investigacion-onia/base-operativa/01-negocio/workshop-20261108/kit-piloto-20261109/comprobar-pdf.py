"""Comprueba texto/pies por página en estos PDF simples generados por Chromium.
No es parser PDF general ni sustituye inspección de la apariencia.
"""
from pathlib import Path
import re,zlib,json,sys

def text_pages(path):
 data=path.read_bytes();objects={int(n):b for n,b in re.findall(rb'(\d+) 0 obj\s*(.*?)\s*endobj',data,re.S)}
 def stream(body):
  b=re.search(rb'stream\r?\n(.*?)\r?\nendstream',body,re.S)[1]
  return zlib.decompress(b) if b'/FlateDecode' in body else b
 fonts={}
 for oid,body in objects.items():
  m=re.search(rb'/ToUnicode (\d+) 0 R',body)
  if not m:continue
  cmap=stream(objects[int(m[1])]);mapping={}
  for part in re.findall(rb'beginbfchar(.*?)endbfchar',cmap,re.S):
   for a,b in re.findall(rb'<([0-9A-F]+)>\s*<([0-9A-F]+)>',part):mapping[int(a,16)]=bytes.fromhex(b.decode()).decode('utf-16-be')
  for part in re.findall(rb'beginbfrange(.*?)endbfrange',cmap,re.S):
   for a,b,c in re.findall(rb'<([0-9A-F]+)>\s*<([0-9A-F]+)>\s*<([0-9A-F]+)>',part):
    for code in range(int(a,16),int(b,16)+1):mapping[code]=chr(int(c,16)+code-int(a,16))
  fonts[oid]=mapping
 pages=[]
 for body in objects.values():
  if not re.search(rb'/Type\s*/Page\b',body):continue
  resources={k:fonts[int(v)] for k,v in re.findall(rb'/(F\d+) (\d+) 0 R',body)}
  content=stream(objects[int(re.search(rb'/Contents (\d+) 0 R',body)[1])]);chunks=[]
  for block in re.findall(rb'BT\b(.*?)\bET',content,re.S):
   font=re.search(rb'/(F\d+) [\d.]+ Tf',block)
   if not font:continue
   mapping=resources[font[1]];strings=re.findall(rb'<([0-9A-Fa-f]+)>\s*Tj',block)
   chunks.append(''.join(mapping.get(int(s[i:i+4],16),'?') for s in strings for i in range(0,len(s),4)))
  pages.append(' '.join(chunks))
 return pages

def validate(folder):
 out=[]
 for name,total in [('laminas',7),('hoja',2),('guia',3)]:
  pages=text_pages(folder/(name+'.pdf'));assert len(pages)==total,(name,len(pages))
  for i,page in enumerate(pages,1):
   compact=re.sub(r'\s+','',page)
   expected=f'{i}de{total}';assert expected in compact,(name,i,'pie propio ausente')
   for j in range(1,total+1):
    if i!=j:assert f'{j}de{total}' not in compact,(name,i,'pie ajeno',j)
   out.append({'documento':name,'pagina':i,'pie_propio':True,'sin_pies_ajenos':True,'caracteres':len(page)})
 return out
if __name__=='__main__':
 print(json.dumps({'controles_por_pagina':validate(Path(sys.argv[1])),'limite':'Parser acotado a PDF Chromium con fuentes ToUnicode/Flate; no rasterización ni comprobación general de coordenadas.'},ensure_ascii=False))
