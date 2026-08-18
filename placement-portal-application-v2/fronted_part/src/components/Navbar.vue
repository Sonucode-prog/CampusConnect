<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow">

        <div class="container">

            <div class="collapse navbar-collapse" id="menu">

                <ul class="navbar-nav ms-auto">

                    <li class="nav-item">
                        <router-link to="/LandingPage" class="nav-link">Home</router-link>
                    </li>

                    <li class="nav-item">
                        <a href="#features" class="nav-link">Features</a>
                    </li>

                    <li class="nav-item">
                        <a href="#about" class="nav-link">About</a>
                    </li>

                    <li class="nav-item">
                        <a href="#stats" class="nav-link">Statistics</a>
                    </li>

                    <div class="ms-auto d-flex">

                        <button class="btn btn-outline-light me-2" @click="toggleTheme">

                            {{ darkMode ? "☀ Light" : "🌙 Dark" }}

                        </button>

                        <router-link to="/login" class="btn btn-light me-2">

                            Login

                        </router-link>
                        <div>
                            <select class="btn btn-warning" @change="$router.push($event.target.value)">
                                <option disabled selected>Register</option>
                                <option value="/StudentRegister">Student Register</option>
                                <option value="/CompanyRegister">Company Register</option>
                            </select>
                        </div>
                        <button class="btn btn-outline-light me-2" @click="$router.back()">
                            ← Back
                        </button>
                    </div>
                </ul>
            </div>
        </div>

    </nav>
</template>

<script setup>
import { ref, onMounted } from "vue"

const darkMode = ref(false)

onMounted(() => {
    darkMode.value = localStorage.getItem("theme") === "dark"

    if (darkMode.value)
        document.body.classList.add("dark-theme")
})

function toggleTheme() {

    darkMode.value = !darkMode.value

    if (darkMode.value) {
        document.body.classList.add("dark-theme")
        localStorage.setItem("theme", "dark")
    }
    else {
        document.body.classList.remove("dark-theme")
        localStorage.setItem("theme", "light")
    }

}
</script>