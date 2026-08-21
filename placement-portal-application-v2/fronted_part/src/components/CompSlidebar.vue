<template>
  <aside class="sidebar">

    <!-- Logo -->
    <div class="sidebar-header">

      <router-link
        to="/CompanyDashboard"
        class="brand text-decoration-none"
      >

        <img
          src="@/assets/logo.png"
          alt="Logo"
          class="logo"
        >

        <div class="brand-text">

          <h5 class="mb-0">
            COMPUSCONNECT
          </h5>

          <small>
            Company Portal
          </small>

        </div>

      </router-link>

    </div>


    <!-- Navigation -->
    <ul class="nav flex-column mt-3">

      <li class="nav-item">

        <router-link
          to="/CompanyDashboard"
          class="nav-link"
        >

          <i class="bi bi-speedometer2"></i>

          <span>
            Dashboard
          </span>

        </router-link>

      </li>


      <li class="nav-item">

        <router-link
          to="/CompProfile"
          class="nav-link"
        >

          <i class="bi bi-building"></i>

          <span>
            Company Profile
          </span>

        </router-link>

      </li>


      <li class="nav-item">

        <router-link
          to="/PostJobs"
          class="nav-link"
        >

          <i class="bi bi-plus-circle"></i>

          <span>
            Post Job
          </span>

        </router-link>

      </li>


      <li class="nav-item">

        <router-link
          to="/ManageJobs"
          class="nav-link"
        >

          <i class="bi bi-briefcase"></i>

          <span>
            Manage Jobs
          </span>

        </router-link>

      </li>


      <li class="nav-item">

        <router-link
          to="/Applicants"
          class="nav-link"
        >

          <i class="bi bi-people"></i>

          <span>
            Applicants
          </span>

        </router-link>

      </li>


      <li class="nav-item">

        <router-link
          to="/CompanyReport"
          class="nav-link"
        >

          <i class="bi bi-bar-chart-line"></i>

          <span>
            Reports
          </span>

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

        <span>
          Logout
        </span>

      </button>

    </div>

  </aside>
</template>


<script setup>

import { useRouter } from "vue-router"

const router = useRouter()


const logout = () => {

  localStorage.removeItem("companytoken")

  localStorage.removeItem("role")

  router.push("/login")

}

</script>


<style scoped>

/* =====================================================
   SIDEBAR
===================================================== */

.sidebar {

  width: 260px;

  height: 100vh;

  position: fixed;

  top: 0;
  left: 0;

  background:
    linear-gradient(
      180deg,
      #0d6efd 0%,
      #0965e5 100%
    );

  color: white;

  display: flex;

  flex-direction: column;

  z-index: 1000;

  transition: all .3s ease;

  box-shadow:
    4px 0 15px rgba(0, 0, 0, .08);

}


/* =====================================================
   HEADER
===================================================== */

.sidebar-header {

  padding: 18px;

  border-bottom:
    1px solid rgba(255,255,255,.15);

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


/* =====================================================
   NAVIGATION
===================================================== */

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

  padding: 11px 14px;

  border-radius: 9px;

  display: flex;

  align-items: center;

  gap: 10px;

  font-size: 13px;

  white-space: nowrap;

  transition: all .25s ease;

}


.nav-link i {

  width: 20px;

  text-align: center;

  flex-shrink: 0;

  font-size: 16px;

}


.nav-link:hover {

  background:
    rgba(255,255,255,.15);

  color: white;

  transform: translateX(3px);

}


.router-link-active {

  background: white;

  color: #0d6efd !important;

  font-weight: 600;

  box-shadow:
    0 4px 12px rgba(0,0,0,.08);

}


/* =====================================================
   LOGOUT
===================================================== */

.logout {

  padding: 15px;

}


.logout-btn {

  width: 100%;

  padding: 10px;

  border: none;

  border-radius: 9px;

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 8px;

  font-size: 13px;

}


.logout-btn i {

  font-size: 16px;

}


/* =====================================================
   TABLET
===================================================== */

@media (max-width: 991px) {

  .sidebar {

    width: 220px;

  }

}


/* =====================================================
   MOBILE
===================================================== */

@media (max-width: 767px) {

  .sidebar {

    width: 80px;

  }


  /* Logo */

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

    width: auto;

    font-size: 18px;

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

    padding: 10px 5px;

  }


  .logout-btn span {

    display: none;

  }

}


/* =====================================================
   DARK THEME
===================================================== */

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