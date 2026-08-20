<template>
    <Navbar />
    <div class="dashboard">
        <AdminSlidebar />
        <main class="dashboard-content">

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
                                <th>Company</th>
                                <th>Job Title</th>
                                <th>Type</th>
                                <th>Location</th>
                                <th>Vacancies</th>
                                <th>Status</th>
                                <th>Approval Status</th>
                                <th>Deadline</th>
                                <th>Action</th>
                            </tr>
                        </thead>

                        <tbody>

                            <tr v-for="(job, index) in filteredJobs" :key="job.job_id">

                                <td>{{ index + 1 }}</td>
                                <td>{{ job.company }}</td>
                                <td>{{ job.title }}</td>
                                <td>{{ job.job_type }}</td>
                                <td>{{ job.location }}</td>
                                <td>{{ job.vacancies }}</td>

                                <td>

                                    <span class="badge" :class="job.status == 'Open' ? 'bg-success' : 'bg-danger'">
                                        {{ job.status }}
                                    </span>

                                </td>

                                <td>
                                    <span class="badge" :class="{
                                        'bg-warning text-dark': job.approve_status == 'Pending',
                                        'bg-success': job.approve_status == 'Approved',
                                        'bg-danger': job.approve_status == 'Rejected'
                                    }">
                                        {{ job.approve_status }}
                                    </span>
                                </td>

                                <td>{{ job.deadline }}</td>

                                <td>

                                    <button v-if="job.approve_status == 'Pending' || job.approve_status=='Rejected'" class="btn btn-success btn-sm me-2"
                                        @click="approveJob(job.job_id)">
                                        Approve
                                    </button>

                                    <button v-if="job.approve_status=='Pending' || job.approve_status=='Approved'" class="btn btn-danger btn-sm me-2"
                                        @click="rejectJob(job.job_id)">
                                        Reject
                                    </button>

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
import AdminSlidebar from "./AdminSlidebar.vue"


const token = localStorage.getItem("admintoken")

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

const closeJob = async (id) => {
    try {
        await axios.put(`${import.meta.env.VITE_API_URL}/api/jobs/${id}/close`, {}, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        fetchJobs()
    } catch (error) {
        console.error(error)
    }
}

const openJob = async (id) => {
    try {
        await axios.put(`${import.meta.env.VITE_API_URL}/api/jobs/${id}/open`, {}, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        fetchJobs()
    } catch (error) {
        console.error(error)
    }
}

const approveJob = async(id) => {
    try{
        await axios.put(`${import.meta.env.VITE_API_URL}/api/admin/jobs/${id}/approve`,{},{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        fetchJobs()
    }catch(error){
        console.error(error)
    }
}

const rejectJob = async(id) => {
    try{
        await axios.put(`${import.meta.env.VITE_API_URL}/api/admin/jobs/${id}/reject`,{},{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        fetchJobs()
    }catch(error){
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