let labels = document.getElementsByClassName("label")
labels = Array.prototype.slice.call( labels )
theme = localStorage.getItem("theme")
const lightthemebutton = document.getElementById("theme-toggle-light")
const darkthemebutton = document.getElementById("theme-toggle-dark")

const darkmode = () => {
    localStorage.setItem("theme","true")
    document.body.classList.add("dark")
    labels.forEach(element => {
        element.classList.add("dark")    
    })
}
    
const lightmode = () => {
    localStorage.setItem("theme","false")
    document.body.classList.remove("dark")
    labels.forEach(element => {
        element.classList.remove("dark")
    })
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