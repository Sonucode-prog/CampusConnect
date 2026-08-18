<template>
  <Navbar />
  <div class="register-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card register-card shadow-lg">
            <div class="card-body p-5">
              <h2 class="text-center text-primary mb-4">Company Registration</h2>

              <form @submit.prevent="handleRegister">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="username">Username:</label>
                    <input class="form-control" type="text" id="username" v-model="formData.username" required />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="email">Email:</label>
                    <input class="form-control" type="email" id="email" v-model="formData.email" required />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="password">Password:</label>
                    <input class="form-control" type="password" id="password" v-model="formData.password" required />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="company_name">Company name:</label>
                    <input class="form-control" type="text" id="company_name" v-model="formData.company_name"
                      required />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="location">Location:</label>
                    <input class="form-control" type="text" id="location" v-model="formData.location" required />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="about_company">About Company:</label>
                    <input class="form-control" type="text" id="about_company" v-model="formData.about_company" />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="industry">Industry</label>
                    <input class="form-control" type="text" id="industry" v-model="formData.industry" required />
                  </div>

                  <div class="col-12">
                    <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">
                      Create Account
                    </button>
                  </div>
                  <div class="text-center mt-3">
                    Already have an account?

                    <router-link to="/Login" class="text-decoration-none fw-semibold">
                      Login
                    </router-link>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: #f8f9fa;
  transition: .4s;
}

.dark-theme .register-page {
  background: #121212;
}

.register-card {
  border: none;
  border-radius: 18px;
  overflow: hidden;
  transition: .3s;
}

.register-card:hover {
  transform: translateY(-5px);
}

.dark-theme .register-card {
  background: #1e1e1e;
  color: white;
  border: 1px solid #333;
  box-shadow: 0 0 20px rgba(255, 255, 255, .08);
}

label {
  font-weight: 600;
  margin-bottom: 6px;
}

.form-control {
  border-radius: 10px;
  padding: 10px 14px;
}

.form-control:focus {
  box-shadow: none;
  border-color: #0d6efd;
}

.dark-theme .form-control {
  background: #222;
  color: white;
  border: 1px solid #444;
}

.dark-theme .form-control:focus {
  background: #2b2b2b;
  color: white;
}

.btn-primary {
  border-radius: 10px;
  transition: .3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
}
</style>

<script setup>
import Navbar from '../components/Navbar.vue'

import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const formData = reactive({
  username: '',
  email: '',
  password: '',
  company_name: '',
  location: '',
  about_company: '',
  industry: ''

})
const router = useRouter()

async function handleRegister() {
  try {
    const response = await axios.post('http://127.0.0.1:5000/company/register', formData)
    alert(response.data.message)
    router.push('/Login')
  } catch (error) {
    alert(error.response.data.message)
  }
}
</script>
