document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");

    if (!loginForm) return;

    loginForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const identifier = document.getElementById("identifier").value;
        const password = document.getElementById("password").value;

        try {

            const response = await fetch("/api/auth/login/", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                },

                credentials: "include",

                body: JSON.stringify({
                    identifier,
                    password
                })
            });

            const data = await response.json();

            if (response.ok) {

                localStorage.setItem(
                    "access_token",
                    data.access_token
                );

                alert("Login Successful");

                window.location.href = "/";
                // localStorage.setItem("isLoggedIn", "true");

            } else {

                alert(data.error);

            }

        } catch (error) {

            console.error(error);

            alert("Something went wrong.");

        }

    });

});