const amzMsg = document.querySelector('.amz-msg');
const closeMsgBtn = document.querySelector('.close-msg-btn');
const slider = document.querySelector('.slider');
const mqmobile = window.matchMedia("(min-width: 320px) and (max-width: 525px)");
const mqdesktop = window.matchMedia("(min-width: 1024px)");
const headerTopBar = document.querySelector('.header-top-bar');
const trigger = document.querySelector(".nav-trigger");
const logoImg = document.querySelector('.logo-img');

closeMsgBtn.addEventListener('click',function(){
    amzMsg.style.display = 'none';
    applyMarginmobile(mqmobile);
    // apply margin desktop
    applyMargindesktop(mqdesktop);


});


function applyMarginmobile(e) {
  if (e.matches) {
    // Media query is active
    if(amzMsg.style.display == "none"){
      // Reset if outside media query (optional)
         slider.style.marginTop = "142px";
    }
    else{
        slider.style.marginTop = "172px";
    }
   
  } else {
    if(amzMsg.style.display == "none"){
      // Reset if outside media query (optional)
        slider.style.marginTop = "140px";
    }
    else{
        slider.style.marginTop = "170px";
    }
  
    
  }
}

function applyMargindesktop(e) {
  if (e.matches) {
    // Media query is active
    slider.style.marginTop = "140px";
  } 
  
}

// Run on window resize
mqmobile.addEventListener("change", applyMarginmobile);


// observer
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) {
        headerTopBar.style.height = "65px";
        logoImg.style.height = "43px";
        logoImg.style.width = "161px"
    


      } else {
         headerTopBar.style.height = "100px";
          logoImg.style.height = "60px";
          logoImg.style.width = "210px";
      }
    });
  },
  { threshold: 0 } // triggers as soon as element leaves the viewport
);

observer.observe(trigger);