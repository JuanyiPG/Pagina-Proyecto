

        fetch("items/headeradmin.html")
             .then(res => res.text())
             .then(data => {
               document.getElementById("header").innerHTML = data;

      const toggleBtn = document.getElementById("formToggle");
      const submenu = document.getElementById("submenuForm");

      toggleBtn.addEventListener("click", function(e) {
        e.preventDefault();
        submenu.classList.toggle("show");
      });
    });
