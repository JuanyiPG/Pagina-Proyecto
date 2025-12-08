document.addEventListener("DOMContentLoaded", () => {

  console.log("JS CARGADO"); // Para verificar

  const container = document.querySelector('.container-l');
  const btnSignIn = document.getElementById('btn-sign-in');
  const btnSignUp = document.getElementById('btn-sign-up');

  console.log(container, btnSignIn, btnSignUp); // Debug

  if (btnSignIn && btnSignUp && container) {
    btnSignIn.addEventListener('click', () => container.classList.remove('toggle'));
    btnSignUp.addEventListener('click', () => container.classList.add('toggle'));
  }

  const formSignIn = document.querySelector(".sign-in");
  if (!formSignIn) return;

  formSignIn.addEventListener("submit", (e) => {
    e.preventDefault();

    const email = formSignIn.querySelector("input[placeholder='Email']").value.trim();
    const password = formSignIn.querySelector("input[placeholder='Contraseña']").value.trim();

    // TEMPORAL para probar
    const users = [
      { email: "test@test.com", password: "1234", redirect: "/home" }
    ];

    const usuarioValido = users.find(u => u.email === email && u.password === password);

    if (usuarioValido) {
      window.location.href = usuarioValido.redirect;
    } else {
      alert("Usuario o contraseña incorrectos");
    }
  });

});
