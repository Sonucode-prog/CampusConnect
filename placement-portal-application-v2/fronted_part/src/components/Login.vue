<template>
  <Navbar/>
  <div class="login-page">
    <div class="container">
      <div class="row vh-100 align-items-center">
        <!-- Left Side -->
        <div class="col-lg-6 d-none d-lg-block">
          <h1 class="display-4 fw-bold text-primary">
            COMPUSCONNECT
          </h1>
  
          <p class="lead">
            Campus Placement Management System
          </p>
  
          <img src="@/assets/login.png" class="img-fluid mt-4">
        </div>
        <!-- Right Side -->
        <div class="col-lg-6">
          <div class="card login-card shadow-lg">
            <div class="card-body p-5">
  
              <h2 class="text-center mb-4">
                Welcome to CampusConnect
              </h2>
  
              <form @submit.prevent="handleLogin">
                  <div class="mb-3">
                    <label for="username">Username:</label>
                    <input type="username" id="username" v-model="formData.username" required />
                  </div>

                  <div class="mb-3">
                    <label for="password">Password:</label>
                    <input type="password" id="password" v-model="formData.password" required />
                  </div>

                  <button class="btn btn-primary w-100 py-2">
                      Login
                  </button>
              </form>
  
              <hr>

              <div class="text-center">

                  <router-link to="/StudentRegister">
                      Student Register//
                  </router-link>

                  <router-link to="/CompanyRegister">
                      Company Register
                  </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>  
  </div>
</template>
  
<style scoped>
  
  .login-page{
  
  background:#f8f9fa;
  min-height:100vh;
  }
  .login-card{
  border:none;
  border-radius:20px;
  }
  
  .form-control{
  height:50px;
  border-radius:10px;
  }
  
  .btn{
  border-radius:10px; 
  }
  
  .dark-theme .login-page{
  background:#121212;
  }
  
  .dark-theme .login-card{
  background:#1e1e1e;
  color:white;
  }
  
  .dark-theme .form-control{
  background:#2b2b2b;
  color:white;
  border:1px solid #444;
  }
  
  .dark-theme .form-control::placeholder{
  color:#ccc;
  }
  
  .dark-theme label{
  color:white;
  }
  
</style>


<script setup>
import Navbar from '../components/Navbar.vue'

import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const formData = reactive({
  username: '',
  password: ''
})

async function handleLogin() {
  try {
    const response = await axios.post('http://localhost:5000/api/login', formData)
    console.log(response.data.message)
    
    const user=response.data.user
    if (user.role === "student") {
      localStorage.setItem("studenttoken", response.data.access_token);
      router.push("/StudentDashboard")
    }
    else if (user.role === "company") {
      localStorage.setItem("companytoken", response.data.access_token);
      router.push("/CompanyDashboard")
    }
    else if (user.role === "admin") {
      localStorage.setItem("admintoken", response.data.access_token);
      router.push("/AdminDashboard")
    }
    // Redirect to student dashboard or store authentication state
  } catch (error) {
    alert(error.response?.data?.message)
  }
}
</script>