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

let elBurger = document.querySelector(".header__burger");
let elSidebar = document.querySelector(".sidebar");

elBurger.addEventListener("click", ()=>{
    elSidebar.classList.toggle("sidebar_active");
})