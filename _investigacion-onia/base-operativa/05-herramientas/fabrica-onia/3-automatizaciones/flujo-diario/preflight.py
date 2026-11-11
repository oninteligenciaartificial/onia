#!/usr/bin/env python3
"""Lectura efímera de login/cuota incluida. No crea threads, turns ni modelos."""
from datetime import datetime, timezone
import json
import math
import os
import selectors
import subprocess
import time

TIMEOUT = 20
MAX_BYTES = 512 * 1024
MAX_MESSAGES = 128
PLANS = {'free', 'go', 'plus', 'pro', 'prolite', 'promax', 'team', 'business',
         'enterprise', 'edu', 'edu_plus', 'edu_pro', 'sci', 'sci_plus'}
COMMAND = ('codex', '-c', 'forced_login_method="chatgpt"', '-c', 'model_provider="openai"',
           'app-server', '--listen', 'stdio://')
SOURCE = 'codex-app-server/account/read+account/rateLimits/read'


class PreflightError(ValueError):
    """Sólo códigos fijos; nunca contiene respuestas RPC, stderr, email o tokens."""
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def check(ok, code='PREFLIGHT_DATOS_INVALIDOS'):
    if not ok:
        raise PreflightError(code)


def instant():
    return datetime.now(timezone.utc).isoformat()


def validate(account, quota, started, completed):
    """Normaliza exclusivamente la respuesta de la lectura actual, sin historial/fallback."""
    check(isinstance(account, dict) and type(account.get('requiresOpenaiAuth')) is bool)
    identity = account.get('account')
    check(isinstance(identity, dict) and identity.get('type') == 'chatgpt'
          and account['requiresOpenaiAuth'] is True, 'LOGIN_CHATGPT_REQUERIDO')
    plan = identity.get('planType')
    check(isinstance(plan, str) and plan in PLANS, 'PLAN_INCLUIDO_NO_COMPROBADO')
    check(isinstance(quota, dict))
    ordinary = quota.get('ordinaryUsageAllowed')
    check(ordinary is None or type(ordinary) is bool)
    check(ordinary is not False, 'CUOTA_AGOTADA')
    check(ordinary is True, 'CUOTA_PERMISO_DESCONOCIDO')
    buckets = quota.get('rateLimitsByLimitId')
    if buckets is None:
        bucket = quota.get('rateLimits')
        check(isinstance(bucket, dict) and bucket.get('limitId') == 'codex', 'CUOTA_CODEX_DESCONOCIDA')
    else:
        check(isinstance(buckets, dict) and isinstance(buckets.get('codex'), dict), 'CUOTA_CODEX_DESCONOCIDA')
        bucket = buckets['codex']
    check(bucket.get('limitId') in (None, 'codex'))
    reached = bucket.get('rateLimitReachedType')
    check(reached is None or isinstance(reached, str))
    check(reached is None, 'CUOTA_AGOTADA')
    spend = bucket.get('spendControlReached')
    check(spend is None or type(spend) is bool)
    check(spend is not True, 'CUOTA_AGOTADA')
    windows = {}
    sampled = datetime.fromisoformat(completed).timestamp()
    for key in ('primary', 'secondary'):
        window = bucket.get(key)
        if window is None:
            continue
        check(isinstance(window, dict))
        used, duration, reset = (window.get(n) for n in ('usedPercent', 'windowDurationMins', 'resetsAt'))
        check(type(used) is int and 0 <= used <= 100)
        check(type(duration) is int and 0 < duration <= 2**31)
        check(type(reset) is int and 0 < reset < 2**63)
        check(used < 100, 'CUOTA_AGOTADA')
        # No se supone renovación a partir de un reset pasado.
        check(reset > sampled, 'CUOTA_VENTANA_VENCIDA')
        windows[key] = {'usedPercent': used, 'windowDurationMins': duration, 'resetsAt': reset}
    check(bool(windows), 'CUOTA_CODEX_DESCONOCIDA')
    return {'schema': 'onia-preflight-incluido-v1', 'fuente': SOURCE, 'iniciada': started,
            'completada': completed, 'login': 'chatgpt', 'plan': plan,
            'ordinaryUsageAllowed': True, 'limites': windows, 'permitido': True}


class RPC:
    """JSONL binario con plazo TOTAL; una línea parcial tampoco puede bloquear readline."""
    def __init__(self, process, deadline):
        self.process, self.deadline = process, deadline
        self.selector = selectors.DefaultSelector()
        self.selector.register(process.stdout, selectors.EVENT_READ)
        self.buffer, self.bytes, self.messages = b'', 0, 0

    def send(self, value):
        check(time.monotonic() < self.deadline, 'PREFLIGHT_TIMEOUT')
        self.process.stdin.write((json.dumps(value) + '\n').encode())
        self.process.stdin.flush()

    def read(self, ident):
        while True:
            check(time.monotonic() < self.deadline, 'PREFLIGHT_TIMEOUT')
            if b'\n' not in self.buffer:
                check(self.selector.select(max(0, self.deadline-time.monotonic())), 'PREFLIGHT_TIMEOUT')
                chunk = os.read(self.process.stdout.fileno(), 65536)
                check(bool(chunk), 'PREFLIGHT_RPC_FALLIDO')
                self.bytes += len(chunk)
                check(self.bytes <= MAX_BYTES, 'PREFLIGHT_RESPUESTA_EXCESIVA')
                self.buffer += chunk
                continue
            line, self.buffer = self.buffer.split(b'\n', 1)
            self.messages += 1
            check(self.messages <= MAX_MESSAGES, 'PREFLIGHT_RESPUESTA_EXCESIVA')
            def unique(pairs):
                result = {}
                for key, value in pairs:
                    check(key not in result)
                    result[key] = value
                return result
            def constant(_):
                raise PreflightError('PREFLIGHT_DATOS_INVALIDOS')
            value = json.loads(line, object_pairs_hook=unique, parse_constant=constant)
            check(isinstance(value, dict))
            if 'id' not in value:
                check(isinstance(value.get('method'), str))
                continue  # Notificación: nunca es una respuesta de cuota.
            check(type(value['id']) is int and value['id'] == ident, 'PREFLIGHT_RPC_FALLIDO')
            check('error' not in value and isinstance(value.get('result'), dict), 'PREFLIGHT_RPC_FALLIDO')
            return value['result']

    def close(self):
        self.selector.close()


def read_live(*, timeout=TIMEOUT, process_factory=subprocess.Popen):
    """Sin refresh proactivo, caché, compra/reset de créditos, herramientas o sesión LLM."""
    check(type(timeout) in (int, float) and math.isfinite(timeout) and 0 < timeout <= TIMEOUT)
    started, deadline = instant(), time.monotonic() + timeout
    process, rpc = None, None
    env = dict(os.environ)
    for key in ('OPENAI_API_KEY', 'CODEX_API_KEY', 'OPENAI_BASE_URL', 'CODEX_ACCESS_TOKEN'):
        env.pop(key, None)
    try:
        process = process_factory(list(COMMAND), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, bufsize=0, env=env)
        rpc = RPC(process, deadline)
        rpc.send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'onia_preflight_readonly', 'version': '1.0'}}})
        rpc.read(1)
        rpc.send({'method': 'initialized'})
        rpc.send({'id': 2, 'method': 'account/read', 'params': {'refreshToken': False}})
        account = rpc.read(2)
        rpc.send({'id': 3, 'method': 'account/rateLimits/read', 'params': {'excludeResetCreditDetails': True}})
        quota = rpc.read(3)
        check(time.monotonic() < deadline, 'PREFLIGHT_TIMEOUT')
        return validate(account, quota, started, instant())
    except PreflightError:
        raise
    except (OSError, ValueError, TypeError, KeyError, UnicodeError):
        raise PreflightError('PREFLIGHT_RPC_FALLIDO') from None
    finally:
        if rpc:
            rpc.close()
        if process:
            try:
                if process.poll() is None:
                    process.terminate()
                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=1)
            except (OSError, subprocess.TimeoutExpired):
                raise PreflightError('PREFLIGHT_RPC_FALLIDO') from None
            finally:
                for stream in (process.stdin, process.stdout):
                    stream.close()


def main():
    try:
        result = read_live()
        code = 0
    except PreflightError as error:
        result = {'schema': 'onia-preflight-incluido-v1', 'fuente': SOURCE, 'permitido': False,
                  'codigo': error.code, 'intento_finalizado': instant()}
        code = 2
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
