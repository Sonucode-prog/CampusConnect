<template>
    <div class="container py-5">

        <button class="btn btn-outline-primary mb-4" @click="$router.back()">
            ← Back
        </button>

        <div class="card profile-card shadow">

            <div class="card-header">

                <h4>Edit Profile</h4>

            </div>

            <div class="card-body">

                <form @submit.prevent="updateProfile">

                    <div class="row">

                        <div class="col-md-6 mb-3">

                            <label class="form-label">
                                Full Name
                            </label>

                            <input type="text" class="form-control" v-model="student.full_name">

                        </div>

                        <div class="col-md-6 mb-3">

                            <label class="form-label">
                                Email
                            </label>

                            <input type="email" class="form-control" v-model="student.email">

                        </div>

                        <div class="col-md-6 mb-3">

                            <label class="form-label">
                                Branch
                            </label>

                            <input type="text" class="form-control" v-model="student.branch">

                        </div>

                        <div class="col-md-6 mb-3">

                            <label class="form-label">
                                Year
                            </label>

                            <select class="form-select" v-model="student.year">
                                <option value="1">1st Year</option>
                                <option value="2">2nd Year</option>
                                <option value="3">3rd Year</option>
                                <option value="4">4th Year</option>
                            </select>

                        </div>

                        <div class="col-md-6 mb-3">

                            <label class="form-label">
                                CGPA
                            </label>

                            <input type="number" class="form-control" step="0.01" min="0" max="10"
                                v-model="student.cgpa">

                        </div>

                        <div class="col-md-6 mb-3">

                            <label class="form-label">
                                Phone
                            </label>

                            <input type="tel" class="form-control" v-model="student.phone">

                        </div>

                    </div>

                    <div class="text-end">

                        <button class="btn btn-primary">
                            Save Changes
                        </button>

                    </div>

                </form>

            </div>

        </div>

    </div>
</template>
<style scoped>
.profile-card {
    border: none;
    border-radius: 15px;
}

.dark-theme .profile-card {
    background: #1e1e1e;
    color: white;
    border: 1px solid #333;
}

.dark-theme .card-header {
    background: #181818;
    color: white;
    border-bottom: 1px solid #333;
}
</style>
<script setup>

import { ref, onMounted } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()

const token = localStorage.getItem("studenttoken")

const student = ref({})

const fetchProfile = async () => {

    const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/student/profile`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    )

    student.value = response.data

}

const updateProfile = async () => {
    try{
    await axios.put(
        `${import.meta.env.VITE_API_URL}/api/student/profile`,
        student.value,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    )

    alert("Profile Updated Successfully")

    router.push("/StudentProfile")
    } catch (err){
        console.log("Status:", err.response.status)
        console.log("Data:", err.response.data)
    }

}

onMounted(() => {

    fetchProfile()

})

</script>