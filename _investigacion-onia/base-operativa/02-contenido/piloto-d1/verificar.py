"""QA del MP4 real y contacto; sólo usa FFmpeg, FFprobe y Pillow existentes."""
from pathlib import Path
from html.parser import HTMLParser
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
VIDEO = ROOT / 'd1-piloto-silencioso.mp4'
FRAMES = ROOT / 'fotogramas'
FRAMES.mkdir(exist_ok=True)

def run(args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)

probe = json.loads(run(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(VIDEO)]).stdout)
(ROOT / 'metadata.json').write_text(json.dumps(probe, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
streams = probe['streams']
videos = [s for s in streams if s['codec_type'] == 'video']
assert len(videos) == 1, 'Se esperaba una sola pista de video'
v = videos[0]
assert (v['codec_name'], v['width'], v['height'], v['r_frame_rate']) == ('h264', 1080, 1920, '24/1')
assert len(streams) == 1, 'No debe haber audio ni pistas adicionales'
assert abs(float(probe['format']['duration']) - 43) < 0.001
assert int(v['nb_read_frames']) == 1032
decode = run(['ffmpeg', '-hide_banner', '-v', 'error', '-xerror', '-threads', '1', '-i', str(VIDEO), '-map', '0:v:0', '-f', 'null', '-'])
(ROOT / 'decodificacion.log').write_text('Exit code: 0\n1032 fotogramas; decodificación completa sin errores.\n' + decode.stderr, encoding='utf-8')

class CopyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.active = []
        self.copies = {}
        self.scenes = []
    def handle_starttag(self, tag, attrs):
        if tag in ('meta', 'link', 'br', 'img', 'input', 'hr'):
            return
        self.depth += 1
        a = dict(attrs)
        if 'data-copy' in a:
            self.active.append({'id': a['data-copy'], 'depth': self.depth, 'parts': []})
        if tag == 'section':
            self.scenes.append([a['id'], float(a['data-start']), float(a['data-duration'])])
    def handle_data(self, data):
        for item in self.active:
            item['parts'].append(data)
    def handle_endtag(self, tag):
        for item in self.active[:]:
            if item['depth'] == self.depth:
                text = ' '.join(''.join(item['parts']).split())
                self.copies.setdefault(item['id'], []).append(text)
                self.active.remove(item)
        self.depth -= 1

expected = {
    'consulta': ['Consulta: ¿Es este viernes?'],
    'ficha': ['Fecha: por confirmar', 'Fecha: por confirmar'],
    'instruccion': ['Respondé sólo con lo confirmado. Si falta un dato, decilo'],
    'borrador': ['La fecha todavía no está confirmada; no puedo confirmar que sea este viernes'],
    'comparacion-ficha': ['Ficha: fecha por confirmar'],
    'comparacion-borrador': ['Borrador: fecha no confirmada'],
    'origen': ['“Este viernes” viene de la pregunta'],
    'ensenanza': ['Antes de usar la respuesta, revisá qué información la respalda'],
    'cta': ['¿Qué consulta de tu trabajo probarías? Contámela en comentarios'],
}
parser = CopyParser()
parser.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
assert parser.copies == expected, {'expected': expected, 'actual': parser.copies}
assert parser.scenes == [['scene1', 0, 8], ['scene2', 8, 10], ['scene3', 18, 9], ['scene4', 27, 10], ['scene5', 37, 6]]

samples = [('inicio', 0), ('escena-1', 4), ('corte-2', 8), ('escena-2', 13), ('corte-3', 18), ('escena-3', 22), ('corte-4', 27), ('escena-4', 32), ('corte-5', 37), ('escena-5', 40), ('final', 42.958333)]
for name, at in samples:
    run(['ffmpeg', '-hide_banner', '-v', 'error', '-y', '-threads', '1', '-ss', str(at), '-i', str(VIDEO), '-frames:v', '1', '-threads', '1', str(FRAMES / f'{name}.png')])

font = ImageFont.truetype(str(ROOT / 'assets/segoeui.ttf'), 26)
bold = ImageFont.truetype(str(ROOT / 'assets/segoeuib.ttf'), 31)
contact = Image.new('RGB', (1320, 1780), '#e0e5df')
draw = ImageDraw.Draw(contact)
draw.text((30, 21), 'D1 / CONTACTO DEL MP4 EXPORTADO', font=bold, fill='#163832')
draw.text((30, 66), '43 s · 1080×1920 · H.264 · 24 fps · SILENCIOSO', font=font, fill='#163832')
panels = [('escena-1', '01 · 0–8 s / muestra 4 s'), ('escena-2', '02 · 8–18 s / muestra 13 s'), ('escena-3', '03 · 18–27 s / muestra 22 s'), ('escena-4', '04 · 27–37 s / muestra 32 s'), ('escena-5', '05 · 37–43 s / muestra 40 s'), ('final', 'Final · 42,958 s')]
for i, (name, label) in enumerate(panels):
    x = 30 + (i % 3) * 440
    y = 127 + (i // 3) * 825
    panel = Image.open(FRAMES / f'{name}.png').convert('RGB').resize((400, 711), Image.Resampling.LANCZOS)
    contact.paste(panel, (x, y))
    draw.text((x, y + 725), label, font=font, fill='#163832')
contact.save(ROOT / 'contacto-visual.jpg', quality=95, subsampling=0)

check_raw = (ROOT / 'check.log').read_text(encoding='utf-8-sig')
check = json.loads(check_raw[check_raw.index('{'):])
result = {
    'video': VIDEO.name, 'sha256': hashlib.sha256(VIDEO.read_bytes()).hexdigest(), 'bytes': VIDEO.stat().st_size,
    'codec': v['codec_name'], 'dimensions': [v['width'], v['height']], 'durationSeconds': float(probe['format']['duration']),
    'fps': v['r_frame_rate'], 'framesDecoded': int(v['nb_read_frames']), 'audioStreams': 0, 'decodeExitCode': 0,
    'exactCardsMatch': True, 'singleCTA': True, 'sceneTiming': parser.scenes,
    'check': {'ok': check['ok'], 'lintErrors': check['lint']['errorCount'], 'lintWarnings': check['lint']['warningCount'], 'runtimeErrors': check['runtime']['errorCount'], 'layoutErrors': check['layout']['errorCount'], 'contrastPassed': check['contrast']['passed'], 'contrastChecked': check['contrast']['checked']},
    'samples': [{'file': f'fotogramas/{name}.png', 'time': at} for name, at in samples],
    'limits': ['Muestreo visual; no visionado humano continuo.', 'Sin audio por diseño; voz, música, SFX y sincronía no evaluados.', 'Comprensión humana y aprobación editorial pendientes de Jefa.'],
}
(ROOT / 'verificacion.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
manifest = {str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT / 'index.html', ROOT / 'run.mjs', ROOT / 'hyperframes.json', *sorted((ROOT / 'assets').iterdir()), VIDEO]}
(ROOT / 'sha256.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
