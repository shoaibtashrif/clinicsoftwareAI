// Respect motion preferences; native video controls remain available to everyone.
(() => {
  const video = document.querySelector('[data-appointment-demo]');
  if (!video) return;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const update = () => {
    if (motion.matches) { video.pause(); video.autoplay = false; }
    else { video.autoplay = true; video.play().catch(() => {}); }
  };
  motion.addEventListener('change', update);
  update();
})();
