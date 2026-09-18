/* ==================================================================
   Comportamento compartilhado das demonstracoes da ELEV.
   Injeta a barra de identificacao e oferece helpers de modal.
   ================================================================== */
(function () {
  "use strict";

  const dados = document.currentScript ? document.currentScript.dataset : {};
  const nome = dados.demo || "Demonstração";

  document.addEventListener("DOMContentLoaded", function () {
    const barra = document.createElement("div");
    barra.className = "elev-barra";
    barra.innerHTML =
      '<span class="marca">ELEV</span>' +
      '<span class="rotulo">Projeto demonstrativo ELEV · ' + nome + "</span>" +
      '<a class="voltar" href="../index.html">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>' +
        "<span>Todas as demos</span></a>" +
      '<a class="voltar" href="../../index.html">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H6M11 6l-6 6 6 6"/></svg>' +
        "<span>Site da ELEV</span></a>";
    document.body.prepend(barra);
  });

  /* modal reaproveitado pelas demos que abrem conteudo ampliado */
  window.ElevModal = {
    abrir: function (id, html) {
      const m = document.getElementById(id);
      if (!m) return;
      if (html !== undefined) m.querySelector(".d-modal-caixa").innerHTML = html;
      m.dataset.aberto = "true";
      document.body.style.overflow = "hidden";
      const f = m.querySelector(".d-modal-fechar");
      if (f) f.focus();
    },
    fechar: function (id) {
      const m = document.getElementById(id);
      if (!m) return;
      m.dataset.aberto = "false";
      document.body.style.overflow = "";
    },
    ligar: function (id) {
      const m = document.getElementById(id);
      if (!m) return;
      m.addEventListener("click", function (e) {
        if (e.target === m || e.target.closest(".d-modal-fechar")) window.ElevModal.fechar(id);
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && m.dataset.aberto === "true") window.ElevModal.fechar(id);
      });
    }
  };

  /* formata moeda em pt-BR, usado pelo catalogo e pelo agendamento */
  window.elevMoeda = function (v) {
    return "R$ " + Number(v).toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  };
})();
