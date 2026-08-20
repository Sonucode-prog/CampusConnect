<template>
    <Navbar />
    <div class="dashboard">
        <CompSlidebar />
        <main class="dashboard-content">
            <h2 class="mb-1">
                Welcome, {{ company.company_name }}
            </h2>
            <p class="text-muted">
                {{ company.email }}
            </p>
            <!-- Cards -->
            <div class="row mt-4">
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="card dashboard-card">
                        <div class="card-body">
                            <h6>Active Jobs</h6>
                            <h2>{{ cards.active_jobs }}</h2>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="card dashboard-card">
                        <div class="card-body">
                            <h6>Applications</h6>
                            <h2>{{ cards.applications }}</h2>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="card dashboard-card">
                        <div class="card-body">
                            <h6>Interviews</h6>
                            <h2>{{ cards.interviews }}</h2>
                        </div>
                    </div>
                </div>

                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="card dashboard-card">
                        <div class="card-body">
                            <h6>Selected</h6>
                            <h2>{{ cards.selected }}</h2>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Applicants -->

            <div class="card mt-4">
                <div class="card-header">
                    Recent Applicants
                </div>
                <div class="card-body table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>College</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="applicant in applicants" :key="applicant.id">
                                <td>{{ applicant.name }}</td>
                                <td>{{ applicant.college }}</td>
                                <td>
                                    <span class="badge" :class="statusClass(applicant.status)">
                                        {{ applicant.status }}
                                    </span>
                                </td>
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

.dashboard-card {
    border: none;
    border-radius: 15px;
    transition: .3s;
}

.dashboard-card:hover {
    transform: translateY(-6px);
}

.dark-theme .dashboard-card {
    background: #1e1e1e;
    color: white;
    border: 1px solid #333;
}

.dark-theme table {
    color: white;
}

.dark-theme .card {
    background: #1e1e1e;
    color: white;
}

.dark-theme .card-header {
    background: #181818;
    color: white;
}
</style>
<script setup>

import { ref, onMounted } from "vue"
import axios from "axios"

import Navbar from "@/components/Navbar.vue"
import CompSlidebar from "@/components/CompSlidebar.vue"

const token = localStorage.getItem("companytoken")

const company = ref({})

const cards = ref({})

const applicants = ref([])

const fetchDashboard = async () => {

    try {
        const response = await axios.get(
            `${import.meta.env.VITE_API_URL}/api/company/dashboard`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        company.value = response.data.company

        cards.value = response.data.cards

        applicants.value = response.data.applicants
        // console.log(response.data)
    }
    catch (error) {
        console.log(error)
    }
}

const statusClass = (status) => {

    switch (status) {

        case "Selected":

            return "bg-success"

        case "Interview":

            return "bg-warning text-dark"

        case "Rejected":

            return "bg-danger"

        default:

            return "bg-secondary"

    }

}

onMounted(() => {

    fetchDashboard()

})

</script>