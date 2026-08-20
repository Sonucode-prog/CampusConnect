<template>
    <Navbar />

    <div class="dashboard">

        <AdminSlidebar />

        <main class="dashboard-content">

            <!-- Back Button -->
            <button class="btn btn-outline-primary mb-4" @click="$router.back()">
                ← Back
            </button>

            <!-- Profile Card -->
            <div class="card shadow-sm">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md text-center">
                            <img src="@/assets/dummypic.png" class="profile-image"
                                alt="Student Profile">

                        </div>

                        <div class="col-md-9">

                            <h2>{{ student.full_name }}</h2>

                            <p class="text-muted mb-2">{{ student.email }}</p>

                            <span class="badge fs-6" :class="statusClass(student.status)">
                                {{ student.status }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Student Information -->

            <div class="card shadow-sm mt-4">

                <div class="card-header">
                    Student Information
                </div>

                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <strong>Username</strong>
                            <p>{{ student.username }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>Phone</strong>
                            <p>{{ student.phone }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>Branch</strong>
                            <p>{{ student.branch }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>Year</strong>
                            <p>{{ student.year }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>CGPA</strong>
                            <p>{{ student.cgpa }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong>Skills</strong>
                            <p>{{ student.skills }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>College</strong>
                            <p>{{ student.college }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Resume -->

            <div class="card shadow-sm mt-4">

                <div class="card-header">
                    Resume
                </div>

                <div class="card-body d-flex justify-content-between align-items-center">

                    <div>
                        <h6>{{ student.resume_name }}</h6>
                        <small class="text-muted">
                            Resume uploaded by the student.
                        </small>
                    </div>

                    <button class="btn btn-success" @click="downloadResume">
                        <i class="bi bi-download me-2"></i>
                        Download Resume
                    </button>

                </div>
            </div>

            <!-- Statistics -->

            <div class="row mt-4">
                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card dashboard-card">
                        <div class="card-body text-center">

                            <h6>Applications</h6>

                            <h2>{{ student.stats.applications }}</h2>

                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card dashboard-card">
                        <div class="card-body text-center">

                            <h6>Selected</h6>

                            <h2>{{ student.stats.selected }}</h2>

                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card dashboard-card">
                        <div class="card-body text-center">

                            <h6>Interview</h6>

                            <h2>{{ student.stats.interview }}</h2>

                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6 mb-3">
                    <div class="card dashboard-card">
                        <div class="card-body text-center">

                            <h6>Rejected</h6>

                            <h2>{{ student.stats.rejected }}</h2>

                        </div>
                    </div>
                </div>
            </div>

            <!-- Account Status -->

            <div class="card shadow-sm mt-4">

                <div class="card-header">
                    Account Status
                </div>

                <div class="card-body">
                    <div class="row align-items-end">
                        <div class="col-md-4">
                            <label class="form-label">
                                Status
                            </label>

                            <select class="form-select" v-model="student.status">

                                <option value="Active">Active</option>
                                <option value="Deactivated">Deactivated</option>
                                <option value="Blacklisted">Blacklisted</option>

                            </select>

                        </div>

                        <div class="col-md-3">

                            <button class="btn btn-primary" @click="saveStatus">
                                Save Status
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import axios from "axios"
import Navbar from "@/components/Navbar.vue"
import AdminSlidebar from "@/components/AdminSlidebar.vue"

const route = useRoute()
const token = localStorage.getItem("admintoken")

const student = ref({
    stats: {}
})

const fetchStudent = async () => {
    try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/admin/student/${route.params.id}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        student.value = response.data
    } catch (error) {
        console.error(error)
    }
}

const saveStatus = async () => {
    try {
        await axios.put(`${import.meta.env.VITE_API_URL}/api/admin/student/${route.params.id}/status`,
            {
                status: student.value.status
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
        alert("Student status updated successfully.")
    } catch (error) {
        console.error(error)
    }
}

const downloadResume = async () => {
    try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/admin/student/${route.params.id}/resume`,{
            responseType:"blob",
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement("a")
        link.href = url
        link.download = "resume.pdf"
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
    } catch(error) {
        console.error(error)
    }
}

const statusClass = (status) => {
    switch (status) {
        case "Active":
            return "bg-success"
        case "Deactivated":
            return "bg-warning text-dark"
        case "Blacklisted":
            return "bg-danger"
        default:
            return "bg-secondary"
    }
}

onMounted(() => {
    fetchStudent()
})
</script>