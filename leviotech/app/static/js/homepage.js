
// slider loader bg
document.addEventListener("DOMContentLoaded", function () {
    const wrapper = document.querySelector(".slider-wraper");
    if (!wrapper) return;

    const slides = wrapper.querySelectorAll(".slider .slide");
    if (!slides.length) {
        wrapper.classList.remove("loading");
        wrapper.classList.add("loaded");
        return;
    }

    // Extract background-image URLs from each slide
    const urls = [];
    slides.forEach(slide => {
        const style = window.getComputedStyle(slide);
        const bg = style.backgroundImage; // e.g. url("https://.../slide1.jpg")

        if (bg && bg !== "none") {
            const match = bg.match(/url\(["']?(.*?)["']?\)/);
            if (match && match[1]) {
                urls.push(match[1]);
            }
        }
    });

    if (!urls.length) {
        wrapper.classList.remove("loading");
        wrapper.classList.add("loaded");
        return;
    }

    let loadedCount = 0;

    function imageDone() {
        loadedCount++;
        if (loadedCount >= urls.length) {
            wrapper.classList.remove("loading");
            wrapper.classList.add("loaded");

            // Optional: init your slider only after images are ready
            if (typeof window.initSlider === "function") {
                window.initSlider();
            }
        }
    }

    // Preload each background image
    urls.forEach(src => {
        const img = new Image();
        img.onload = imageDone;
        img.onerror = imageDone; // don't hang if one fails
        img.src = src;
    });
});

// slider js
window.addEventListener("load", function () {
  const wrapper = document.querySelector(".slider-wraper");
  const slides = document.querySelectorAll(".slide");
  const nextBtn = document.querySelector(".next");
  const prevBtn = document.querySelector(".prev");

  if (!slides.length) return;

  // Mobile = 320px–525px viewport width
  const mqmobile = window.matchMedia("(min-width: 320px) and (max-width: 525px)");
  const isMobile = mqmobile.matches;

  if (wrapper) {
    wrapper.classList.remove("loading");
    wrapper.classList.add("loaded");
  }

  let current = 0;

  function getSlideBgUrl(slide) {
    if (!slide) return null;

    const desktop = slide.dataset.bg;      // from data-bg="..."
    const mobile  = slide.dataset.bgMob;   // from data-bg-mob="..."

    if (isMobile && mobile) {
      return mobile;
    }
    // On desktop (or if no mobile version), use desktop
    return desktop || mobile || null;
  }

  function loadSlideBackground(index, callback) {
    const slide = slides[index];
    if (!slide) {
      if (callback) callback();
      return;
    }

    // already loaded?
    if (slide.dataset.bgLoaded === "true") {
      if (callback) callback();
      return;
    }

    const url = getSlideBgUrl(slide);
    if (!url) {
      slide.dataset.bgLoaded = "true";
      if (callback) callback();
      return;
    }

    const img = new Image();
    img.onload = function () {
      slide.style.backgroundImage = `url("${url}")`;
      slide.dataset.bgLoaded = "true";
      if (callback) callback();
    };
    img.onerror = function () {
      slide.dataset.bgLoaded = "true";
      if (callback) callback();
    };
    img.src = url;
  }

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle("active", i === index);
    });
  }

  function goToSlide(index) {
    loadSlideBackground(index, function () {
      current = index;
      showSlide(current);

      // Preload next slide quietly for smoother transitions
      const nextIndex = (current + 1) % slides.length;
      loadSlideBackground(nextIndex);
    });
  }

  function nextSlide() {
    goToSlide((current + 1) % slides.length);
  }

  function prevSlide() {
    goToSlide((current - 1 + slides.length) % slides.length);
  }

  if (nextBtn) nextBtn.addEventListener("click", nextSlide);
  if (prevBtn) prevBtn.addEventListener("click", prevSlide);

  // Initial slide
  goToSlide(0);

  // Auto-slide
  setInterval(nextSlide, 7000);
});



// end slider js

// tabs js
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

