from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, html, hashlib
ROOT=Path(__file__).resolve().parent
BG='#102D32'; WHITE='#F8F4E9'; ACC='#DBED91'; MUT='#CBD8D4'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
# Text coordinates are shared by the SVG editable and the PNG render.
slides=[
('01', 'REVISAR TAMBIÉN ES TRABAJAR', [('Una agenda prolija',76,True),('puede no entrar.',76,True),('',25,False),('Antes de usarla, compará:',42,False),('01  ¿Están todas las tareas?',43,False),('02  ¿Cuánto dura cada una?',43,False),('03  ¿Respeta horarios fijos?',43,False)],'Si falta algo, pedí la corrección.','P02 · Lista de revisión'),
('02','CASO FICTICIO · P03',[('Todo parece entrar…',70,True),('',25,False),('Tiempo disponible: 120 min',46,False),('Tareas previstas: 105 min',46,False),('',25,False),('120 − 105 = 15',84,True),('Quedan 15 minutos.',44,False)],'Ahora cambia una duración →','Ejemplo preparado · no es una salida de IA'),
('03','CASO FICTICIO · P03',[('Pero faltan 10 min.',72,True),('',25,False),('Inventario pasa de 25 a 50 min.',42,False),('50 − 25 = 25 min más',53,True),('105 + 25 = 130 min de tareas',43,False),('130 − 120 = 10 min de más',43,False),('',25,False),('Decidí qué cambia.',54,True),('Después, ajustá el plan.',43,False)],'Una tabla ordenada no arregla la cuenta.','Ejemplo preparado · no es un resultado de alumno'),
('04','UN PEDIDO CON DATOS · P05',[('Antes de pedir',76,True),('un mensaje de venta…',65,True),('',25,False),('Completá estos cinco campos:',42,False),('Qué ofrecés: ______________',42,False),('A quién: __________________',42,False),('Qué incluye: ______________',42,False),('Cuánto cuesta: ____________',42,False),('Cómo se consulta: _________',42,False)],'Pedí dos borradores y revisá sus condiciones.','Ficha vacía · propuesta de práctica'),
('05','GUARDÁ ESTA LISTA',[('Pedir. Revisar.',80,True),('Corregir.',80,True),('',25,False),('Agenda: tareas, duraciones',45,False),('y horarios fijos.',45,False),('',25,False),('Mensaje: producto, persona,',45,False),('entrega, precio y consulta.',45,False),('',25,False),('Usá siempre tus propios datos.',43,False)],'Guardala para tu próxima agenda o mensaje.','P02 + P03 + P05 · práctica sin bot')]
checks=[]
def render(name,w,h,kicker,lines,cta,foot,story=False):
    im=Image.new('RGB',(w,h),BG); d=ImageDraw.Draw(im)
    els=[f'<rect width="{w}" height="{h}" fill="{BG}"/>']
    sizes=[]
    def text(s,x,y,size,bold=False,color=WHITE):
        f=ImageFont.truetype(BOLD if bold else FONT,size)
        box=d.textbbox((x,y),s,font=f,anchor='lt')
        assert box[2]<=w-55,(name,s,box)
        assert box[3]<h-75,(name,s,box)
        d.text((x,y),s,font=f,fill=color,anchor='lt')
        els.append(f'<text x="{x}" y="{y}" dominant-baseline="text-before-edge" font-family="DejaVu Sans" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{html.escape(s)}</text>')
        sizes.append(size)
    d.rectangle((72,180 if story else 70,170,190 if story else 80),fill=ACC)
    els.append(f'<rect x="72" y="{180 if story else 70}" width="98" height="10" fill="{ACC}"/>')
    text('ONIA  /  PRÁCTICA CON IA',72,215 if story else 110,27,True,MUT)
    text(kicker,72,280 if story else 180,29,True,ACC)
    y=365 if story else 280
    for s,size,b in lines:
        if s:text(s,72,y,size,b)
        y+=size*1.36
    cy=1510 if story else 1120
    assert y<cy-25,(name,y)
    text(cta,72,cy,35,True,ACC)
    text(foot,72,cy+85,26,False,MUT)
    if not story:text(f'{name} / 05',865,1240,27,True,MUT)
    (ROOT/'editables').mkdir(exist_ok=True); (ROOT/'png').mkdir(exist_ok=True)
    (ROOT/'editables'/f'{name}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'+''.join(els)+'</svg>')
    im.save(ROOT/'png'/f'{name}.png')
    checks.append({'archivo':f'png/{name}.png','dimensiones':[w,h],'modo':im.mode,'tipografia_minima_px':min(sizes),'limites_texto':'sin desborde según métricas DejaVu Sans','sha256':hashlib.sha256((ROOT/'png'/f'{name}.png').read_bytes()).hexdigest()})
for n,k,l,c,f in slides:render(n,1080,1350,k,l,c,f)
render('06-historia',1080,1920,'WORKSHOP · TRES CLASES POR GOOGLE MEET',[
('Claude de 0 a 100:',68,True),('tu negocio con IA',68,True),('',20,False),('Practicá pedir, revisar',46,False),('y corregir con tus datos.',46,False),('',20,False),('NOVIEMBRE 2026',30,True),('Viernes 13   ·   20:00',51,True),('Sábado 14   ·   14:00',51,True),('Lunes 16     ·   20:00',51,True),('Hora de Caracas / La Paz',37,False),('',20,False),('Grupal  Bs 50',56,True),('VIP  Bs 150 total',56,True),('5 cupos VIP totales',38,False),('Llamada privada de 30 minutos',38,False),('Disponibilidad por confirmar',30,False)],'Si te interesa, comentá NEGOCIO.','QR privado · Sergio confirma cada pago',True)
# Contact sheet at 360px feed width, story at 360px width.
canvas=Image.new('RGB',(1080,1090),'#E8E5DE')
for i,c in enumerate(checks):
    a=Image.open(ROOT/c['archivo']); a.thumbnail((360,640)); canvas.paste(a,((i%3)*360,(i//3)*450))
canvas.save(ROOT/'VISTA-CONJUNTA.jpg')
(ROOT/'comprobacion.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print('6 PNG RGB + 6 SVG + vista conjunta; límites de texto comprobados')
