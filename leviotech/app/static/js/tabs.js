const tabButtons = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');

function loadImagesForPane(pane) {
  if (!pane) return;
  const lazyImages = pane.querySelectorAll('img[data-src]');
  lazyImages.forEach(img => {
    img.src = img.dataset.src;
    img.removeAttribute('data-src'); // prevent reloading
  });
}

// Ensure the initially active tab (e.g. tab1) loads its images if using data-src
const initialActivePane = document.querySelector('.tab-pane.active');
if (initialActivePane) {
  loadImagesForPane(initialActivePane);
}

tabButtons.forEach(button => {
  button.addEventListener('click', () => {
    const targetId = button.getAttribute('data-tab');
    const targetPane = document.getElementById(targetId);

    // Remove active classes
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabPanes.forEach(pane => pane.classList.remove('active'));

    // Add active to clicked tab and its content
    button.classList.add('active');
    if (targetPane) {
      targetPane.classList.add('active');

      // Lazy-load images for this pane on first activation
      loadImagesForPane(targetPane);
    }
  });
});
