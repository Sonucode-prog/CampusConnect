<template>
    <CompSlidebar />
    <Navbar />

    <div class="dashboard">
        <main class="dashboard-content">
            <button class="btn btn-outline-primary mb-4" @click="$router.back()">
                ← Back
            </button>
            <div class="card shadow-sm">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3 text-center">
                            <img src="@/assets/dummypic.png" class="company-logo">
                        </div>
                        <div class="col-md-9">
                            <h2>{{ company.company_name }}</h2>
                            <p class="text-muted"><strong>Email:</strong> {{ company.email }}</p>
                            <p class="text-muted"><strong>Username:</strong> {{ company.username }}</p>
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
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(job, index) in company.jobs" :key="job.id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ job.title }}</td>
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
.dark-theme .text-muted{
    color:#d1d5db !important;
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
import CompSlidebar from "@/components/CompSlidebar.vue"

const route = useRoute()

const token = localStorage.getItem("companytoken")

const company = ref({
    company_name: "",
    email: "",
    username: "",
    industry: "",
    location: "",
    about_company: "",
    logo: "",
    status: "",
    jobs: []
})

const fetchCompany = async () => {

    try {

        const response = await axios.get(
            `http://127.0.0.1:5000/api/company/profile`,
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

onMounted(() => {
    fetchCompany()
})
</script>