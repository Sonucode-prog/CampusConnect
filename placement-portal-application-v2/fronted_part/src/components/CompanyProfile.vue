<template>
    <Navbar />

    <div class="dashboard">

        <AdminSlidebar />

        <main class="dashboard-content">

            <button class="btn btn-outline-primary mb-4" @click="$router.back()">
                ← Back
            </button>

            <div class="card shadow-sm">

                <div class="card-body">

                    <div class="row">


                        <div class="col-md-9">

                            <h2>{{ company.company_name }}</h2>

                            <p class="text-muted">{{ company.email }}</p>

                            <span class="badge fs-6" :class="statusClass(company.status)">
                                {{ company.status }}
                            </span>

                        </div>

                    </div>

                </div>

            </div>

            <!-- Company Details -->

            <div class="card shadow-sm mt-4">

                <div class="card-header">
                    Company Information
                </div>

                <div class="card-body">

                    <div class="row">

                        

                        <div class="col-md-6 mb-3">
                            <strong>Industry</strong>
                            <p>{{ company.industry }}</p>
                        </div>

                        <div class="col-md-6 mb-3">
                            <strong>Location</strong>
                            <p>{{ company.location }}</p>
                        </div>

                        

                        <div class="col-12">

                            <strong>About Company</strong>

                            <p>
                                {{ company.about_company }}
                            </p>

                        </div>

                    </div>

                </div>

            </div>

            <!-- Status -->

            <div class="card shadow-sm mt-4">

                <div class="card-header">
                    Company Status
                </div>

                <div class="card-body">

                    <div class="row align-items-end">

                        <div class="col-md-4">

                            <label class="form-label">
                                Status
                            </label>

                            <select class="form-select" v-model="company.status">

                                <option>Pending</option>
                                <option>Approved</option>
                                <option>Rejected</option>
                                <option>Blocked</option>

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

            <!-- Jobs -->

            <div class="card shadow-sm mt-4">

                <div class="card-header">

                    Jobs Posted

                </div>

                <div class="card-body table-responsive">

                    <table class="table">

                        <thead>

                            <tr>

                                <th>#</th>
                                <th>Job Title</th>
                                <th>Job Type</th>

                            </tr>

                        </thead>

                        <tbody>

                            <tr v-for="(job, index) in company.jobs" :key="job.id">

                                <td>{{ index + 1 }}</td>

                                <td>{{ job.title }}</td>
                                <td>{{ job.job_type }}</td>

                            </tr>

                        </tbody>

                    </table>

                </div>

            </div>

        </main>

    </div>

</template>

<style>
.dashboard {
    display: flex;
}

.dashboard-content {
    flex: 1;
    margin-left: 260px;
    padding: 30px;
}

.company-logo {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border-radius: 15px;
    border: 3px solid #0d6efd;
}

.card {
    border: none;
    border-radius: 15px;
}

.badge {
    padding: 8px 15px;
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

.dark-theme .form-select {
    background: #222;
    color: white;
    border-color: #444;
}
</style>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import axios from "axios"

import Navbar from "@/components/Navbar.vue"
import AdminSlidebar from "@/components/AdminSlidebar.vue"

const route = useRoute()

const token = localStorage.getItem("admintoken")

const company = ref({
    jobs: []
})

const fetchCompany = async () => {

    try {

        const response = await axios.get(
            `http://127.0.0.1:5000/api/admin/company/${route.params.id}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        company.value = response.data

    }

    catch (error) {

        console.error(error)

    }

}

const saveStatus = async () => {

    try {

        await axios.put(
            `http://127.0.0.1:5000/api/admin/company/${route.params.id}/status`,
            {
                status: company.value.status
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        alert("Company status updated successfully.")

    }

    catch (error) {

        console.error(error)

    }

}

const statusClass = (status) => {

    switch (status) {

        case "Approved":
            return "bg-success"

        case "Pending":
            return "bg-warning text-dark"

        case "Rejected":
            return "bg-danger"

        case "Blocked":
            return "bg-dark"

        default:
            return "bg-secondary"

    }

}

onMounted(() => {

    fetchCompany()

})
</script>