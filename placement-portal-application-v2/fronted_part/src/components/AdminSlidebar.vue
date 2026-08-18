<template>
    <aside class="sidebar">

        <!-- Logo -->
        <div class="sidebar-header">
            <router-link to="/admin/dashboard" class="brand text-decoration-none">
                <img src="@/assets/logo.png" alt="Logo" class="logo">

                <div>
                    <h5 class="mb-0">COMPUSCONNECT</h5>
                    <small>Admin Portal</small>
                </div>
            </router-link>
        </div>

        <!-- Navigation -->
        <ul class="nav flex-column mt-3">

            <li class="nav-item">
                <router-link to="/AdminDashboard" class="nav-link">
                    <i class="bi bi-speedometer2 me-2"></i>
                    Dashboard
                </router-link>
            </li>

            <li class="nav-item">
                <router-link to="/admin/students" class="nav-link">
                    <i class="bi bi-mortarboard me-2"></i>
                    Students
                </router-link>
            </li>

            <li class="nav-item">
                <router-link to="/admin/companies" class="nav-link">
                    <i class="bi bi-building me-2"></i>
                    Companies
                </router-link>
            </li>

            <li class="nav-item">
                <router-link to="/AdminManageJobs" class="nav-link">
                    <i class="bi bi-briefcase me-2"></i>
                    Jobs
                </router-link>
            </li>

            <li class="nav-item">
                <router-link to="/AdminApplicants" class="nav-link">
                    <i class="bi bi-file-earmark-text me-2"></i>
                    Applications
                </router-link>
            </li>

        </ul>

        <!-- Logout -->
        <div class="logout">
            <button class="btn btn-danger w-100" @click="logout">
                <i class="bi bi-box-arrow-right me-2"></i>
                Logout
            </button>
        </div>

    </aside>
</template>

<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

const logout = () => {
    localStorage.removeItem("admintoken")
    localStorage.removeItem("role")
    router.push("/login")
}
</script>

<style scoped>
.sidebar {
    width: 260px;
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    background: #0d6efd;
    color: white;
    display: flex;
    flex-direction: column;
    transition: .3s;
    z-index: 1000;
}

.sidebar-header {
    padding: 20px;
    border-bottom: 1px solid rgba(255,255,255,.15);
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    color: white;
}

.logo {
    width: 45px;
    height: 45px;
    border-radius: 50%;
}

.nav {
    flex: 1;
}

.nav-link {
    color: white;
    margin: 6px 12px;
    padding: 12px 16px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    transition: .3s;
}

.nav-link:hover {
    background: rgba(255,255,255,.15);
}

.router-link-active {
    background: white;
    color: #0d6efd !important;
    font-weight: 600;
}

.logout {
    padding: 20px;
}

/* Dark Theme */

.dark-theme .sidebar {
    background: #0d1117;
}

.dark-theme .router-link-active {
    background: #1e1e1e;
    color: white !important;
}

.dark-theme .nav-link:hover {
    background: #222;
}
</style>