<template>
  <Navbar/>
  <div class="register-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card register-card shadow-lg">
            <div class="card-body p-5">
              <h2 class="text-center text-primary mb-4">Student Registration</h2>

              <form @submit.prevent="handleSubmit">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="username">Username:</label>
                    <input class="form-control" type="text" id="username" v-model="formData.username"
                      required />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="email">Email:</label>
                    <input class="form-control" type="email" id="email"  v-model="formData.email"
                      required />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="password">Password:</label>
                    <input class="form-control" type="password" id="password"
                      v-model="formData.password" required />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="fullname">Fullname:</label>
                    <input class="form-control" type="text" id="full_name" v-model="formData.full_name"
                      required />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="branch">Branch:</label>
                    <input class="form-control" type="text" id="branch" v-model="formData.branch"
                      required />
                  </div>
                  <div class="col-md-6 mb-3">
                    <select class="form-select" v-model="formData.year">
                      <option value="">Select Year</option>
                      <option>1st Year</option>
                      <option>2nd Year</option>
                      <option>3rd Year</option>
                      <option>4th Year</option>
                      <option>5th Year</option>
                    </select>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="cgpa">CGPA:</label>
                    <input class="form-control" type="number" id="cgpa"
                      v-model="formData.cgpa"  required/>
                  </div>

                  <div class="col-md-6 mb-3">
                    <label for="college">College:</label>
                    <input class="form-control" type="text" id="college" v-model="formData.college"
                      required />
                  </div>

                  
                  <div class="col-md-6 mb-3">
                    <label for="skill">Skills:</label>
                    <input class="form-control" type="text" id="skill" v-model="formData.skill"
                      required />
                  </div>


                  <div class="col-md-6 mb-3">
                    <label for="phone">Phone_Number:</label>
                    <input class="form-control" type="number" id="phone" maxlength="10" placeholder="xxxxxxxxxx"
                      v-model="formData.phone" required />
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

import { useRouter } from 'vue-router'
import { reactive } from 'vue'
import axios from 'axios' // Import axios for making HTTP requests so that we can send the registration data to the backend API.

const router = useRouter() // Create an instance of the router

const formData = reactive({
  //reactive:- A function used to create a reactive state object.
  username: '',
  email: '',
  password: '',
  full_name:'',
  branch:'',
  year:'',
  cgpa:'',
  college:'',
  skill:'',
  phone:'',
  
  
})

const handleSubmit = async () => {
  // handleSubmit:- An asynchronous function that will be called when the registration form is submitted.
  // It will send the form data to the backend API and handle the response.
  try {
    const response = await axios.post('http://127.0.0.1:5000/student/register', formData) // Send a POST request to the backend API endpoint '/student/register' with the formData as the request body.

    console.log(response.data.message)
    router.push('/Login') // Navigate to the login page after successful registration
  } catch (error) {
    alert(error.response?.data?.message)
  }
}

</script>
