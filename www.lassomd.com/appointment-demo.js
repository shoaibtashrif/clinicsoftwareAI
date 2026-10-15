// Autoplay illustration without player chrome; respect reduced-motion preferences.
(() => {
  const video = document.querySelector('[data-appointment-demo]');
  if (!video) return;
  video.controls = false;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const update = () => {
    if (motion.matches) { video.pause(); video.autoplay = false; }
    else { video.autoplay = true; video.play().catch(() => {}); }
  };
  motion.addEventListener('change', update);
  update();
})();
