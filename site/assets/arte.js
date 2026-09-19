/* ==================================================================
   Biblioteca de ilustracoes das demonstracoes da ELEV.

   Por que existe: as demos precisam de imagem, e o ambiente nao pode
   distribuir foto de banco nem de busca (direito autoral). Entao cada
   item ganha uma ilustracao propria em SVG, desenhada aqui.

   Foto de verdade depois: qualquer slot aceita `data-foto="caminho"`.
   Se o arquivo existir, a foto entra no lugar da ilustracao sozinha
   (ver ElevArte.plugarFotos). Nada mais precisa mudar.
   ================================================================== */
(function () {
  "use strict";

  const svg = function (conteudo, vb) {
    return '<svg viewBox="' + (vb || "0 0 120 120") + '" preserveAspectRatio="xMidYMid slice" ' +
           'xmlns="http://www.w3.org/2000/svg" class="arte-svg" aria-hidden="true">' + conteudo + "</svg>";
  };

  /* fundo com luz difusa: da profundidade sem parecer bloco chapado */
  const fundo = function (c1, c2, id) {
    return '<defs><radialGradient id="f' + id + '" cx="32%" cy="24%" r="85%">' +
             '<stop offset="0" stop-color="' + c1 + '"/><stop offset="1" stop-color="' + c2 + '"/>' +
           "</radialGradient></defs>" +
           '<rect width="120" height="120" fill="url(#f' + id + ')"/>';
  };
  const sombra = function (cx, cy, rx) {
    return '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + rx + '" ry="' + (rx * 0.22) +
           '" fill="rgba(0,0,0,.28)"/>';
  };

  let n = 0;
  const id = function () { return ++n; };

  const ARTES = {
    /* ---------------- cafeteria ---------------- */
    cafe: function () {
      const i = id();
      return svg(fundo("#5A3A22", "#1C1109", i) + sombra(60, 92, 30) +
        '<path d="M34 46h44v20a22 22 0 0 1-44 0z" fill="#F3E4D2"/>' +
        '<path d="M34 46h44v6a22 22 0 0 1-44 0z" fill="#fff" opacity=".55"/>' +
        '<ellipse cx="56" cy="46" rx="22" ry="7" fill="#6B4327"/>' +
        '<ellipse cx="56" cy="45" rx="17" ry="5" fill="#8B5A33"/>' +
        '<path d="M78 50h6a9 9 0 0 1 0 18h-3" stroke="#F3E4D2" stroke-width="5" fill="none" stroke-linecap="round"/>' +
        '<ellipse cx="60" cy="92" rx="34" ry="7" fill="#F3E4D2" opacity=".18"/>' +
        '<path d="M48 26c-4 5 4 8 0 13M60 22c-5 6 5 9 0 15M72 27c-4 5 4 8 0 12" ' +
          'stroke="rgba(255,255,255,.45)" stroke-width="2.4" fill="none" stroke-linecap="round"/>');
    },
    paoNaPedra: function () {
      const i = id();
      return svg(fundo("#8A5A2E", "#241408", i) + sombra(60, 88, 34) +
        '<ellipse cx="60" cy="66" rx="40" ry="24" fill="#C98A4B"/>' +
        '<ellipse cx="60" cy="62" rx="38" ry="22" fill="#E0A863"/>' +
        '<path d="M32 58c10-7 46-7 56 0" stroke="#8A5A2E" stroke-width="3" fill="none" stroke-linecap="round"/>' +
        '<path d="M38 68c12-6 32-6 44 0" stroke="#A96F38" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".8"/>' +
        '<ellipse cx="46" cy="58" rx="3" ry="2" fill="#F5CF9A" opacity=".8"/>' +
        '<ellipse cx="72" cy="61" rx="4" ry="2.4" fill="#F5CF9A" opacity=".7"/>');
    },
    graos: function () {
      const i = id();
      let g = fundo("#7A4A26", "#1A0F07", i);
      const pos = [[38,44,14],[64,38,12],[86,52,13],[50,66,13],[76,74,12],[34,80,11],[60,54,10]];
      pos.forEach(function (p) {
        g += '<g transform="translate(' + p[0] + ',' + p[1] + ') rotate(' + (p[0] % 40) + ')">' +
             '<ellipse rx="' + p[2] + '" ry="' + (p[2] * 0.72) + '" fill="#4A2A15"/>' +
             '<ellipse rx="' + (p[2] - 2) + '" ry="' + (p[2] * 0.62) + '" fill="#6B3D1F"/>' +
             '<path d="M0 ' + (-p[2] * 0.6) + ' Q 3 0 0 ' + (p[2] * 0.6) + '" stroke="#2E1A0D" stroke-width="2.2" fill="none"/>' +
             "</g>";
      });
      return svg(g);
    },
    coador: function () {
      const i = id();
      return svg(fundo("#4E6B4A", "#14200F", i) + sombra(60, 94, 26) +
        '<path d="M40 40h40l-8 30H48z" fill="#E8DCC8"/>' +
        '<path d="M40 40h40l-3 11H43z" fill="#fff" opacity=".5"/>' +
        '<rect x="44" y="72" width="32" height="20" rx="4" fill="#D9C8AE"/>' +
        '<path d="M60 52v16" stroke="#6B4327" stroke-width="3" stroke-linecap="round"/>' +
        '<ellipse cx="60" cy="72" rx="15" ry="4" fill="#6B4327" opacity=".7"/>');
    },
    mesaCafe: function () {
      const i = id();
      return svg(fundo("#3B2A1C", "#120B06", i) +
        '<rect x="14" y="52" width="92" height="46" rx="6" fill="#6B4A2E"/>' +
        '<rect x="14" y="52" width="92" height="8" rx="4" fill="#8A6038"/>' +
        '<circle cx="42" cy="74" r="12" fill="#F3E4D2"/><circle cx="42" cy="74" r="8" fill="#6B4327"/>' +
        '<rect x="66" y="64" width="26" height="20" rx="3" fill="#E8DCC8"/>' +
        '<path d="M70 70h18M70 76h12" stroke="#B99E7E" stroke-width="2" stroke-linecap="round"/>' +
        '<rect x="20" y="22" width="18" height="26" rx="9" fill="#4E6B4A"/>' +
        '<path d="M29 22v-8" stroke="#3A5238" stroke-width="3"/>');
    },
    equipe: function () {
      const i = id();
      return svg(fundo("#4A3020", "#150C06", i) +
        '<circle cx="42" cy="48" r="14" fill="#C98A4B"/><path d="M22 92a20 20 0 0 1 40 0z" fill="#E0A863"/>' +
        '<circle cx="78" cy="52" r="12" fill="#A96F38"/><path d="M60 92a18 18 0 0 1 36 0z" fill="#C98A4B"/>');
    },

    /* ---------------- plantas ---------------- */
    folhagem: function (c) {
      const i = id(), base = c || "#3F7A44";
      return svg(fundo("#2A4A2C", "#0C1610", i) + sombra(60, 100, 22) +
        '<path d="M52 100V56" stroke="#2F5A33" stroke-width="4" stroke-linecap="round"/>' +
        '<path d="M52 62c-16-4-24-16-22-30 14-2 26 8 28 22z" fill="' + base + '"/>' +
        '<path d="M52 50c12-8 16-22 10-34-13 4-20 16-18 28z" fill="' + base + '" opacity=".82"/>' +
        '<path d="M54 72c14 2 24-6 26-18-12-4-24 2-28 12z" fill="' + base + '" opacity=".92"/>' +
        '<path d="M46 84c-12 0-20-8-20-18 11-2 20 4 22 12z" fill="' + base + '" opacity=".75"/>' +
        '<path d="M40 100h30l-3 14a4 4 0 0 1-4 3H47a4 4 0 0 1-4-3z" fill="#B0764E"/>');
    },
    espada: function () {
      const i = id();
      return svg(fundo("#27462C", "#0B140D", i) + sombra(60, 100, 20) +
        '<path d="M60 100V22" stroke="#3F7A44" stroke-width="11" stroke-linecap="round"/>' +
        '<path d="M60 100V22" stroke="#5B9E5F" stroke-width="4" stroke-linecap="round" opacity=".6"/>' +
        '<path d="M46 100c-4-22-2-42 4-56" stroke="#356A3A" stroke-width="9" stroke-linecap="round" fill="none"/>' +
        '<path d="M76 100c5-20 3-38-3-50" stroke="#47874B" stroke-width="8" stroke-linecap="round" fill="none"/>' +
        '<path d="M40 100h40l-3 14a4 4 0 0 1-4 3H47a4 4 0 0 1-4-3z" fill="#9C6B46"/>');
    },
    pendente: function () {
      const i = id();
      let g = fundo("#2E5233", "#0B140D", i);
      g += '<path d="M36 22h48l-5 20H41z" fill="#B0764E"/>';
      [[46, "#4E8F52"],[60, "#3F7A44"],[74, "#5FA463"]].forEach(function (p) {
        g += '<path d="M' + p[0] + ' 42c-6 18 4 34 0 52" stroke="' + p[1] + '" stroke-width="3" fill="none"/>';
        for (let k = 0; k < 6; k++) {
          g += '<circle cx="' + (p[0] + (k % 2 ? 5 : -5)) + '" cy="' + (52 + k * 10) + '" r="4.4" fill="' + p[1] + '"/>';
        }
      });
      return svg(g);
    },
    cacto: function () {
      const i = id();
      return svg(fundo("#4E5B2E", "#161A0B", i) + sombra(60, 100, 20) +
        '<rect x="50" y="34" width="20" height="66" rx="10" fill="#5E8A45"/>' +
        '<path d="M50 58H38a8 8 0 0 0-8 8v10" stroke="#5E8A45" stroke-width="13" fill="none" stroke-linecap="round"/>' +
        '<path d="M70 50h10a8 8 0 0 1 8 8v14" stroke="#4E7A38" stroke-width="12" fill="none" stroke-linecap="round"/>' +
        '<path d="M56 40v52M64 44v48" stroke="#7BA85E" stroke-width="1.6" opacity=".7"/>' +
        '<circle cx="60" cy="30" r="5" fill="#E8A0B0"/>' +
        '<path d="M40 100h40l-3 14a4 4 0 0 1-4 3H47a4 4 0 0 1-4-3z" fill="#A9784F"/>');
    },
    suculenta: function () {
      const i = id();
      let g = fundo("#55663A", "#171B0E", i) + sombra(60, 96, 24);
      for (let k = 0; k < 8; k++) {
        const a = (k * 45) * Math.PI / 180;
        g += '<ellipse cx="' + (60 + Math.cos(a) * 18) + '" cy="' + (62 + Math.sin(a) * 13) +
             '" rx="13" ry="9" fill="#7C9B5A" transform="rotate(' + (k * 45) + ' 60 62)" opacity=".92"/>';
      }
      g += '<circle cx="60" cy="62" r="9" fill="#A3C07E"/>' +
           '<path d="M40 96h40l-3 14a4 4 0 0 1-4 3H47a4 4 0 0 1-4-3z" fill="#B58455"/>';
      return svg(g);
    },
    vaso: function (cor, aro) {
      const i = id();
      return svg(fundo("#4A4034", "#14100B", i) + sombra(60, 100, 26) +
        '<path d="M34 40h52l-8 60a6 6 0 0 1-6 5H48a6 6 0 0 1-6-5z" fill="' + (cor || "#B99A74") + '"/>' +
        '<path d="M34 40h52l-2 12H36z" fill="' + (aro || "#D4B489") + '"/>' +
        '<path d="M46 56c-2 20-2 32 0 44" stroke="rgba(255,255,255,.25)" stroke-width="3" fill="none"/>');
    },

    /* ---------------- beleza ---------------- */
    tesoura: function () {
      const i = id();
      return svg(fundo("#5A3540", "#170C10", i) +
        '<circle cx="42" cy="86" r="11" stroke="#E8CBD0" stroke-width="5" fill="none"/>' +
        '<circle cx="76" cy="86" r="11" stroke="#E8CBD0" stroke-width="5" fill="none"/>' +
        '<path d="M46 78L82 28M72 78L36 28" stroke="#E8CBD0" stroke-width="5" stroke-linecap="round"/>' +
        '<circle cx="59" cy="56" r="4" fill="#B76E79"/>');
    },
    secador: function () {
      const i = id();
      return svg(fundo("#523344", "#150B11", i) +
        '<rect x="28" y="40" width="46" height="30" rx="15" fill="#E8CBD0"/>' +
        '<rect x="70" y="46" width="18" height="18" rx="5" fill="#D9A8B2"/>' +
        '<path d="M44 70l-6 26" stroke="#E8CBD0" stroke-width="11" stroke-linecap="round"/>' +
        '<path d="M92 44c6 4 6 14 0 18M98 38c10 6 10 26 0 32" stroke="rgba(255,255,255,.4)" stroke-width="3" fill="none" stroke-linecap="round"/>');
    },
    corTintura: function () {
      const i = id();
      return svg(fundo("#4A2E3C", "#140A0F", i) +
        '<path d="M40 30h40v22a20 20 0 0 1-40 0z" fill="#D9A8B2"/>' +
        '<path d="M44 58c2 16 2 28 0 40h32c-2-12-2-24 0-40z" fill="#E8CBD0"/>' +
        '<circle cx="60" cy="74" r="10" fill="#B76E79"/>' +
        '<circle cx="46" cy="40" r="4" fill="#fff" opacity=".5"/>');
    },
    escova: function () {
      const i = id();
      return svg(fundo("#4E3040", "#150B11", i) +
        '<rect x="52" y="26" width="16" height="50" rx="8" fill="#D9A8B2"/>' +
        '<rect x="56" y="74" width="8" height="26" rx="4" fill="#E8CBD0"/>' +
        '<path d="M52 36h-8M52 46h-8M52 56h-8M68 36h8M68 46h8M68 56h8" stroke="#E8CBD0" stroke-width="3" stroke-linecap="round"/>');
    },

    /* ---------------- construcao ---------------- */
    obra: function () {
      const i = id();
      return svg(fundo("#1E4A45", "#07100F", i) +
        '<path d="M18 96V52l26-18 26 18v44z" fill="#14A08A" opacity=".85"/>' +
        '<path d="M70 96V62l22-14 22 14v34z" fill="#0E7A69" opacity=".9"/>' +
        '<rect x="34" y="66" width="10" height="10" fill="#04120F" opacity=".5"/>' +
        '<rect x="50" y="66" width="10" height="10" fill="#04120F" opacity=".5"/>' +
        '<rect x="38" y="82" width="14" height="14" fill="#04120F" opacity=".6"/>' +
        '<rect x="82" y="74" width="9" height="9" fill="#04120F" opacity=".5"/>' +
        '<rect x="96" y="74" width="9" height="9" fill="#04120F" opacity=".5"/>' +
        '<path d="M8 96h108" stroke="#4ECDB0" stroke-width="3" stroke-linecap="round"/>');
    },
    planta2d: function () {
      const i = id();
      return svg(fundo("#123B38", "#060E0D", i) +
        '<rect x="22" y="24" width="76" height="72" rx="3" stroke="#4ECDB0" stroke-width="2.4" fill="none"/>' +
        '<path d="M22 60h34M56 24v72M56 60h42" stroke="#4ECDB0" stroke-width="2" opacity=".85"/>' +
        '<path d="M34 60v-8M42 24v10" stroke="#0A1A19" stroke-width="4"/>' +
        '<circle cx="78" cy="42" r="7" stroke="#4ECDB0" stroke-width="1.8" fill="none" opacity=".7"/>' +
        '<path d="M64 78h12v12H64z" stroke="#4ECDB0" stroke-width="1.8" fill="none" opacity=".7"/>');
    },
    reforma: function () {
      const i = id();
      return svg(fundo("#1A443F", "#06100E", i) +
        '<path d="M26 92V50h34v42z" fill="#0E7A69"/>' +
        '<path d="M60 92V36h36v56z" fill="#14A08A" opacity=".9"/>' +
        '<path d="M70 20l14 14-10 10-14-14z" fill="#4ECDB0"/>' +
        '<path d="M60 30L36 54" stroke="#4ECDB0" stroke-width="5" stroke-linecap="round"/>' +
        '<path d="M14 92h96" stroke="#4ECDB0" stroke-width="3" stroke-linecap="round"/>');
    },

    /* ---------------- viagem (marca Nomade, demo de design) ---------------- */
    serra: function (cor) {
      const i = id();
      return svg(fundo(cor || "#2E4A3F", "#0B1310", i) +
        '<circle cx="86" cy="30" r="13" fill="#F7A072" opacity=".9"/>' +
        '<path d="M0 96l30-40 18 22 16-26 26 44z" fill="#14231D"/>' +
        '<path d="M18 96l30-40 22 28 20-18 30 30z" fill="#1E3A30"/>' +
        '<path d="M48 56l10 13-5 4-6-8z" fill="#E8DFD2" opacity=".85"/>' +
        '<path d="M0 96h120v24H0z" fill="#0B1310"/>' +
        '<path d="M0 100c24-6 44 6 64 0s38-8 56-2" stroke="rgba(232,223,210,.22)" stroke-width="2.4" fill="none"/>');
    },
    estrada: function (cor) {
      const i = id();
      return svg(fundo(cor || "#E2542C", "#3A1206", i) +
        '<path d="M0 120L44 46h32l44 74z" fill="#231610"/>' +
        '<path d="M52 46h16l26 74H26z" fill="#33231A"/>' +
        '<path d="M60 52v10M60 70v12M60 90v14M60 112v8" stroke="#F7E4CE" stroke-width="3.4" stroke-linecap="round" opacity=".85"/>' +
        '<circle cx="30" cy="26" r="9" fill="#F7A072" opacity=".8"/>' +
        '<path d="M0 46c18-8 34 4 52 0s40-10 68-2" stroke="rgba(247,160,114,.4)" stroke-width="3" fill="none"/>');
    },
    barraca: function (cor) {
      const i = id();
      return svg(fundo(cor || "#1B2B33", "#080E12", i) + sombra(60, 92, 32) +
        '<path d="M60 34l34 54H26z" fill="#E2542C"/>' +
        '<path d="M60 34l16 54H44z" fill="#0E0E0F" opacity=".55"/>' +
        '<path d="M60 34v54" stroke="#F7A072" stroke-width="2" opacity=".6"/>' +
        '<path d="M22 88h76" stroke="#E8DFD2" stroke-width="3" stroke-linecap="round" opacity=".5"/>' +
        '<circle cx="26" cy="24" r="2.2" fill="#E8DFD2"/><circle cx="46" cy="16" r="1.6" fill="#E8DFD2"/>' +
        '<circle cx="92" cy="22" r="2.6" fill="#E8DFD2"/><circle cx="74" cy="12" r="1.5" fill="#E8DFD2"/>');
    },
    mapa: function (cor) {
      const i = id();
      return svg(fundo(cor || "#E8DFD2", "#B8A98F", i) +
        '<path d="M14 20l30 10 32-10 30 10v72l-30-10-32 10-30-10z" fill="#F3ECE0" stroke="#C4B39A" stroke-width="2"/>' +
        '<path d="M44 30v72M76 20v72" stroke="#C4B39A" stroke-width="1.8"/>' +
        '<path d="M20 64c14-14 26 10 40-4s26 6 42-10" stroke="#E2542C" stroke-width="3" fill="none" stroke-dasharray="6 5" stroke-linecap="round"/>' +
        '<circle cx="24" cy="62" r="5" fill="#2E4A3F"/>' +
        '<path d="M100 48a7 7 0 1 0-14 0c0 5 7 12 7 12s7-7 7-12z" fill="#E2542C"/>' +
        '<circle cx="93" cy="48" r="2.6" fill="#F3ECE0"/>');
    },
    bussola: function (cor) {
      const i = id();
      return svg(fundo(cor || "#0E0E0F", "#2E4A3F", i) +
        '<circle cx="60" cy="60" r="38" fill="#171A19" stroke="#E8DFD2" stroke-width="3"/>' +
        '<circle cx="60" cy="60" r="30" fill="none" stroke="rgba(232,223,210,.3)" stroke-width="1.6"/>' +
        '<path d="M60 22v7M60 91v7M22 60h7M91 60h7" stroke="#E8DFD2" stroke-width="2.6" stroke-linecap="round"/>' +
        '<path d="M60 34l9 22-9 30-9-30z" fill="#E2542C"/>' +
        '<path d="M60 86l9-30-9-22-9 22z" fill="#E8DFD2" opacity=".5"/>' +
        '<circle cx="60" cy="60" r="4" fill="#F7A072"/>');
    },
    mochila: function (cor) {
      const i = id();
      return svg(fundo(cor || "#7A2411", "#170805", i) + sombra(60, 96, 26) +
        '<path d="M42 32a18 18 0 0 1 36 0v6H42z" fill="none" stroke="#C9B79E" stroke-width="5"/>' +
        '<rect x="32" y="36" width="56" height="58" rx="15" fill="#2E4A3F"/>' +
        '<rect x="32" y="36" width="56" height="20" rx="13" fill="#3B5E50"/>' +
        '<rect x="44" y="62" width="32" height="22" rx="7" fill="#1F352C"/>' +
        '<path d="M44 72h32" stroke="#E2542C" stroke-width="3" stroke-linecap="round"/>' +
        '<circle cx="60" cy="50" r="4" fill="#F7A072"/>');
    },
  };

  /* Slot de imagem: usa a ilustracao e troca por foto se o arquivo existir. */
  function plugarFotos(raiz) {
    (raiz || document).querySelectorAll("[data-foto]").forEach(function (slot) {
      const caminho = slot.getAttribute("data-foto");
      if (!caminho) return;
      const teste = new Image();
      teste.onload = function () {
        const img = document.createElement("img");
        img.src = caminho;
        img.alt = slot.getAttribute("data-alt") || "";
        img.className = "arte-foto";
        slot.innerHTML = "";
        slot.appendChild(img);
      };
      teste.src = caminho;
    });
  }

  window.ElevArte = {
    desenhar: function (nome, arg) {
      const f = ARTES[nome];
      return f ? f(arg) : "";
    },
    lista: Object.keys(ARTES),
    plugarFotos: plugarFotos
  };
})();
