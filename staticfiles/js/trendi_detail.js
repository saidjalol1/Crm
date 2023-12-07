let elDeliveryImage = document.querySelectorAll(".also__card--image");
elDeliveryImage.forEach(delivery_image => {
    delivery_image.addEventListener("mouseover", ()=>{
        delivery_image.setAttribute("src", "../images/download.jpg")
    })
    delivery_image.addEventListener("mouseout", ()=>{
        delivery_image.setAttribute("src", "../images/product-image-1.jpg")
    })
});



let slideIndex = 1;
showSlides(slideIndex)

function plusSlides(n){
showSlides(slideIndex += n)
}
function currentSlide(n){
showSlides(slideIndex = n)
}
function showSlides(n){
    let slides = document.getElementsByClassName("hero__slide");
    let dots = document.getElementsByClassName("dot");
    if(n > slides.length){
    slideIndex = 1
    }
    if(n < 1){ 
        slideIndex=slides.length 
    }
    for(let i=0; i < slides.length; i++){
        slides[i].style.display="none" 
    }
    for(i=0; i < dots.length; i++){
        dots[i].className=dots[i].className.replace(" active", "" ) 
    }
    slides[slideIndex-1].style.display="flex";
    dots[slideIndex-1].className +=" active"
}