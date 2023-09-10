min = document.getElementsByName("min_price")[0]
max = document.getElementsByName("max_price")[0]

min.addEventListener("input", function(){
    max.setAttribute("min", this.value)
})