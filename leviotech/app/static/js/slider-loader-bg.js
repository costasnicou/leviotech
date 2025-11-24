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
