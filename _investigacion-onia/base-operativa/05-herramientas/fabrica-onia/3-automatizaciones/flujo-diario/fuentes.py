"""Índice Anthropic acotado. URLs remotas son datos; no se ejecuta ni sigue otro host."""
from datetime import date, datetime
from html.parser import HTMLParser
import re
import socket
import urllib.error
import urllib.parse
import urllib.request

from comun import lector, require, now

INDEX = 'https://www.anthropic.com/news'
MAX_ARTICLES = 3
MAX_LINKS = 20
EXCLUDED = {'announcements', 'models', 'product', 'policy', 'features', 'company', 'partnerships'}


def canonical(url):
    require(isinstance(url, str) and len(url) <= 250, 'URL_INVALIDA')
    u = urllib.parse.urlsplit(url)
    require(u.scheme == 'https' and u.netloc == 'www.anthropic.com' and not u.query
            and not u.fragment and not any(c in url for c in '\\\r\n'), 'URL_NO_PERMITIDA')
    require(u.path == '/news' or re.fullmatch(r'/news/[a-z0-9][a-z0-9-]{0,160}', u.path), 'RUTA_NO_PERMITIDA')
    return url


def fetch(url):
    canonical(url)
    request = urllib.request.Request(url, headers={'User-Agent': 'ONIA-bounded-reader/1.0',
        'Accept': 'text/html', 'Accept-Encoding': 'identity'})
    with lector.deadline(lector.TIMEOUT), urllib.request.build_opener(lector.NoRedirect()).open(
            request, timeout=lector.TIMEOUT) as response:
        require(response.status == 200 and response.geturl() == url, 'RESPUESTA_INVALIDA')
        require(response.headers.get_content_type() == 'text/html', 'TIPO_INVALIDO')
        require(response.headers.get('Content-Encoding', 'identity') == 'identity', 'COMPRESION_RECHAZADA')
        raw = response.read(lector.MAX_BYTES + 1)
        require(len(raw) <= lector.MAX_BYTES, 'TAMANO_EXCEDIDO')
        return raw


class Page(lector.Metadata):
    def __init__(self):
        super().__init__()
        self.links, self.headline, self.visible, self.description = [], [], [], ''
        self.in_h1 = False

    def handle_starttag(self, tag, attrs):
        # HTMLParser normaliza dateTime a datetime; reutiliza fechas y metadatos del lector.
        super().handle_starttag(tag, attrs)
        values = dict(attrs)
        if tag == 'h1':
            self.in_h1 = True
        if tag == 'a':
            href = values.get('href', '')
            if re.fullmatch(r'/news/[a-z0-9][a-z0-9-]{0,160}', href) and href.rsplit('/', 1)[1] not in EXCLUDED:
                url = 'https://www.anthropic.com' + href
                if url not in self.links and len(self.links) < MAX_LINKS:
                    self.links.append(url)
        if tag == 'meta' and values.get('name') == 'description':
            self.description = lector.clean(values.get('content', ''), 700)

    def handle_data(self, data):
        super().handle_data(data)
        if self.in_h1:
            self.headline.append(data)
        # Fecha visible primaria: no se obtiene de scripts ni de cabeceras HTTP.
        if re.fullmatch(r'(?:[A-Z][a-z]+) \d{1,2}, \d{4}', data.strip()):
            self.visible.append(data.strip())

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        if tag == 'h1':
            self.in_h1 = False


def parsed(raw):
    require(len(raw) <= lector.MAX_BYTES, 'TAMANO_EXCEDIDO')
    page = Page()
    page.feed(raw.decode('utf-8', errors='strict'))
    return page


def article(raw, url, consulted):
    canonical(url)
    require(url != INDEX, 'INDICE_NO_ES_NOTICIA')
    page = parsed(raw)
    title = lector.clean(''.join(page.headline), 240)
    require(title and page.publication, 'NOTICIA_SIN_FECHA_PRIMARIA')
    dates = {date.fromisoformat(value[:10]) for value in page.publication}
    require(len(dates) == 1, 'FECHAS_CONFLICTIVAS')
    published = dates.pop()
    visible = []
    for value in page.visible:
        for pattern in ('%B %d, %Y', '%b %d, %Y'):
            try:
                visible.append(datetime.strptime(value, pattern).date())
            except ValueError:
                pass
    require(published in visible and published <= datetime.fromisoformat(consulted).date(), 'FECHA_NO_COINCIDE')
    return {'url': url, 'titulo': title, 'publicada': published.isoformat(),
            'fecha_hecho': published.isoformat(), 'consultada': consulted,
            'resumen': page.description, 'sha256_respuesta': lector.sha(raw),
            'precision': 'dia', 'limites': 'Anuncio primario; fecha del anuncio, no despliegue individual. Revisión editorial pendiente.'}


def collect(urls=None, transport=fetch, cursor=0, clock=now):
    consulted = clock()
    errors, items = [], []
    index_hash = None
    try:
        if urls is None:
            raw = transport(INDEX)
            page = parsed(raw)
            require(page.headline and ''.join(page.headline).strip() == 'News' and page.links, 'INDICE_NO_RECONOCIDO')
            urls = page.links
            index_hash = lector.sha(raw)
            cursor %= len(urls)
            selected = (urls + urls)[cursor:cursor + min(MAX_ARTICLES, len(urls))]
            cursor = (cursor + len(selected)) % len(urls)
        else:
            require(0 < len(urls) <= MAX_ARTICLES, 'LIMITE_FUENTES')
            selected = list(dict.fromkeys(canonical(u) for u in urls))
        for url in selected:
            try:
                items.append(article(transport(url), url, clock()))
            except Exception:
                errors.append({'codigo': 'NOTICIA_INVALIDA_O_FUENTE_CAIDA', 'url': url})
    except Exception:
        errors.append({'codigo': 'INDICE_INVALIDO_O_FUENTE_CAIDA', 'url': INDEX})
    return {'consulta': consulted, 'finalizada': clock(), 'items': items, 'errores': errors,
            'cursor': cursor, 'indice_sha256': index_hash, 'sintetico': transport is not fetch}
