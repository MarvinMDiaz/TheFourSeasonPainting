function initBeforeAfterSlider(container) {
  const afterWrap = container.querySelector('.ba-after-wrap');
  const handle = container.querySelector('.ba-handle');
  if (!afterWrap || !handle) return;

  let isDragging = false;
  let rafId = null;

  const setPosition = (pct) => {
    const position = Math.max(2, Math.min(98, pct));
    afterWrap.style.clipPath = `inset(0 ${100 - position}% 0 0)`;
    handle.style.left = `${position}%`;
  };

  const getPositionFromEvent = (e) => {
    const rect = container.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    return ((clientX - rect.left) / rect.width) * 100;
  };

  const onMove = (e) => {
    if (!isDragging) return;
    e.preventDefault();
    if (rafId) cancelAnimationFrame(rafId);
    rafId = requestAnimationFrame(() => setPosition(getPositionFromEvent(e)));
  };

  const onEnd = () => {
    isDragging = false;
    container.style.cursor = 'col-resize';
    document.removeEventListener('mousemove', onMove);
    document.removeEventListener('mouseup', onEnd);
    document.removeEventListener('touchmove', onMove);
    document.removeEventListener('touchend', onEnd);
  };

  const onStart = (e) => {
    isDragging = true;
    container.style.cursor = 'grabbing';
    setPosition(getPositionFromEvent(e));
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onEnd);
    document.addEventListener('touchmove', onMove, { passive: false });
    document.addEventListener('touchend', onEnd);
  };

  container.addEventListener('mousedown', onStart);
  container.addEventListener('touchstart', onStart, { passive: true });

  setPosition(50);
}
