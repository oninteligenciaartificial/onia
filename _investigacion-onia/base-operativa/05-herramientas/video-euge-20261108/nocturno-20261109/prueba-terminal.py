import copy
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('captura',Path(__file__).with_name('ejecutar.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
for frames,expected in [([], 'sin_fotogramas'),([{'file':'fixture.png'}], 'parcial')]:
 raw={'status':'en_curso','frames':frames};before=copy.deepcopy(raw)
 result=m.terminal_result(raw,137)
 assert result['estado_efectivo']==expected
 assert result['estado_manifiesto']=='en_curso'
 assert result['diagnostico_efectivo']=='SALIDA_SIN_MANIFIESTO_TERMINAL'
 assert result['rc']==137 and raw==before
 assert result['visionado_completo_acreditado'] is False
assert m.terminal_result({'status':'en_curso'},124,expired=True)['diagnostico_efectivo']=='LIMITE_DE_TIEMPO'
assert m.terminal_result({'status':'en_curso'},143,interrupted=15)['diagnostico_efectivo']=='INTERRUMPIDO'
assert m.terminal_result({'status':'parcial','diagnostico':'AVANCE_DETENIDO'},3)['diagnostico_efectivo']=='AVANCE_DETENIDO'
print('OK: salida terminal tras muerte, timeout e interrupción; manifiesto original intacto.')
