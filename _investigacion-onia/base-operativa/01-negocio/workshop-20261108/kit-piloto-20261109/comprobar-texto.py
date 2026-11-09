"""Controles documentales sin red ni dependencias externas; no validan renderizado."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent


class Node:
    def __init__(self, tag="root", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def find(self, tag=None, attr=None):
        result = []
        for c in self.children:
            if isinstance(c, Node):
                if (tag is None or c.tag == tag) and (attr is None or attr in c.attrs):
                    result.append(c)
                result.extend(c.find(tag, attr))
        return result


class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(text)
        assert len(self.stack) == 1, "HTML sin cerrar"

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {"meta", "link", "br", "hr", "img", "input"}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        assert self.stack[-1].tag == tag, (tag, self.stack[-1].tag)
        self.stack.pop()

    def handle_data(self, text):
        self.stack[-1].children.append(text)


def agenda_errors(rows, inventory=25):
    def mins(t):
        a, b = map(int, t.split(":"))
        return a * 60 + b
    durations = {"Revisar caja": 10, "Confirmar pedidos": 20,
                 "Contar inventario": inventory, "Preparar entregas": 15,
                 "Proveedor": 20, "Pausa": 15, "Tiempo libre": 15}
    errors, seen, prev = [], set(), 540
    for a, b, task in rows:
        a, b = mins(a), mins(b)
        if a != prev or b <= a or a < 540 or b > 660:
            errors.append("cobertura/solapamiento")
        if task in seen:
            errors.append("duplicado")
        seen.add(task)
        if b - a != durations.get(task):
            errors.append("duración: " + task)
        if task == "Revisar caja" and a != 540:
            errors.append("caja")
        if task == "Confirmar pedidos" and b > 600:
            errors.append("pedidos")
        if task == "Proveedor" and (a, b) != (610, 630):
            errors.append("proveedor")
        if task == "Pausa" and (a, b) != (630, 645):
            errors.append("pausa")
        prev = b
    errors += ["falta: " + task for task in durations.keys() - seen]
    if prev != 660:
        errors.append("final")
    return errors


def cells(table):
    return [[c.text() for c in row.find("td")] for row in table.find("tr") if row.find("td")]


def contrast(a, b):
    def lum(color):
        rgb = [int(color[i:i+2], 16)/255 for i in (1, 3, 5)]
        linear = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb]
        return sum(x*y for x, y in zip(linear, (.2126, .7152, .0722)))
    x, y = sorted((lum(a), lum(b)))
    return (y+.05)/(x+.05)


def main():
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "evidencia/texto-v1.json"
    assert not dest.exists(), "No sobrescribir evidencia: elegí otro destino."
    controls = []
    def check(name, condition):
        assert condition, name
        controls.append({"control": name, "resultado": "OK"})
    source = ROOT.parent / "noche-20261109/CLASE1-PRIMEROS10MIN.md"
    text = source.read_text()
    prompts = re.findall(r"```text\n(.*?)\n```", text, re.S)
    docs = {name: HTML((ROOT/(name+".html")).read_text()).root
            for name in ("index", "laminas", "hoja", "guia")}
    for name, doc in docs.items():
        check(name + ": idioma español", doc.find("html")[0].attrs.get("lang") == "es")
        for node in doc.find():
            for attr in ("href", "src"):
                href = node.attrs.get(attr)
                if href:
                    check(name + ": destino local " + href,
                          not re.match(r"(?:[a-z]+:)?//", href) and
                          (href.startswith("#") or (ROOT/href.split("#")[0]).is_file()))
        check(name + ": sin servicios/formularios", not doc.find("iframe") and not doc.find("form"))
    hoja, guia = docs["hoja"], docs["guia"]
    check("A/B en hoja idénticos a fuente", [n.text() for n in hoja.find("textarea")] == prompts)
    check("A/B impresos completos e idénticos", [n.text() for n in hoja.find(attr="data-print-prompt")] == prompts)
    check("A/B en guía idénticos a fuente", [n.text() for n in guia.find(attr="data-prompt")] == prompts)
    check("7 láminas, 2 hojas y 3 páginas de guía declaradas",
          len(docs["laminas"].find("section")) == 7 and len(hoja.find("section")) == 2 and len(guia.find("section")) == 3)
    samples = [cells(t) for doc in docs.values() for t in doc.find("table", "data-sample")]
    check("tres muestras iguales", len(samples) == 3 and all(s == samples[0] for s in samples))
    ref = [line.strip("| ").split(" | ") for line in text.splitlines()
           if re.match(r"\| \d\d:\d\d \|", line)]
    check("muestra idéntica a agenda fuente", samples[0] == ref)
    check("A respeta cobertura, duración, orden, bloques y límites", not agenda_errors(samples[0]))
    check("fallo material: omitir pausa se rechaza",
          "falta: Pausa" in agenda_errors([r for r in samples[0] if r[2] != "Pausa"]))
    check("fallo material: acortar inventario en B se rechaza",
          "duración: Contar inventario" in agenda_errors(samples[0], 50))
    check("A=105, libre15; B=130, exceso10", sum((10,20,25,15,20,15)) == 105 and sum((10,20,50,15,20,15))-120 == 10)
    cases = [cells(t) for doc in docs.values() for t in doc.find("table", "data-case")]
    check("caso idéntico en láminas y hoja", len(cases) == 2 and cases[0] == cases[1])
    check("duraciones de ficha A", [r[1] for r in cases[0]] == ["10 min","20 min","25 min","15 min","20 min","15 min"])
    timeline = [t for t in guia.find("table") if t.attrs.get("class") == "timeline"][0]
    intervals = re.findall(r"(\d\d:\d\d)–(\d\d:\d\d)", timeline.text())
    # Sólo intervalos al inicio de la primera celda (el texto tiene también horarios del caso).
    intervals = [re.match(r"(\d\d:\d\d)–(\d\d:\d\d)", row[0]).groups() for row in cells(timeline)]
    check("tiempos guía = piloto", intervals == [("00:00","01:00"),("01:00","02:00"),("02:00","03:00"),("03:00","04:00"),("04:00","06:00"),("06:00","08:00"),("08:00","09:00"),("09:00","10:00")])
    check("muestras rotuladas sin atribución falsa", all("No es salida de Claude ni resultado de alumno" in d.text() for d in (docs["laminas"],hoja,guia)))
    css = (ROOT/"kit.css").read_text()
    check("CSS sin importaciones ni recursos remotos", not re.search(r"@import|url\(",css))
    check("impresión sin textarea recortado", ".copybox{display:none}.print-only{display:block}" in css)
    pairs = [("#142e38","#faf8f0"),("#00675e","#faf8f0"),("#834000","#fff0db"),("#142e38","#e2efea"),("#ffffff","#142e38")]
    ratios = [{"texto":a,"fondo":b,"ratio":round(contrast(a,b),2)} for a,b in pairs]
    check("pares de color del diseño >=4.5:1", all(r["ratio"] >= 4.5 for r in ratios))
    source_names = ["CLASE1-PRIMEROS10MIN.md","OFERTA-Y-RECORRIDO.md","SINTESIS-PROPUESTA.md","CONTROL-EDITORIAL-Y-PENDIENTES.md"]
    sources = [ROOT.parent/"noche-20261109"/n for n in source_names]
    base=ROOT.parents[2]
    sources += [base/"05-herramientas/2026-11-08-harness"/n for n in ("00-decisiones.md","plan-workshop.md")]
    receipt = {"fecha":datetime.now(timezone.utc).isoformat(),"resultado":"OK documental; renderizado pendiente",
               "controles":controls,"contraste_diseno":ratios,
               "fuentes":[{"ruta":str(p.relative_to(base)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources],
               "limites":["No certifica impresión real ni capturas de Chromium", "No prueba Claude, alumno, audio ni revisión independiente"]}
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"resultado":receipt["resultado"],"controles":len(controls),"salida":str(dest)},ensure_ascii=False))


if __name__ == "__main__":
    main()
