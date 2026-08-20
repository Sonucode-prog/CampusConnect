<template>
    <nav class="navbar navbar-expand-lg custom-navbar">
        <div class="container">

            <!-- Brand -->
            <router-link to="/LandingPage" class="navbar-brand brand">
                <span class="brand-icon">🎓</span>
                <span>Campus<span class="brand-highlight">Connect</span></span>
            </router-link>

            <!-- Mobile Toggle -->
            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#menu"
                aria-controls="menu"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>

            <!-- Navigation -->
            <div class="collapse navbar-collapse" id="menu">

                <!-- Center Menu -->
                <ul class="navbar-nav mx-auto navigation-links">

                    <li class="nav-item">
                        <router-link
                            to="/LandingPage"
                            class="nav-link"
                            active-class="active-link"
                        >
                            Home
                        </router-link>
                    </li>

                    <li class="nav-item">
                        <a href="#features" class="nav-link">
                            Features
                        </a>
                    </li>

                    <li class="nav-item">
                        <a href="#about" class="nav-link">
                            About
                        </a>
                    </li>

                    <li class="nav-item">
                        <a href="#stats" class="nav-link">
                            Statistics
                        </a>
                    </li>

                </ul>

                <!-- Right Side -->
                <div class="navbar-actions">

                    <!-- Theme -->
                    <button
                        class="theme-btn"
                        @click="toggleTheme"
                        :title="darkMode ? 'Switch to light mode' : 'Switch to dark mode'"
                    >
                        <span v-if="darkMode">☀️</span>
                        <span v-else>🌙</span>

                        <span class="theme-text">
                            {{ darkMode ? "Light" : "Dark" }}
                        </span>
                    </button>

                    <!-- Login -->
                    <router-link
                        to="/login"
                        class="login-btn"
                    >
                        Login
                    </router-link>

                    <!-- Register Dropdown -->
                    <div class="register-wrapper">

                        <select
                            class="register-select"
                            @change="$router.push($event.target.value)"
                        >
                            <option value="" disabled selected>
                                Register
                            </option>

                            <option value="/StudentRegister">
                                Student Register
                            </option>

                            <option value="/CompanyRegister">
                                Company Register
                            </option>
                        </select>

                    </div>

                    <!-- Back -->
                    <button
                        class="back-btn"
                        @click="$router.back()"
                        title="Go back"
                    >
                        ←
                        <span>Back</span>
                    </button>

                </div>

            </div>
        </div>
    </nav>
</template>


<script setup>
import { ref, onMounted } from "vue"

const darkMode = ref(false)

onMounted(() => {

    darkMode.value = localStorage.getItem("theme") === "dark"

    if (darkMode.value) {
        document.body.classList.add("dark-theme")
    }

})


function toggleTheme() {

    darkMode.value = !darkMode.value

    if (darkMode.value) {

        document.body.classList.add("dark-theme")

        localStorage.setItem("theme", "dark")

    } else {

        document.body.classList.remove("dark-theme")

        localStorage.setItem("theme", "light")

    }

}
</script>


<style scoped>

/* =========================
   NAVBAR
========================= */

.custom-navbar {
    min-height: 72px;

    background: linear-gradient(
        135deg,
        #0d6efd,
        #0b5ed7
    );

    box-shadow:
        0 4px 20px rgba(0, 0, 0, 0.12);

    position: sticky;
    top: 0;
    z-index: 1000;
}


/* =========================
   BRAND
========================= */

.brand {
    display: flex;
    align-items: center;
    gap: 9px;

    font-size: 1.35rem;
    font-weight: 700;

    color: white !important;

    text-decoration: none;

    letter-spacing: -0.4px;
}

.brand-icon {
    width: 40px;
    height: 40px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: rgba(255, 255, 255, 0.18);

    border-radius: 12px;

    font-size: 20px;

    backdrop-filter: blur(10px);
}

.brand-highlight {
    color: #ffe082;
}


/* =========================
   NAVIGATION
========================= */

.navigation-links {
    gap: 5px;
}

.navigation-links .nav-link {

    position: relative;

    color: rgba(255, 255, 255, 0.85) !important;

    font-weight: 500;

    padding: 10px 15px !important;

    border-radius: 10px;

    transition:
        background 0.25s ease,
        color 0.25s ease,
        transform 0.25s ease;
}

.navigation-links .nav-link:hover {

    color: white !important;

    background: rgba(255, 255, 255, 0.12);

    transform: translateY(-1px);
}


/* Active Link */

.navigation-links .active-link {

    color: white !important;

    background: rgba(255, 255, 255, 0.16);

}


/* =========================
   RIGHT ACTIONS
========================= */

.navbar-actions {

    display: flex;

    align-items: center;

    gap: 8px;
}


/* =========================
   THEME BUTTON
========================= */

.theme-btn {

    border: 1px solid rgba(255, 255, 255, 0.35);

    background: rgba(255, 255, 255, 0.10);

    color: white;

    padding: 8px 13px;

    border-radius: 10px;

    font-weight: 500;

    display: flex;

    align-items: center;

    gap: 6px;

    transition: all 0.25s ease;
}

.theme-btn:hover {

    background: rgba(255, 255, 255, 0.20);

    transform: translateY(-1px);
}


/* =========================
   LOGIN
========================= */

.login-btn {

    padding: 9px 18px;

    border-radius: 10px;

    background: white;

    color: #0d6efd;

    font-weight: 600;

    text-decoration: none;

    transition: all 0.25s ease;
}

.login-btn:hover {

    background: #f1f5ff;

    color: #084298;

    transform: translateY(-2px);

    box-shadow:
        0 5px 15px rgba(0, 0, 0, 0.15);
}


/* =========================
   REGISTER
========================= */

.register-wrapper {
    position: relative;
}

.register-select {

    appearance: none;

    min-width: 130px;

    padding: 9px 34px 9px 15px;

    border: none;

    border-radius: 10px;

    background-color: #ffc107;

    color: #212529;

    font-weight: 600;

    cursor: pointer;

    transition: all 0.25s ease;

    background-image:
        linear-gradient(45deg, transparent 50%, #212529 50%),
        linear-gradient(135deg, #212529 50%, transparent 50%);

    background-position:
        calc(100% - 16px) 14px,
        calc(100% - 11px) 14px;

    background-size:
        5px 5px,
        5px 5px;

    background-repeat: no-repeat;
}

.register-select:hover {

    background-color: #ffca2c;

    transform: translateY(-1px);

    box-shadow:
        0 5px 15px rgba(0, 0, 0, 0.12);
}

.register-select:focus {

    outline: none;

    box-shadow:
        0 0 0 3px rgba(255, 193, 7, 0.3);
}


/* =========================
   BACK BUTTON
========================= */

.back-btn {

    border: 1px solid rgba(255, 255, 255, 0.35);

    background: transparent;

    color: white;

    padding: 8px 13px;

    border-radius: 10px;

    font-weight: 500;

    transition: all 0.25s ease;
}

.back-btn:hover {

    background: rgba(255, 255, 255, 0.15);

    transform: translateX(-2px);
}


/* =========================
   MOBILE
========================= */

@media (max-width: 991px) {

    .custom-navbar {
        padding: 10px 0;
    }

    .navigation-links {

        margin-top: 15px;

        width: 100%;

        gap: 3px;
    }

    .navigation-links .nav-link {

        padding: 10px 15px !important;
    }

    .navbar-actions {

        margin-top: 15px;

        padding-top: 15px;

        border-top:
            1px solid rgba(255, 255, 255, 0.2);

        flex-wrap: wrap;
    }

}


@media (max-width: 576px) {

    .brand {
        font-size: 1.15rem;
    }

    .brand-icon {
        width: 36px;
        height: 36px;
    }

    .theme-text {
        display: none;
    }

    .navbar-actions {
        gap: 6px;
    }

    .login-btn,
    .register-select,
    .back-btn,
    .theme-btn {
        font-size: 13px;
    }

    .register-select {
        min-width: 115px;
    }

    .back-btn span {
        display: none;
    }

}

</style>