const productImgs = document.querySelectorAll('.product-image');
const featuredImg = document.querySelector('.featured-image');

productImgs.forEach(img =>{
    
    img.addEventListener('mouseover', function(){

        const imgurl = img.getAttribute("src");
        featuredImg.src = imgurl;
    })


});