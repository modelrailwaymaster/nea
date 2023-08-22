const showpassword = document.getElementById("show-password")
const passwordfeild = document.querySelector("#password");

showpassword.addEventListener("click",function(){
    this.classList.toggle("fa-eye-slash");
    this.classList.toggle("fa-eye");
    const type = passwordfeild.getAttribute("type") === "password" ? "text" : "password";
    passwordfeild.setAttribute("type",type);
})