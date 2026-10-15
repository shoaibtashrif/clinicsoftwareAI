/* ClinicSoftware.ai sales assistant embed. */
(() => {
  if (document.getElementById('clinicsoftware-assistant')) return;
  const installScript = document.currentScript;
  const base = new URL(installScript.src).origin;
  const host = document.createElement('div');
  host.id = 'clinicsoftware-assistant';
  const root = host.attachShadow({mode: 'open'});
  root.innerHTML = `<style>
    :host{all:initial}button{position:fixed;right:24px;bottom:24px;width:66px;height:66px;border:1px solid #ffffff26;border-radius:22px 22px 22px 7px;background:#0b0b0d;color:#fff;box-shadow:0 16px 42px #170e3038,0 5px 16px #0003;cursor:pointer;z-index:2147483000;display:grid;place-items:center;transition:.2s ease}button:hover{transform:translateY(-3px);box-shadow:0 20px 48px #170e3045,0 7px 20px #0004}button svg{width:39px;height:31px;display:block}iframe{position:fixed;right:24px;bottom:104px;width:410px;height:min(660px,calc(100dvh - 128px));border:1px solid #251b3830;border-radius:18px;box-shadow:0 28px 90px #1b102638;background:#fff;z-index:2147483001}iframe[hidden]{display:none}@media(max-width:600px){iframe{inset:0;width:100%;height:100dvh;border:0;border-radius:0}button{right:16px;bottom:16px}}
  </style><button type="button" aria-label="Chat with ClinicSoftware" aria-expanded="false"><svg viewBox="0 0 64 48" aria-hidden="true"><path fill="white" d="M32 2C15.4 2 2 11.7 2 23.7c0 7 4.6 13.3 11.7 17.2L9 47l12.2-3.1c3.4.9 7 1.4 10.8 1.4 16.6 0 30-9.7 30-21.6S48.6 2 32 2Z"/></svg></button>`;
  const button = root.querySelector('button');
  let frame;
  const toggle = open => {
    if (!frame) {
      frame = document.createElement('iframe');
      frame.title = 'ClinicSoftware website consultant';
      const url = new URL('/clinicsoftware/widget', base);
      url.searchParams.set('parent_origin', location.origin);
      frame.src = url;
      root.append(frame);
    }
    frame.hidden = !open;
    button.setAttribute('aria-expanded', String(open));
  };
  button.onclick = () => toggle(button.getAttribute('aria-expanded') !== 'true');
  window.addEventListener('message', event => {
    if (frame && event.source === frame.contentWindow && event.origin === base && event.data?.type === 'clinicsoftware:minimize') toggle(false);
  });
  document.body.append(host);
})();
