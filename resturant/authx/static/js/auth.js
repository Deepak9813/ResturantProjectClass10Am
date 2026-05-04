
const passwordInput = document.getElementsByClassName("passwordHo");
const toggleEyes = document.querySelectorAll(".showHideEye");

toggleEyes.forEach((eye) => {
    eye.addEventListener("click", function () {
        const input = this.parentElement.querySelector(".passwordHo");

        if (input.type === "password") {
            input.type = "text";
            this.innerHTML = '<i class="fa-solid fa-eye"></i>';
        } else {
            input.type = "password";
            this.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
        }
    });
});



