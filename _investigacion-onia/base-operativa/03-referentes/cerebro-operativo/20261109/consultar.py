#!/usr/bin/env python3
"""Recuperación editorial offline mediante etiquetas explícitas, Python stdlib."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlsplit


DIRECTORIO = Path(__file__).resolve().parent
BASE = DIRECTORIO.parents[2]
USOS = ("ordenar", "vender", "ensenar", "contenido", "workshop", "ideas", "guiones", "automatizar")
REFERENTES = {
    "a": {"alex-hormozi", "pedro-buerbaum", "victor-heras", "iman-gadzhi", "justin-welsh", "alex-carrera"},
    "b": {"erik-taveras", "enrique-rocha", "ali-abdaal", "san-munoz", "cormac-hayden", "bastian-xu"},
    "c": {"gonzalo-teba", "beltran-briones", "toto-artuso", "nick-bare", "jeff-nippard", "alvaro-risoglio", "voltra"},
}


def exigir(condicion, mensaje):
    if not condicion:
        raise ValueError(mensaje)


def normalizar(valor):
    texto = unicodedata.normalize("NFKD", valor.strip().lower())
    return "".join(caracter for caracter in texto if not unicodedata.combining(caracter))


def etiqueta(valor):
    texto = normalizar(valor)
    if not re.fullmatch(r"[a-z0-9][a-z0-9 -]{0,79}", texto):
        raise argparse.ArgumentTypeError("La etiqueta debe tener de 1 a 80 letras, números, espacios o guiones.")
    return texto


def indexar(elementos, clave):
    indice = {elemento[clave]: elemento for elemento in elementos}
    exigir(len(indice) == len(elementos), f"Identificador duplicado en {clave}.")
    return indice


def verificar_pasaje(pasaje, contenidos):
    lineas = contenidos[pasaje["fuente"]].splitlines()
    inicio, fin = pasaje["desde"], pasaje["hasta"]
    exigir(type(inicio) is int and type(fin) is int, "Líneas de pasaje inválidas.")
    exigir(1 <= inicio <= fin <= len(lineas), "Pasaje fuera de la ficha.")
    texto = "\n".join(lineas[inicio - 1:fin])
    exigir(hashlib.sha256(texto.encode()).hexdigest() == pasaje["sha256"], "Huella de pasaje diferente.")


def cargar(ruta, base=BASE):
    catalogo = json.loads(ruta.read_text(encoding="utf-8"))
    exigir(catalogo["version"] == 1, "Versión de catálogo incompatible.")
    exigir(catalogo["naturaleza"] == "catalogo_de_conocimiento_editorial", "Naturaleza de catálogo inválida.")
    fuentes = indexar(catalogo["fuentes"], "id")
    contenidos = {}
    for fuente in fuentes.values():
        relativa = Path(fuente["ruta"])
        destino = (base / relativa).resolve()
        exigir(not relativa.is_absolute() and destino.is_relative_to(base.resolve()), "Fuente fuera de la base.")
        exigir(destino.is_file(), f"Fuente faltante — {fuente['ruta']}")
        datos = destino.read_bytes()
        exigir(hashlib.sha256(datos).hexdigest() == fuente["sha256"], f"Fuente alterada — {fuente['ruta']}")
        contenidos[fuente["id"]] = datos.decode("utf-8")

    referentes = indexar(catalogo["referentes"], "id")
    exigir(set(referentes) == set.union(*REFERENTES.values()), "Se requieren los 19 referentes asignados.")
    totales = {}
    for grupo, esperados in REFERENTES.items():
        actuales = {ref["id"] for ref in referentes.values() if ref["grupo"] == grupo}
        exigir(actuales == esperados, f"Integrantes incorrectos del grupo {grupo}.")
        cobertura = json.loads(contenidos[f"cobertura-{grupo}"])
        originales = indexar(cobertura["referentes"], "slug")
        totales[grupo] = 0
        for slug in sorted(esperados):
            ref = referentes[slug]
            original = originales[slug]
            heredada = ref["cobertura_heredada"]
            exigir(heredada["fuente"] == f"cobertura-{grupo}", "Cobertura de otro grupo.")
            total = sum(pieza["completa"] is True for pieza in original["piezas"])
            exigir(heredada["piezas_completas"] == total, "Conteo heredado diferente.")
            exigir(heredada["limites"] == original["faltantes"], "Límites heredados diferentes.")
            exigir(bool(heredada["limites"] or ref["limites_adicionales_ficha"]), "Faltan límites del referente.")
            exigir(bool(heredada["dependencia_entre_piezas"]), "Falta dependencia de muestra.")
            aceptacion = ref["aceptacion"]
            fila_aceptada = f"| cerebros-{grupo}-20261108 | `{aceptacion['commit_entrega']}`"
            exigir(fila_aceptada in contenidos[aceptacion["fuente"]], "Entrega ausente del grupo aceptado.")
            ruta_ficha = f"03-referentes/cerebros-profundos/{grupo}/{original['archivo']}"
            exigir(fuentes[slug]["ruta"] == ruta_ficha, "Ruta de ficha diferente de la cobertura.")
            exigir(ref["patron_en_ficha"]["fuente"] == slug, "Patrón enlazado a otra ficha.")
            verificar_pasaje(ref["patron_en_ficha"], contenidos)
            piezas = indexar(ref["piezas_seleccionadas"], "id")
            exigir(bool(piezas), f"Falta pieza para {slug}.")
            for pieza in piezas.values():
                exigir(pieza in original["piezas"] and pieza["completa"] is True, "Pieza ajena a cobertura completa.")
                exigir(pieza["url"] != original["pagina_comercial"]["url"], "Página comercial contada como pieza.")
                url = urlsplit(pieza["url"])
                exigir(url.scheme in ("https", "http") and bool(url.netloc), "URL pública inválida.")
                exigir(pieza["url"] in contenidos[slug], f"URL ausente de la ficha {slug}.")
            totales[grupo] += total
    total_esperado = {"referentes": 19, "piezas": sum(totales.values()), "grupos": totales}
    exigir(catalogo["cobertura_total_heredada"] == total_esperado, "Total heredado diferente.")

    indexar(catalogo["patrones"], "id")
    piezas_usadas = set()
    for patron in catalogo["patrones"]:
        slug = patron["referente"]
        ref = referentes[slug]
        exigir(patron["pieza"] in {p["id"] for p in ref["piezas_seleccionadas"]}, "Patrón sin pieza seleccionada.")
        exigir(patron["pasaje"]["fuente"] == slug, "Pasaje enlazado a otro referente.")
        verificar_pasaje(patron["pasaje"], contenidos)
        lineas = contenidos[slug].splitlines()
        encabezados = [linea for linea in lineas[:patron["pasaje"]["desde"]]
                       if re.match(r"^## P\d+\b", linea)]
        exigir(bool(encabezados) and encabezados[-1].startswith(f"## {patron['pieza']} ·"), "Pasaje de otra pieza.")
        exigir(bool(patron["temas"]) and all(etiqueta(t) == t for t in patron["temas"]), "Temas inválidos.")
        exigir(bool(patron["usos"]) and set(patron["usos"]) <= set(USOS), "Usos inválidos.")
        for campo in ("titulo", "hecho_documentado", "inferencia_acotada", "localizacion_temporal_heredada"):
            exigir(isinstance(patron[campo], str) and bool(patron[campo].strip()), f"Falta {campo}.")
        for campo in ("aplicacion", "comprobacion_pendiente"):
            exigir(bool(patron["propuesta_onia"][campo].strip()), f"Falta propuesta {campo}.")
        piezas_usadas.add((slug, patron["pieza"]))
    seleccionadas = {(ref["id"], p["id"]) for ref in referentes.values() for p in ref["piezas_seleccionadas"]}
    exigir(piezas_usadas == seleccionadas, "Hay piezas seleccionadas sin patrón.")
    for antecedente in catalogo["reglas_propuestas_onia"]["antecedentes"]:
        exigir(antecedente in fuentes, "Antecedente ausente.")
    exigir(set(catalogo["limites_comunes"]) >= {"lectura", "asr", "visual", "audio", "privado", "portabilidad", "vigencia", "consulta", "aplicacion"}, "Faltan límites comunes.")
    return catalogo


def consultar(catalogo, temas, usos):
    referentes = indexar(catalogo["referentes"], "id")
    fuentes = indexar(catalogo["fuentes"], "id")
    seleccion = [
        patron for patron in catalogo["patrones"]
        if (not temas or set(temas).intersection(patron["temas"]))
        and (not usos or set(usos).intersection(patron["usos"]))
    ]
    seleccion.sort(key=lambda p: (not referentes[p["referente"]]["prioridad_editorial"], p["referente"], p["id"]))
    resultados = []
    for patron in seleccion:
        ref = referentes[patron["referente"]]
        pieza = next(p for p in ref["piezas_seleccionadas"] if p["id"] == patron["pieza"])
        resultados.append({
            **patron,
            "nombre": ref["nombre"],
            "ficha": fuentes[ref["id"]],
            "patron_en_ficha": ref["patron_en_ficha"],
            "fuente_publica": pieza,
            "aceptacion": {**ref["aceptacion"], "documento": fuentes[ref["aceptacion"]["fuente"]]},
            "cobertura_heredada_referente": ref["cobertura_heredada"],
            "limites_adicionales_ficha": ref["limites_adicionales_ficha"],
        })
    return {
        "consulta": {"temas": sorted(set(temas)), "usos": sorted(set(usos))},
        "cantidad": len(resultados),
        "mensaje": "Coincidencias por etiquetas explícitas." if resultados else "Sin resultados en las etiquetas del catálogo. La ausencia se limita a esta selección documental.",
        "limites_comunes": catalogo["limites_comunes"],
        "reglas_propuestas_onia": catalogo["reglas_propuestas_onia"],
        "antecedentes": [fuentes[f] for f in catalogo["reglas_propuestas_onia"]["antecedentes"]],
        "resultados": resultados,
    }


def markdown(resultado):
    lineas = ["# Consulta editorial OnIA", "", resultado["mensaje"], "", f"{resultado['cantidad']} patrones recuperados.", "", "## Límites comunes", ""]
    lineas.extend(f"- {texto}" for texto in resultado["limites_comunes"].values())
    lineas.extend(["", resultado["reglas_propuestas_onia"]["autoridad"]])
    for item in resultado["resultados"]:
        ficha = (BASE / item["ficha"]["ruta"]).as_posix()
        cierre = (BASE / item["aceptacion"]["documento"]["ruta"]).as_posix()
        pieza = item["fuente_publica"]
        cobertura = item["cobertura_heredada_referente"]
        lineas.extend([
            "", f"## {item['id']} · {item['titulo']}", "",
            f"Hecho documentado. {item['hecho_documentado']}", "",
            f"Inferencia acotada. {item['inferencia_acotada']}", "",
            f"Propuesta OnIA. {item['propuesta_onia']['aplicacion']}", "",
            f"Comprobación pendiente. {item['propuesta_onia']['comprobacion_pendiente']}", "",
            f"Localización heredada. {item['localizacion_temporal_heredada']}", "",
            f"Cobertura de la pieza. {pieza['cobertura']}", "",
            f"Procedencia temporal. {pieza['fuente_tiempos']}", "",
            f"Dependencia de muestra. {cobertura['dependencia_entre_piezas']}", "",
            "### Límites heredados del referente", "",
        ])
        lineas.extend(f"- {limite}" for limite in cobertura["limites"] + item["limites_adicionales_ficha"])
        lineas.extend([
            "", f"[Ficha, pasaje]({ficha}:{item['pasaje']['desde']}) · [Patrón en ficha]({ficha}:{item['patron_en_ficha']['desde']}) · [Pieza pública]({pieza['url']}) · [Cierre aceptado]({cierre})",
            "", f"Entrega aceptada de origen `{item['aceptacion']['commit_entrega']}`.",
        ])
    return "\n".join(lineas) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogo", type=Path, default=DIRECTORIO / "catalogo.json")
    comandos = parser.add_subparsers(dest="comando", required=True)
    comandos.add_parser("validar", help="Verificar fuentes, pasajes y cobertura heredada.")
    comandos.add_parser("etiquetas", help="Listar vocabulario explícito.")
    consulta = comandos.add_parser("consultar", help="Filtrar por tema y uso, sin red.")
    consulta.add_argument("--tema", action="append", type=etiqueta, default=[])
    consulta.add_argument("--uso", action="append", type=etiqueta, choices=USOS, default=[])
    consulta.add_argument("--formato", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args(argv)
    try:
        catalogo = cargar(args.catalogo)
        if args.comando == "validar":
            resultado = {
                "integridad": "correcta",
                "referentes": len(catalogo["referentes"]),
                "patrones": len(catalogo["patrones"]),
                "piezas_seleccionadas": sum(len(ref["piezas_seleccionadas"]) for ref in catalogo["referentes"]),
                "piezas_heredadas": catalogo["cobertura_total_heredada"]["piezas"],
                "fuentes_locales": len(catalogo["fuentes"]),
            }
        elif args.comando == "etiquetas":
            resultado = {"temas": sorted({t for p in catalogo["patrones"] for t in p["temas"]}), "usos": list(USOS)}
        else:
            resultado = consultar(catalogo, args.tema, args.uso)
            if args.formato == "markdown":
                print(markdown(resultado), end="")
                return 0
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, AttributeError, IndexError, argparse.ArgumentTypeError) as error:
        print(json.dumps({"error": "Catálogo o fuentes inválidos", "detalle": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
