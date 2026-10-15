(() => {
  const formMessage = 'Thanks. This local preview is ready to connect to the ClinicSoftware enquiry workflow.';
  const navbar = document.querySelector('.navbar');

  const updateNavbar = () => navbar?.classList.toggle('is-scrolled', window.scrollY > 24);
  updateNavbar();
  window.addEventListener('scroll', updateNavbar, {passive: true});

  // Own only the simplified Solutions dropdown; Webflow retains the page layout.
  const solutions = document.querySelector('.cs-solutions');
  const trigger = solutions?.querySelector('.cs-solutions-toggle');
  let closeTimer;
  const setOpen = open => {
    clearTimeout(closeTimer);
    if (!solutions) return;
    navbar.style.setProperty('--cs-menu-top', `${navbar.getBoundingClientRect().bottom}px`);
    solutions.classList.toggle('is-open', open);
    trigger.setAttribute('aria-expanded', String(open));
  };
  trigger?.addEventListener('click', () => setOpen(!solutions.classList.contains('is-open')));
  solutions?.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse' && matchMedia('(min-width:992px)').matches) setOpen(true);
  });
  solutions?.addEventListener('pointerleave', event => {
    if (event.pointerType === 'mouse') closeTimer = setTimeout(() => setOpen(false), 220);
  });
  solutions?.addEventListener('focusout', event => {
    if (!solutions.contains(event.relatedTarget)) setOpen(false);
  });
  document.addEventListener('click', event => {
    if (!solutions?.contains(event.target)) setOpen(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && solutions?.classList.contains('is-open')) {
      setOpen(false);
      trigger.focus();
    }
  });
  window.addEventListener('resize', () => setOpen(false));

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
