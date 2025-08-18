// photoapp/static/photoapp/js/jwt_register.js

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("jwtRegisterForm");
  const errorBox = document.getElementById("registerErrorBox");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    errorBox.classList.add("d-none");

    const username = document.getElementById("jwt_username").value.trim();
    const email = document.getElementById("jwt_email").value.trim();
    const password = document.getElementById("jwt_password").value.trim();

    if (!email || !password) {
      showError("⚠️ Email and password are required.");
      return;
    }

    const payload = { email, password };
    if (username) payload.username = username;

    try {
      const response = await fetch("/api/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.status === 201) {
        alert("✅ Registration successful! Please login.");
        window.location.href = "/login/";
      } else {
        // Handle DRF validation errors (like {"email":["This field must be unique."]})
        if (data.email) {
          showError(data.email[0]);
        } else if (data.password) {
          showError(data.password[0]);
        } else if (data.username) {
          showError(data.username[0]);
        } else {
          showError(data.error || data.detail || "❌ Registration failed.");
        }
      }
    } catch (err) {
      showError("🚨 Server not reachable. Try again later.");
      console.error(err);
    }
  });

  function showError(msg) {
    errorBox.textContent = msg;
    errorBox.classList.remove("d-none");
  }
});
