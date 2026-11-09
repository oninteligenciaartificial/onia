// Mejora opcional: los documentos también se leen e imprimen sin JavaScript.
document.querySelectorAll('[data-print]').forEach(button=>button.addEventListener('click',()=>window.print()));
document.querySelectorAll('[data-select]').forEach(button=>button.addEventListener('click',()=>{
  const field=document.getElementById(button.dataset.select);
  field.focus();field.select();
  document.getElementById('copy-status').textContent='Texto seleccionado. Copiá con Ctrl+C o ⌘C; en móvil, usá Copiar.';
}));
const slides=[...document.querySelectorAll('.slide')];
if(slides.length){
  let current=Math.max(0,slides.findIndex(s=>'#'+s.id===location.hash));
  function move(offset){current=Math.max(0,Math.min(slides.length-1,current+offset));location.hash=slides[current].id;}
  document.querySelector('[data-prev]').addEventListener('click',()=>move(-1));
  document.querySelector('[data-next]').addEventListener('click',()=>move(1));
  window.addEventListener('hashchange',()=>{current=Math.max(0,slides.findIndex(s=>'#'+s.id===location.hash));});
  document.addEventListener('keydown',event=>{
    if(event.target.closest('textarea,input,button,a')||event.altKey||event.ctrlKey||event.metaKey)return;
    if(['ArrowRight','PageDown','ArrowLeft','PageUp'].includes(event.key)){event.preventDefault();move(['ArrowRight','PageDown'].includes(event.key)?1:-1);}
  });
}
