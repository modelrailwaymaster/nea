let labels = document.getElementsByClassName("label")
labels = Array.prototype.slice.call( labels )
theme = localStorage.getItem("theme")
let lightthemebutton = document.getElementById("theme-toggle-light")
let darkthemebutton = document.getElementById("theme-toggle-dark")
let inputs = document.getElementsByTagName('input')
inputs = Array.prototype.slice.call(inputs)

const darkmode = () => {
    localStorage.setItem("theme","true")
    document.body.classList.add("dark")
    labels.forEach(element => {
        element.classList.add("dark")    
    })
    inputs.forEach(element => {
        element.classList.add("dark")
    })
    $('input').addClass('darkinput');
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