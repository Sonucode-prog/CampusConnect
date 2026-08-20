<template>
    <Navbar />
    <div class="dashboard">
        <CompSlidebar />
        <main class="dashboard-content">
            <h2 class="mb-4">Post New Job</h2>
            <div class="card shadow-sm">
                <div class="card-body">
                    <form @submit.prevent="postJob">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Job Title</label>
                                <input type="text" class="form-control" v-model="job.title" required>
                            </div>

                            <div class="col-md-6 mb-3">
                                <label class="form-label">Job Type</label>
                                <select class="form-select" v-model="job.job_type">
                                    <option value="">Select Job Type</option>
                                    <option>Full Time</option>
                                    <option>Internship</option>
                                    <option>Part Time</option>
                                    <option>Contract</option>
                                </select>
                            </div>

                            <div class="col-md-6 mb-3">
                                <label class="form-label">Location</label>
                                <input type="text" class="form-control" v-model="job.location" required>
                            </div>

                            <div class="col-md-6 mb-3">
                                <label class="form-label">Salary / Stipend</label>
                                <input type="text" class="form-control" v-model="job.salary" required>
                            </div>

                            <div class="col-md-6 mb-3">
                                <label class="form-label">Experience</label>
                                <input type="text" class="form-control" v-model="job.experience" required>
                            </div>

                            <div class="col-md-6 mb-3">
                                <label class="form-label">Application Deadline</label>
                                <input type="date" class="form-control" v-model="job.deadline" required>
                            </div>

                            <div class="col-md-6 mb-3">
                                <label class="form-label">Required CGPA</label>
                                <input type="number" step="0.01" class="form-control" v-model="job.cgpa" required>
                            </div>

                            <div class="col-md-6 mb-3">
                                <label class="form-label">Vacancies</label>
                                <input type="number" class="form-control" v-model="job.vacancies" required>
                            </div>

                            <div class="col-12 mb-3">
                                <label class="form-label">Required Skills</label>
                                <input type="text" class="form-control" placeholder="Python, Flask, SQL..." v-model="job.skills" required>
                            </div>

                            <div class="col-12 mb-3">
                                <label class="form-label">Job Description</label>
                                <textarea rows="6" class="form-control" v-model="job.description"></textarea>
                            </div>

                            <div class="col-12 text-end">
                                <button class="btn btn-primary">
                                    <i class="bi bi-plus-circle me-2"></i>
                                    Post Job
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import Navbar from "@/components/Navbar.vue"
import CompSlidebar from "@/components/CompSlidebar.vue"

const router = useRouter()
const token = localStorage.getItem("companytoken")

const job = ref({
    title: "",
    job_type: "",
    location: "",
    salary: "",
    experience: "",
    deadline: "",
    cgpa: "",
    vacancies: "",
    skills: "",
    description: ""
})

const postJob = async () => {
    try {
        await axios.post(
            `${import.meta.env.VITE_API_URL}/api/company/jobs`,
            job.value,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        alert("Job posted successfully.")

        job.value = {
            title: "",
            job_type: "",
            location: "",
            salary: "",
            experience: "",
            deadline: "",
            cgpa: "",
            vacancies: "",
            skills: "",
            description: ""
        }

        router.push("/ManageJobs")

    } catch (error) {
        console.error(error)

        if (error.response) {
            alert(error.response.data.message)
        } else {
            alert("Something went wrong.")
        }
    }
}
</script>