document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("jwtLoginForm");
  const errorBox = document.getElementById("loginErrorBox");
  const submitBtn = form?.querySelector("button[type='submit']");
  

  const nextUrlInput = document.getElementById("next_url");
  const nextUrl = nextUrlInput && nextUrlInput.value && nextUrlInput.value !== "None"
    ? nextUrlInput.value
    : "/";  // fallback → home page

  if (!form) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML =
        '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging in...';
    }

    const email = document.getElementById("jwt_email").value.trim();
    const password = document.getElementById("jwt_password").value.trim();

    if (!email || !password) {
      showError("⚠ Email and password are required.");
      enableSubmit();
      return;
    }

    try {
      // 1 JWT login API call
      const loginResponse = await fetch("/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include"
      });

      const loginData = await loginResponse.json();

      if (!loginResponse.ok) {
        showError(loginData.detail || loginData.error || "⚠ Invalid credentials");
        enableSubmit();
        return;
      }

      // 2 Save tokens in sessionStorage (optional)
      sessionStorage.setItem("access", loginData.access);
      sessionStorage.setItem("refresh", loginData.refresh);

      // 3 Save tokens in Django session
      const sessionResponse = await fetch("/login_session_save/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          access: loginData.access,
          refresh: loginData.refresh
        }),
        credentials: "include"
      });

      if (!sessionResponse.ok) {
        const sessionError = await sessionResponse.json().catch(() => ({}));
        showError(sessionError.error || "⚠ Session could not be established");
        enableSubmit();
        return;
      }

      // 4️⃣ Show welcome alert before redirecting
      alert("✅ Welcome! Login successful.");

      // 5️⃣ Redirect on successful login
      window.location.href = nextUrl;

    } catch (err) {
      console.error("Login error:", err);
      showError("⚠ Network error. Please try again.");
      enableSubmit();
    }
  });

  function showError(msg) {
    if (errorBox) {
      errorBox.textContent = msg;
      errorBox.classList.remove("d-none");
      setTimeout(() => errorBox.classList.add("d-none"), 5000);
    } else {
      alert(msg);
    }
  }

  function enableSubmit() {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = "Login";
    }
  }
});
