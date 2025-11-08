const amzMsg = document.querySelector('.amz-msg');
const closeMsgBtn = document.querySelector('.close-msg-btn');
const slider = document.querySelector('.slider');
const mq = window.matchMedia("(min-width: 320px) and (max-width: 525px)");
closeMsgBtn.addEventListener('click',function(){
    amzMsg.style.display = 'none';
    applyMargin(mq);
    // slider.style.marginTop = "173px";


});


function applyMargin(e) {
  if (e.matches) {
    // Media query is active
    slider.style.marginTop = "142px";
  } else {
    // Reset if outside media query (optional)
    slider.style.marginTop = "140px";
  }
}

// Run on window resize
mq.addEventListener("change", applyMargin);