const showpassword = document.getElementById("show-password")
const showpassword2 = document.getElementById("show-password2")
const passwordfeild = document.querySelector("#password1");
const passwordfeild2 = document.querySelector("#password2");

showpassword.addEventListener("click",function(){
    this.classList.toggle("fa-eye-slash");
    this.classList.toggle("fa-eye");
    const type = passwordfeild.getAttribute("type") === "password" ? "text" : "password";
    passwordfeild.setAttribute("type",type);
})

showpassword2.addEventListener("click",function(){
    this.classList.toggle("fa-eye-slash");
    this.classList.toggle("fa-eye");
    const type = passwordfeild2.getAttribute("type") === "password" ? "text" : "password";
    passwordfeild2.setAttribute("type",type);
})