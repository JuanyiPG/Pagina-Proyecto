const container=document.querySelector('.container-l');
const btnSignIn=document.getElementById('btn-sign-in');
const btnSignUp=document.getElementById('btn-sign-up');

btnSignIn.addEventListener('click',()=>{
    container.classList.remove('toggle');
});

btnSignUp.addEventListener('click',()=>{
    container.classList.add('toggle');
});

document.addEventListener("DOMContentLoaded", () => {
  const formSignIn = document.querySelector(".sign-in");
  if (!formSignIn) return; 

  formSignIn.addEventListener("submit", (e) => {
    e.preventDefault();

    const email = formSignIn.querySelector("input[placeholder='Email']").value.trim();
    const password = formSignIn.querySelector("input[placeholder='Contraseña']").value.trim();

    
    const users = [
      { email: "luxyfashion@admin.com", password: "luxy123", redirect: "../PHP/index-admin.php" },
      { email: "yulieth@luxy.com", password: "yuli123", redirect: "../PAGINA_EMPLEADO/index-emple.php" },
      { email: "juanpintow@gmail.com", password: "juan12345", redirect: "../Cliente/index-cliente.html" }
    ];

    
    const usuarioValido = users.find(u => u.email === email && u.password === password);

    if (usuarioValido) {
      window.location.href = usuarioValido.redirect; 
    } else {
      alert("Usuario o contraseña incorrectos");
    }
  });
});

