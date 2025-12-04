const button = document.querySelector("btnSearch");
const input = document.querySelector("searchInput");

button.addEventListener("click", (event) => {
    event.preventDefault()
    if(input.ariaValueMax.length < 3){
        alert("Debes de ingresar al menos 3 caracteres para la busqueda.")
        return false
    }
    const obj = {
        value: input.value,
        function: "search"
    }
    fetch("/PHP/PRODUCTOS/INDEX_PRODUCTOT.PHP",{
        method:"POST",
        body: JSON.stringify(obj)
    })
} )