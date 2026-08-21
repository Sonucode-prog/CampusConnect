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

                <div class="brand-text">
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
                    <i class="bi bi-speedometer2"></i>
                    <span>Dashboard</span>
                </router-link>
            </li>


            <li class="nav-item">
                <router-link
                    to="/StudentProfile"
                    class="nav-link"
                >
                    <i class="bi bi-person-circle"></i>
                    <span>My Profile</span>
                </router-link>
            </li>


            <li class="nav-item">
                <router-link
                    to="/BrowserJobs"
                    class="nav-link"
                >
                    <i class="bi bi-briefcase"></i>
                    <span>Browse Jobs</span>
                </router-link>
            </li>


            <li class="nav-item">
                <router-link
                    to="/ApplicationPage"
                    class="nav-link"
                >
                    <i class="bi bi-file-earmark-text"></i>
                    <span>My Applications</span>
                </router-link>
            </li>


            <li class="nav-item">
                <router-link
                    to="/ResumeCard"
                    class="nav-link"
                >
                    <i class="bi bi-file-earmark-arrow-up"></i>
                    <span>Resume</span>
                </router-link>
            </li>


            <li class="nav-item">
                <router-link
                    to="/Notification"
                    class="nav-link"
                >
                    <i class="bi bi-bell"></i>
                    <span>Notifications</span>
                </router-link>
            </li>

        </ul>


        <!-- Logout -->
        <div class="logout">

            <button
                class="btn btn-danger logout-btn"
                @click="logout"
            >
                <i class="bi bi-box-arrow-right"></i>
                <span>Logout</span>
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

.sidebar {

    width: 260px;

    height: 100vh;

    position: fixed;

    left: 0;
    top: 0;

    background: linear-gradient(
        180deg,
        #0d6efd 0%,
        #0965e5 100%
    );

    color: white;

    display: flex;
    flex-direction: column;

    z-index: 1000;

    transition: all 0.3s ease;

    box-shadow: 4px 0 15px rgba(0, 0, 0, 0.08);
}


/* =========================
   HEADER
========================= */

.sidebar-header {

    padding: 18px;

    border-bottom: 1px solid rgba(255,255,255,.15);

}

.brand {

    display: flex;

    align-items: center;

    color: white;

    gap: 12px;

}

.logo {

    width: 42px;
    height: 42px;

    object-fit: cover;

    border-radius: 50%;

    background: white;

}

.brand-text h5 {

    font-size: 15px;

    font-weight: 700;

}

.brand-text small {

    font-size: 10px;

    opacity: .75;

}


/* =========================
   NAVIGATION
========================= */

.nav {

    flex: 1;

    padding-top: 5px;

}

.nav-item {

    width: 100%;

}

.nav-link {

    color: rgba(255,255,255,.9);

    margin: 5px 12px;

    border-radius: 9px;

    padding: 11px 14px;

    transition: all .25s ease;

    display: flex;

    align-items: center;

    gap: 10px;

    font-size: 13px;

    white-space: nowrap;

}

.nav-link i {

    width: 20px;

    text-align: center;

    font-size: 15px;

    flex-shrink: 0;

}

.nav-link:hover {

    background: rgba(255,255,255,.15);

    color: white;

    transform: translateX(3px);

}

.router-link-active {

    background: white;

    color: #0d6efd !important;

    font-weight: 600;

    box-shadow: 0 4px 12px rgba(0,0,0,.08);

}


/* =========================
   LOGOUT
========================= */

.logout {

    padding: 15px;

}

.logout-btn {

    border: none;

    padding: 10px;

    border-radius: 9px;

    display: flex;

    align-items: center;

    justify-content: center;

    gap: 8px;

    font-size: 13px;

}

.logout-btn i {

    font-size: 15px;

}


/* =========================
   TABLET
========================= */

@media (max-width: 991px) {

    .sidebar {

        width: 220px;

    }

}


/* =========================
   MOBILE SIDEBAR
========================= */

@media (max-width: 767px) {

    .sidebar {

        width: 80px;

    }


    /* Hide logo text */

    .sidebar-header {

        padding: 15px 10px;

    }

    .brand {

        justify-content: center;

    }

    .brand-text {

        display: none;

    }

    .logo {

        width: 42px;

        height: 42px;

    }


    /* Navigation */

    .nav-link {

        justify-content: center;

        margin: 5px 8px;

        padding: 12px 5px;

        gap: 0;

    }

    .nav-link i {

        font-size: 18px;

        width: auto;

    }

    .nav-link span {

        display: none;

    }

    .nav-link:hover {

        transform: none;

    }


    /* Logout */

    .logout {

        padding: 10px 8px;

    }

    .logout-btn {

        width: 100% !important;

        padding: 10px 5px;

    }

    .logout-btn span {

        display: none;

    }

}


/* =========================
   DARK THEME
========================= */

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