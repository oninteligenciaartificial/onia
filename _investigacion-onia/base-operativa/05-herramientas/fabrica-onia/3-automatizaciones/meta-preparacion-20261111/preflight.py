"""Inventario local de lectura. --ensayo reutiliza el ensayo aceptado con red bloqueada.
No lee entorno, credenciales, DB privadas ni configuración de cuentas.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[3]
ADAPTER = HERE.parent / 'meta-canales-20261111'
CHANNELS = ('instagram_comentario', 'instagram_dm', 'facebook_comentario', 'facebook_dm')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preflight(ensayo=False):
    files = [ADAPTER / name for name in (
        'adaptador.py', 'motor.py', 'ensayo.py', 'test_canales.py',
        'contrato-canales.json', 'oferta-referencia.json', 'config.ejemplo.json',
        'fixtures/recorridos.json', 'fixtures/resultados.json')]
    reference = json.loads((ADAPTER / 'oferta-referencia.json').read_text())
    reference['decisiones'] = '05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md'
    reference['oferta'] = reference['catalogo']
    for key in ('decisiones', 'oferta'):
        files.append(BASE / reference[key])
    manifest = {str(p.relative_to(BASE)): digest(p) if p.is_file() else None for p in files}
    # El adaptador firma el objeto oferta canónico, no el catálogo completo.
    catalog_offer = json.loads((BASE / reference['catalogo']).read_text())['oferta']
    canonical_offer = json.dumps(catalog_offer, ensure_ascii=False, sort_keys=True,
                                separators=(',', ':'))
    offer = (digest(BASE / reference['decisiones']) == reference['decisiones_sha256'] and
             hashlib.sha256(canonical_offer.encode()).hexdigest() == reference['oferta_sha256'])
    contract = json.loads((ADAPTER / 'contrato-canales.json').read_text())
    local = (all(manifest.values()) and offer and
             [c['canal'] for c in contract['canales']] == list(CHANNELS) and
             contract['conector_real_habilitado'] is False and contract['envios_reales'] == 0)
    result = {
        'schema': 'onia-meta-preflight-v1', 'alcance': 'LOCAL_SOLO_LECTURA_NO_E2E',
        'artefactos_sha256': manifest, 'contrato_local_correcto': bool(local),
        'hashes_oferta_coinciden': offer,
        'vigencia_en_fecha_actual': 'no_evaluada; ensayo con reloj fijo, no habilita venta',
        'cuentas_credenciales_permisos_versiones_remotos': 'inaccesibles_no_consultados',
        'n8n_version_instalada': None, 'n8n_mcp_disponible_en_sesion': False,
        'canales': [{'canal': c, 'contrato_local': bool(local), 'ensayo_local': 'no_ejecutado',
                     'cuenta_actual': 'desconocida', 'credencial_actual': 'desconocida',
                     'permisos_version_ventana': 'desconocidos', 'e2e_real': False,
                     'listo_para_conectar': False} for c in CHANNELS],
        'ensayo': None, 'archivos_fuente_intactos': True, 'correcto': bool(local)}
    if ensayo:
        # Ejecuta el programa existente sin copiar su motor ni sus fixtures.
        # El proceso hijo no puede abrir sockets, ni siquiera por error futuro.
        wrapper = """import runpy, socket, sys
sys.dont_write_bytecode = True
def deny(*args, **kwargs):
    raise RuntimeError('RED_BLOQUEADA_PREFLIGHT')
socket.socket = deny
socket.create_connection = deny
sys.path.insert(0, sys.argv[1])
runpy.run_path(sys.argv[1] + '/ensayo.py', run_name='__main__')
"""
        run = subprocess.run([sys.executable, '-I', '-B', '-c', wrapper, str(ADAPTER)],
                             capture_output=True, text=True, timeout=60)
        if run.returncode:
            # No publicar tracebacks arbitrarios que pudieran incluir datos futuros.
            result['ensayo'] = {'correcto': False, 'exit_code': run.returncode}
            result['correcto'] = False
        else:
            data = json.loads(run.stdout)
            good = (data['tipo_evidencia'] == 'SIMULACION_LOCAL_NO_E2E' and
                    data['envios_reales'] == 0 and
                    [c['canal'] for c in data['canales']] == list(CHANNELS) and
                    len(data['resultados_transporte_por_canal']) == 16)
            result['ensayo'] = {'correcto': good, 'exit_code': 0, 'resultado': data}
            result['correcto'] = bool(local and good)
            for channel in result['canales']:
                channel['ensayo_local'] = 'ejecutado_sintetico' if good else 'fallo'
        result['archivos_fuente_intactos'] = manifest == {
            str(p.relative_to(BASE)): digest(p) if p.is_file() else None for p in files}
        result['correcto'] &= result['archivos_fuente_intactos']
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ensayo', action='store_true', help='DB temporales privadas; sin red')
    args = parser.parse_args()
    report = preflight(args.ensayo)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report['correcto'] else 1)
