<template>
    <Navbar />

    <div class="dashboard">

        <CompSlidebar />

        <main class="dashboard-content">

            <button class="btn btn-outline-primary mb-4" @click="$router.back()">
                ← Back
            </button>

            <div class="card shadow-sm">

                <div class="card-body">

                    <div class="row align-items-center">

                        <div class="col-md-3 text-center">

                            <img src="@/assets/dummypic.png" class="company-logo" alt="Student">

                        </div>

                        <div class="col-md">

                            <h2>{{ applicant.full_name }}</h2>

                            <p class="text-muted mb-1">{{ applicant.email }}</p>

                            <span class="badge bg-primary">
                                {{ applicant.branch }}
                            </span>

                        </div>

                    </div>

                </div>

            </div>

            <div class="card shadow-sm mt-4">

                <div class="card-header">
                    Student Information
                </div>

                <div class="card-body">

                    <div class="row">

                        <div class="col-md-6 mb-3">
                            <strong>Phone</strong>
                            <p>{{ applicant.phone }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>College</strong>
                            <p>{{ applicant.college }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>Branch</strong>
                            <p>{{ applicant.branch }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>Year</strong>
                            <p>{{ applicant.year }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>CGPA</strong>
                            <p>{{ applicant.cgpa }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>Skills</strong>
                            <p>{{ applicant.skills }}</p>
                        </div>

                    </div>

                </div>

            </div>

            <div class="card shadow-sm mt-4">

                <div class="card-header">
                    Applied Job
                </div>

                <div class="card-body">

                    <h5>{{ applicant.job_title }}</h5>

                    <p>{{ applicant.job_type }}</p>

                    <p>{{ applicant.location }}</p>

                </div>

            </div>

            <div class="card shadow-sm mt-4">

                <div class="card-header">
                    Resume
                </div>

                <div class="card-body d-flex justify-content-between align-items-center">

                    <div>

                        <h6>{{ applicant.resume_name }}</h6>

                        <small class="text-muted">
                            Uploaded Resume
                        </small>

                    </div>

                    <button class="btn btn-success" @click="downloadResume">
                        Download Resume
                    </button>

                </div>

            </div>

            <div class="card shadow-sm mt-4">

                <div class="card-header">
                    Application Status
                </div>

                <div class="card-body">

                    <div class="row align-items-end">

                        <div class="col-md-4">

                            <label class="form-label">
                                Status
                            </label>

                            <select class="form-select" v-model="applicant.status">

                                <option>Pending</option>
                                <option>Shortlisted</option>
                                <option>Interview</option>
                                <option>Selected</option>
                                <option>Rejected</option>

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
import CompSlidebar from "@/components/AdminSlidebar.vue"

const route = useRoute()
const token = localStorage.getItem("companytoken")

const applicant = ref({})

const fetchApplicant = async () => {
    try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/applicant/${route.params.id}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        applicant.value = response.data
        
    } catch (error) {
        console.error(error)
    }
}

const saveStatus = async () => {
    try {
        await axios.put(`${import.meta.env.VITE_API_URL}/api/application/${route.params.id}/status`,
            {
                status: applicant.value.status
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
        alert("Application status updated successfully.")
    } catch (error) {
        console.error(error)
        alert("Failed to update status.")
    }
}

const downloadResume = async () => {
    // const token = localStorage.getItem("token");
    try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/application/${route.params.id}/resume`,{
            responseType:"blob",
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        // Handle the downloaded file (e.g., save it or open it)
        const url = window.URL.createObjectURL(new Blob([response.data])) //create temporary URL and This URL points to the PDF stored temporarily in the browser's memory.
        const link = document.createElement('a') //Create an <a> Element like <a></a>
        link.href = url //is equivalent to <a href="blob:http://localhost:5173/...">
        link.download = "resume.pdf" // Set the desired filename, The download attribute tells the browser to download the file instead of opening it.
        document.body.appendChild(link) // The browser temporarily adds: <body>...</body>
        link.click() //Click the Link Automatically without user
        link.remove(link) //The hidden link is removed from the page because it's no longer needed.
        window.URL.revokeObjectURL(url) //The temporary Blob URL is deleted. Otherwise, it would stay in memory until the page is refreshed.
    }
    catch (error) {
        console.error(error)
        alert("Unable to download resume.")
    }
}
onMounted(() =>{
    fetchApplicant()
    })
</script>