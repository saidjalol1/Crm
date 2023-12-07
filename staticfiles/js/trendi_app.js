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

let elDeliveryOne = document.querySelector(".delivery__type-one");
let elMoreOne = document.querySelector(".delivery__more-one");
let elDeliveryTwo = document.querySelector(".delivery__type-two");
let elMoreTwo = document.querySelector(".delivery__more-two");
let elDeliveryThree = document.querySelector(".delivery__type-three");
let elMoreThree = document.querySelector(".delivery__more-three");
let elDeliveryPlusOne = document.querySelector(".delivery__plus-one");
let elDeliveryPlusTwo = document.querySelector(".delivery__plus-two");
let elDeliveryPlusThree = document.querySelector(".delivery__plus-three");
let elDeliveryTopOne = document.querySelector(".delivery__top-one");
let elDeliveryTopTwo = document.querySelector(".delivery__top-two");
let elDeliveryTopThree = document.querySelector(".delivery__top-three");
let elDeliveryImage = document.querySelectorAll(".product__card--image");

elMoreOne.addEventListener("click", ()=>{
    elDeliveryOne.classList.toggle("delivery_active");
    elDeliveryPlusOne.classList.toggle("delivery-plus_active")
})
elMoreTwo.addEventListener("click", ()=>{
    elDeliveryTwo.classList.toggle("delivery_active");
    elDeliveryPlusTwo.classList.toggle("delivery-plus_active")
})
elMoreThree.addEventListener("click", ()=>{
    elDeliveryThree.classList.toggle("delivery_active");
    elDeliveryPlusThree.classList.toggle("delivery-plus_active")
})
elDeliveryTopOne.addEventListener("click", ()=>{
    elDeliveryOne.classList.toggle("delivery_active");
    elDeliveryPlusOne.classList.toggle("delivery-plus_active")
})
elDeliveryTopTwo.addEventListener("click", ()=>{
    elDeliveryTwo.classList.toggle("delivery_active");
    elDeliveryPlusTwo.classList.toggle("delivery-plus_active")
})
elDeliveryTopThree.addEventListener("click", ()=>{
    elDeliveryThree.classList.toggle("delivery_active");
    elDeliveryPlusThree.classList.toggle("delivery-plus_active")
})
elDeliveryImage.forEach(delivery_image => {
    delivery_image.addEventListener("mouseover", ()=>{
        delivery_image.setAttribute("src", "../images/download.jpg")
    })
    delivery_image.addEventListener("mouseout", ()=>{
        delivery_image.setAttribute("src", "../images/product-image-1.jpg")
    })
});