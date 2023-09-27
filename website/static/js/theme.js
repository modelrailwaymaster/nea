let labels = document.getElementsByClassName("label")
labels = Array.prototype.slice.call( labels )
theme = localStorage.getItem("theme")
let lightthemebutton = document.getElementById("theme-toggle-light")
let darkthemebutton = document.getElementById("theme-toggle-dark")
let inputs = document.getElementsByTagName('input')
inputs = Array.prototype.slice.call(inputs)
let filter_background = document.getElementById("home-grid-filters")
let checkbox_label = document.getElementsByClassName("checkbox-label")
checkbox_label = Array.prototype.slice.call(checkbox_label)
console.log(checkbox_label)

const darkmode = () => {
    localStorage.setItem("theme","true")
    document.body.classList.add("dark")
    labels.forEach(element => {
        element.classList.add("dark")    
    })
    inputs.forEach(element => {
        element.classList.add("dark")
    })
    checkbox_label.forEach(element => {
        element.style.color = "rgb(250,0,0) !important"
    })
    $('input').addClass('darkinput');
    filter_background.style.backgroundColor = "rgb(50,50,50)"
}
    
const lightmode = () => {
    localStorage.setItem("theme","false")
    document.body.classList.remove("dark")
    labels.forEach(element => {
        element.classList.remove("dark")
    })
    inputs.forEach(element => {
        element.classList.remove("dark")
        element.classList.remove('dark-placeholder');
    })
    checkbox_label.forEach(element => {
        element.style.color = "rgb(0,250,0) !important"
    })
    $('input').removeClass('darkinput');
}

try{
lightthemebutton.addEventListener("click",function(){
    lightmode()
    lightthemebutton.classList.add("is-active")
    darkthemebutton.classList.remove("is-active")
})}
catch{}

try{
darkthemebutton.addEventListener("click",function(){
    darkmode()
    darkthemebutton.classList.add("is-active")
    lightthemebutton.classList.remove("is-active")
})}
catch{}

if (theme === "true"){
    darkmode()}