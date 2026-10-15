(() => {
  const watch = image => {
    if (image.dataset.csLoadingWatched) return;
    image.dataset.csLoadingWatched = 'true';
    const done = () => image.classList.remove('cs-image-pending');
    if (image.complete) { done(); return; }
    image.classList.add('cs-image-pending');
    image.addEventListener('load', done, { once: true });
    image.addEventListener('error', done, { once: true });
  };
  document.querySelectorAll('img').forEach(watch);
  new MutationObserver(records => records.forEach(record => record.addedNodes.forEach(node => {
    if (node.nodeType !== 1) return;
    if (node.matches('img')) watch(node);
    node.querySelectorAll('img').forEach(watch);
  }))).observe(document.body, { childList: true, subtree: true });
})();
