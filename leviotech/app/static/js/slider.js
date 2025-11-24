// const slides = document.querySelectorAll('.slide');
// let current = 0;

// function showSlide(index) {
//   slides.forEach((slide, i) => {
//     slide.classList.remove('active');
//     if (i === index) {
//       slide.classList.add('active');
//     }
//   });
// }

// function nextSlide() {
//   current = (current + 1) % slides.length;
//   showSlide(current);
// }

// function prevSlide() {
//   current = (current - 1 + slides.length) % slides.length;
//   showSlide(current);
// }

// document.querySelector('.next').addEventListener('click', nextSlide);
// document.querySelector('.prev').addEventListener('click', prevSlide);

// // Auto-slide (optional)
// setInterval(nextSlide, 7000);

// window.addEventListener("load", () => {
//   document.querySelector(".slide").classList.add("active");
// });
window.addEventListener("load", function () {
  const wrapper = document.querySelector(".slider-wraper");
  const slides = document.querySelectorAll(".slide");
  const nextBtn = document.querySelector(".next");
  const prevBtn = document.querySelector(".prev");

  if (!wrapper || !slides.length) return;

  // Hide loader, un-blur slider
  wrapper.classList.remove("loading");
  wrapper.classList.add("loaded");

  let current = 0;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle("active", i === index);
    });
  }

  function nextSlide() {
    current = (current + 1) % slides.length;
    showSlide(current);
  }

  function prevSlide() {
    current = (current - 1 + slides.length) % slides.length;
    showSlide(current);
  }

  if (nextBtn) nextBtn.addEventListener("click", nextSlide);
  if (prevBtn) prevBtn.addEventListener("click", prevSlide);

  // Initial slide
  showSlide(0);

  // Auto-slide (optional)
  setInterval(nextSlide, 7000);
});
