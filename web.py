#!/usr/bin/env python3
"""Interface local de teste do ELEV AI (roda no navegador, so na sua maquina).

    python web.py               # http://localhost:8000
    python web.py --offline

Nao e a interface do cliente final: e a bancada de teste para conferir se o
agente responde certo antes de conectar em qualquer canal.
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from elev.agente import AgenteElev
from elev.armazenamento import registrar_lead, salvar_registro
from elev.config import carregar_config

SESSOES: dict[str, AgenteElev] = {}
CONFIG = None

PAGINA = """<!doctype html>
<html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ELEV AI - teste local</title><style>
:root{color-scheme:light dark}
body{font:15px/1.5 system-ui,sans-serif;margin:0;background:#0f1115;color:#e8e8ea;
display:flex;flex-direction:column;height:100vh}
header{padding:14px 18px;background:#171a21;border-bottom:1px solid #262a33}
header b{color:#5ac8fa}header span{color:#8b909b;font-size:13px;margin-left:8px}
#chat{flex:1;overflow-y:auto;padding:18px;display:flex;flex-direction:column;gap:10px}
.msg{max-width:70ch;padding:10px 14px;border-radius:14px;white-space:pre-wrap}
.cliente{align-self:flex-end;background:#2a5bd7}
.agente{align-self:flex-start;background:#1e222b;border:1px solid #2b3039}
.aviso{align-self:center;font-size:12px;color:#f0b400;background:#2a2415;
padding:6px 12px;border-radius:8px}
form{display:flex;gap:8px;padding:14px 18px;background:#171a21;border-top:1px solid #262a33}
input{flex:1;padding:11px 14px;border-radius:10px;border:1px solid #2b3039;
background:#0f1115;color:inherit;font:inherit}
button{padding:11px 18px;border:0;border-radius:10px;background:#2a5bd7;color:#fff;
font:inherit;cursor:pointer}button:disabled{opacity:.5}
button.sec{background:#2b3039}
</style></head><body>
<header><b>ELEV AI</b><span id="modo"></span></header>
<div id="chat"></div>
<form id="f"><input id="txt" placeholder="Escreva como um cliente escreveria..." autocomplete="off" autofocus>
<button id="env">Enviar</button><button type="button" class="sec" id="fim">Encerrar e salvar</button></form>
<script>
const chat=document.getElementById('chat');let sessao=null;
function add(txt,classe){const d=document.createElement('div');d.className='msg '+classe;
d.textContent=txt;chat.appendChild(d);chat.scrollTop=chat.scrollHeight;}
async function post(url,dados){const r=await fetch(url,{method:'POST',
headers:{'Content-Type':'application/json'},body:JSON.stringify(dados)});return r.json();}
(async()=>{const d=await post('/api/iniciar',{});sessao=d.id_conversa;
document.getElementById('modo').textContent=d.modo+' - conversa '+d.id_conversa;
add(d.saudacao,'agente');})();
document.getElementById('f').onsubmit=async e=>{e.preventDefault();
const i=document.getElementById('txt'),b=document.getElementById('env');
const t=i.value.trim();if(!t)return;add(t,'cliente');i.value='';b.disabled=true;
try{const d=await post('/api/mensagem',{id_conversa:sessao,texto:t});
if(d.erro){add('erro: '+d.erro,'aviso');}else{add(d.texto,'agente');
if(d.handoff)add('encaminhar para a equipe - motivo: '+d.motivo_handoff,'aviso');}}
finally{b.disabled=false;i.focus();}};
document.getElementById('fim').onclick=async()=>{
const d=await post('/api/encerrar',{id_conversa:sessao});
add('Salvo. Lead '+d.temperatura+' (pontuacao '+d.pontuacao+') em '+d.arquivo,'aviso');};
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _json(self, dados: dict, status: int = 200) -> None:
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self) -> None:  # noqa: N802
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        corpo = PAGINA.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self) -> None:  # noqa: N802
        tamanho = int(self.headers.get("Content-Length", 0))
        dados = json.loads(self.rfile.read(tamanho) or b"{}")

        if self.path == "/api/iniciar":
            agente = AgenteElev.novo(CONFIG, canal="web-local")
            SESSOES[agente.id_conversa] = agente
            modo = "offline (sem IA)" if CONFIG.offline else CONFIG.modelo
            self._json({"id_conversa": agente.id_conversa, "saudacao": agente.saudacao(), "modo": modo})
            return

        agente = SESSOES.get(dados.get("id_conversa", ""))
        if agente is None:
            self._json({"erro": "sessao nao encontrada, recarregue a pagina"}, 404)
            return

        if self.path == "/api/mensagem":
            try:
                r = agente.responder(dados.get("texto", ""))
            except Exception as erro:
                self._json({"erro": f"{type(erro).__name__}: {erro}"})
                return
            self._json({"texto": r.texto, "handoff": r.handoff, "motivo_handoff": r.motivo_handoff})
            return

        if self.path == "/api/encerrar":
            reg = agente.registro(agente.extrair_lead())
            caminho = salvar_registro(reg, CONFIG.dir_dados)
            registrar_lead(reg, CONFIG.dir_dados)
            self._json({"temperatura": reg.temperatura, "pontuacao": reg.pontuacao, "arquivo": str(caminho)})
            return

        self.send_error(404)

    def log_message(self, *_):  # silencia o log de acesso
        pass


def main() -> int:
    global CONFIG
    parser = argparse.ArgumentParser(description="ELEV AI - interface local de teste")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--porta", type=int, default=8000)
    args = parser.parse_args()

    CONFIG = carregar_config(offline=True if args.offline else None)
    print(f"ELEV AI em http://localhost:{args.porta}  "
          f"({'offline' if CONFIG.offline else CONFIG.modelo}) - Ctrl+C para parar")
    try:
        ThreadingHTTPServer(("127.0.0.1", args.porta), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nencerrado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
