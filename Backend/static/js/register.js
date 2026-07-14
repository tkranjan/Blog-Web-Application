document.addEventListener("DOMContentLoaded", () => {

    const registerForm = document.getElementById("registerForm");

    if (!registerForm) return;

    registerForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const first_name = document.getElementById("first_name").value;
        const last_name = document.getElementById("last_name").value;
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const confirm_password = document.getElementById("confirm_password").value;

        if (password !== confirm_password) {
            alert("Passwords do not match.");
            return;
        }

        try {

            const response = await fetch("/api/auth/register/", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    first_name,
                    last_name,
                    username,
                    email,
                    password
                })

            });

            const data = await response.json();

            if (response.ok) {

                alert("Registration Successful");

                window.location.href = "/login/";

            }

            else {

                alert(JSON.stringify(data));

            }

        }

        catch(error){

            console.error(error);

            alert("Something went wrong.");

        }

    });

});