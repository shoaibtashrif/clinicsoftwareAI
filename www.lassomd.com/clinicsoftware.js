(() => {
  const formMessage = 'Thanks. This local preview is ready to connect to the ClinicSoftware enquiry workflow.';
  const navbar = document.querySelector('.navbar');

  const updateNavbar = () => navbar?.classList.toggle('is-scrolled', window.scrollY > 24);
  updateNavbar();
  window.addEventListener('scroll', updateNavbar, {passive: true});

  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', event => {
      event.preventDefault();
      let status = form.querySelector('[data-clinicsoftware-status]');
      if (!status) {
        status = document.createElement('p');
        status.dataset.clinicsoftwareStatus = 'true';
        status.style.marginTop = '1rem';
        status.style.fontWeight = '700';
        form.append(status);
      }
      status.textContent = formMessage;
    });
  });

  let chatHost = document.documentElement.dataset.chatHost;
  if (chatHost?.includes('127.0.0.1') && !['127.0.0.1', 'localhost'].includes(location.hostname)) {
    chatHost = `${location.protocol}//${location.hostname}:8000`;
  }
  if (!chatHost || document.querySelector('script[data-clinicsoftware-chat]')) return;
  const script = document.createElement('script');
  script.src = `${chatHost.replace(/\/$/, '')}/static/clinicsoftware-embed.js?v=20261015-lavender`;
  script.defer = true;
  script.dataset.clinicsoftwareChat = 'true';
  document.body.append(script);
})();
