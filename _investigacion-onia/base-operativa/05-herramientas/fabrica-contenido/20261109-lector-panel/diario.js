// Sólo reemplaza la bandeja del ciclo. Formularios, versiones y huellas quedan intactos.
(() => {
  const feed = document.getElementById('flujo-bandeja');
  if (!feed) return;
  const warning = document.getElementById('flujo-aviso');
  let busy = false;
  async function refresh() {
    if (busy || document.hidden) return;
    busy = true;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    try {
      const response = await fetch('/flujo', {cache: 'no-store', signal: controller.signal, credentials: 'same-origin'});
      if (!response.ok) throw new Error('projection unavailable');
      const body = await response.text();
      // HTML escapado generado por diario.fragment en el mismo servidor local.
      const template = document.createElement('template');
      template.innerHTML = body;
      feed.replaceChildren(template.content);
      warning.textContent = '';
    } catch (_) {
      warning.textContent = 'No se pudo actualizar el ciclo. Se conserva la última vista; revisar productor y conexión local.';
    } finally {
      clearTimeout(timeout);
      busy = false;
    }
  }
  setInterval(refresh, 15000);
})();
