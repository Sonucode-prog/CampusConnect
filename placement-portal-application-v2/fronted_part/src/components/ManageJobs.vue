<template>
    <Navbar />
    <div class="dashboard">
        <CompSlidebar />
        <main class="dashboard-content">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Manage Jobs</h2>
                <router-link to="/PostJobs" class="btn btn-primary">
                    <i class="bi bi-plus-circle me-2"></i>
                    Post Job
                </router-link>
            </div>

            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <input type="text" class="form-control" placeholder="Search Job by Title..." v-model="search">
                </div>
            </div>

            <div class="card shadow-sm">
                <div class="card-header">
                    Posted Jobs
                </div>

                <div class="card-body table-responsive">

                    <table class="table align-middle">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Job Title</th>
                                <th>Type</th>
                                <th>Location</th>
                                <th>Vacancies</th>
                                <th>Status</th>
                                <th>Approval</th>
                                <th>Deadline</th>
                                <th>Action</th>
                            </tr>
                        </thead>

                        <tbody>

                            <tr v-for="(job, index) in filteredJobs" :key="job.job_id">

                                <td>{{ index + 1 }}</td>
                                <td>{{ job.title }}</td>
                                <td>{{ job.job_type }}</td>
                                <td>{{ job.location }}</td>
                                <td>{{ job.vacancies }}</td>

                                <td>

                                    <span class="badge" :class="job.status == 'Open' ? 'bg-success' : 'bg-danger'">
                                        {{ job.status }}
                                    </span>

                                </td>
                                <td>{{job.approve_status}}</td>

                                <td>{{ job.deadline }}</td>

                                <td>

                                    <button class="btn btn-warning btn-sm me-2" @click="deleteJob(job.job_id)">
                                        Delete
                                    </button>

                                    <button v-if="job.status == 'Open'" class="btn btn-danger btn-sm"
                                        @click="closeJob(job.job_id)">
                                        Close
                                    </button>

                                    <button v-else class="btn btn-success btn-sm" @click="openJob(job.job_id)">
                                        Reopen
                                    </button>

                                </td>
                            </tr>

                            <tr v-if="filteredJobs.length == 0">
                                <td colspan="8" class="text-center">
                                    No Jobs Found
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"
import Navbar from "@/components/Navbar.vue"
import CompSlidebar from "@/components/CompSlidebar.vue"

const token = localStorage.getItem("companytoken")

const jobs = ref([])
const search = ref("")

const fetchJobs = async () => {
    try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/jobs`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        jobs.value = response.data
    } catch (error) {
        console.error(error)
    }
}

const filteredJobs = computed(() => {
    return jobs.value.filter(job =>
        job.title.toLowerCase().includes(search.value.toLowerCase())
    )
})

const deleteJob = async (id) => {
    if (!confirm("Delete this job?")) return

    try {
        await axios.delete(`${import.meta.env.VITE_API_URL}/api/jobs/${id}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })

        jobs.value = jobs.value.filter(job => job.job_id !== id)


    } catch (error) {
        console.error(error)
        alert("you can't delete , there is some applicats in this Jobs, Close it instead of deleting")
    }
}

const closeJob = async(id) => {
    try {
        await axios.put(`${import.meta.env.VITE_API_URL}/api/jobs/${id}/close`,{},{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        fetchJobs()
    } catch(error) {
        console.error(error)
    }
}

const openJob = async(id) => {
    try {
        await axios.put(`${import.meta.env.VITE_API_URL}/api/jobs/${id}/open`,{},{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        fetchJobs()
    } catch(error) {
        console.error(error)
    }
}

onMounted(() => {
    fetchJobs()
})
</script>

<style>
.dashboard {
    display: flex;
}

.dashboard-content {
    flex: 1;
    margin-left: 260px;
    padding: 30px;
}

.card {
    border: none;
    border-radius: 15px;
}

.dark-theme .card {
    background: #1e1e1e;
    color: white;
    border: 1px solid #333;
}

.dark-theme .card-header {
    background: #181818;
    color: white;
    border-bottom: 1px solid #333;
}

.dark-theme table {
    color: white;
}

.dark-theme input {
    background: #222;
    color: white;
    border-color: #444;
}

.badge {
    padding: 7px 12px;
}
</style>