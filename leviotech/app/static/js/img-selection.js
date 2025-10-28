const productImgs = document.querySelectorAll('.product-image');
const featuredImg = document.querySelector('.featured-image');

productImgs.forEach(img =>{
    
    img.addEventListener('click', function(){

        const imgurl = img.getAttribute("src");
        featuredImg.src = imgurl;
    })


});