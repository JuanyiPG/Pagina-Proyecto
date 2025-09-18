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

  formSignIn.addEventListener("submit", (e) => {
    e.preventDefault(); 

    const email = formSignIn.querySelector("input[placeholder='Email']").value.trim();
    const password = formSignIn.querySelector("input[placeholder='Contraseña']").value.trim();

    const users = [
      { email: "juanpintow@gmail.com", password: "12345" },
      { email: "admin@correo.com", password: "admin" }
    ];

    const usuarioValido = users.find(u => u.email === email && u.password === password);

    if (usuarioValido) {
      window.location.href = "../Admin/index-admin.html"; 
    } else {
      alert("Usuario o contraseña incorrectos ");
    }
  });
});

