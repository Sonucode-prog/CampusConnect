<template>
    <aside class="sidebar">

        <!-- Logo -->
        <div class="sidebar-header">

            <router-link
                to="/Landing"
                class="brand text-decoration-none"
            >
                <img
                    src="@/assets/logo.png"
                    alt="Logo"
                    class="logo"
                >

                <div>
                    <h5 class="mb-0">COMPUSCONNECT</h5>
                    <small>Student Portal</small>
                </div>

            </router-link>

        </div>

        <!-- Navigation -->

        <ul class="nav flex-column mt-3">

            <li class="nav-item">

                <router-link
                    to="/StudentDashboard"
                    class="nav-link"
                >
                    <i class="bi bi-speedometer2 me-2"></i>
                    Dashboard
                </router-link>

            </li>

            <li class="nav-item">

                <router-link
                    to="/StudentProfile"
                    class="nav-link"
                >
                    <i class="bi bi-person-circle me-2"></i>
                    My Profile
                </router-link>

            </li>

            <li class="nav-item">

                <router-link
                    to="/BrowserJobs"
                    class="nav-link"
                >
                    <i class="bi bi-briefcase me-2"></i>
                    Browse Jobs
                </router-link>

            </li>

            <li class="nav-item">

                <router-link
                    to="/ApplicationPage"
                    class="nav-link"
                >
                    <i class="bi bi-file-earmark-text me-2"></i>
                    My Applications
                </router-link>

            </li>


            <li class="nav-item">

                <router-link
                    to="/ResumeCard"
                    class="nav-link"
                >
                    <i class="bi bi-file-earmark-arrow-up me-2"></i>
                    Resume
                </router-link>

            </li>

            <li class="nav-item">

                <router-link
                    to="/Notification"
                    class="nav-link"
                >
                    <i class="bi bi-bell me-2"></i>
                    Notifications
                </router-link>

            </li>

        </ul>

        <!-- Logout -->

        <div class="logout">

            <button
                class="btn btn-danger w-100"
                @click="logout"
            >
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

    localStorage.removeItem("studenttoken")

    localStorage.removeItem("role")

    router.push("/login")

}
</script>

<style scoped>

.sidebar{

    width:260px;

    height:100vh;

    position:fixed;

    left:0;

    top:0;

    background:#0d6efd;

    color:white;

    display:flex;

    flex-direction:column;

    transition:.4s;

}

.sidebar-header{

    padding:20px;

    border-bottom:1px solid rgba(255,255,255,.15);

}

.brand{

    display:flex;

    align-items:center;

    color:white;

    gap:12px;

}

.logo{

    width:45px;

    height:45px;

    border-radius:50%;

}

.nav{

    flex:1;

}

.nav-link{

    color:white;

    margin:6px 12px;

    border-radius:10px;

    padding:12px 15px;

    transition:.3s;

    display:flex;

    align-items:center;

}

.nav-link:hover{

    background:rgba(255,255,255,.15);

}

.router-link-active{

    background:white;

    color:#0d6efd !important;

    font-weight:600;

}

.logout{

    padding:20px;

}

/* Dark Theme */

.dark-theme .sidebar{

    background:#0d1117;

}

.dark-theme .router-link-active{

    background:#1e1e1e;

    color:white !important;

}

.dark-theme .nav-link:hover{

    background:#222;

}

</style>