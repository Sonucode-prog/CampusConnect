<template>
    <Navbar />

    <div class="dashboard">

        <AdminSlidebar />

        <main class="dashboard-content">

            <h2>Admin Dashboard</h2>
            <p class="text-muted">Welcome Administrator</p>

            <!-- Statistics -->

            <div class="row mt-4">
                <div class="col-lg-3 col-md-6 mb-4" v-for="card in cards" :key="card.title">
                    <div class="card dashboard-card shadow-sm">
                        <div class="card-body">
                            <h6 class="text-muted">{{ card.title }}</h6>
                            <h2>{{ card.value }}</h2>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Registrations -->

            <div class="card mt-4">
                <div class="card-header">
                    Recent Registrations
                </div>
                <div class="card-body table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Role</th>
                                <th>Date</th>
                                <th>Is Activate</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="user in registrations" :key="user.id">
                                <td>{{ user.name }}</td>
                                <td>{{ user.role }}</td>
                                <td>{{ user.date }}</td>
                                <td>{{ user.is_activated }}</td>
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
    transform: translateY(-5px);
}

.dark-theme .dashboard-card {
    background: #1e1e1e;
    color: white;
    border: 1px solid #333;
}

.dark-theme .card {
    background: #1e1e1e;
    color: white;
}

.dark-theme .card-header {
    background: #181818;
    color: white;
    border-bottom: 1px solid #333;
}

.dark-theme table {
    color: white;
}
</style>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

import Navbar from "@/components/Navbar.vue"
import AdminSlidebar from "@/components/AdminSlidebar.vue"

const token = localStorage.getItem("admintoken")

const cards = ref([])
const registrations = ref([])

const fetchDashboard = async () => {
    try {
        const response = await axios.get(
            `${import.meta.env.VITE_API_URL}/api/admin/dashboard`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        cards.value = [
            { title: "Students", value: response.data.students },
            { title: "Companies", value: response.data.companies },
            { title: "Jobs", value: response.data.jobs },
            { title: "Applications", value: response.data.applications },
            { title: "Placements", value: response.data.placements }
        ]

        registrations.value = response.data.recent_registrations

    } catch (error) {
        console.error(error)
    }
}

onMounted(() => {
    fetchDashboard()
})
</script>