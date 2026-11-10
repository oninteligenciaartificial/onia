"""Sergio carga el webhook desde una terminal privada; nunca imprime sus valores."""
import getpass
import os
import pwd
from pathlib import Path
import sys
import warnings

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_boss import no_links, private_write, Rejected, locked
from harness_retorno import validate_secret


def main():
    if pwd.getpwuid(os.getuid()).pw_name != 'onia-codex-worker':
        raise Rejected('Ejecutar como onia-codex-worker en el VPS.')
    if not sys.stdin.isatty():
        raise Rejected('Ejecutar en una terminal interactiva del VPS.')
    root = no_links(Path.home() / 'operacion/puente-boss')
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    path = root / 'webhook.json'
    with locked(root), warnings.catch_warnings():
        warnings.simplefilter('error', getpass.GetPassWarning)
        if path.exists():
            raise Rejected('El archivo ya existe. Se conserva; coordinar una rotación explícita.')
        secret = {'url': getpass.getpass('URL de la rutina (oculta): '),
                  'clave': getpass.getpass('Clave sola, sin Bearer (oculta): ')}
        validate_secret(secret)
        private_write(path, secret)
    print('Webhook guardado con permisos privados. No se envió ninguna petición.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, getpass.GetPassWarning):
        print('No se guardó: revisar terminal, formato HTTPS, clave y archivo previo; valores ocultos.', file=sys.stderr)
        sys.exit(2)
