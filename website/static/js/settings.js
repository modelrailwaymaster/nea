theme = localStorage.getItem("theme")

window.onload = function() {
if (theme === "true"){
    darkthemebutton.classList.add("is-active")
    lightthemebutton.classList.remove("is-active")
}}