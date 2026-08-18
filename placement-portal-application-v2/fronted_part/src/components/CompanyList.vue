<template>
    <Navbar />
    <div class="dashboard">
        <AdminSlidebar />
        <main class="dashboard-content">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Company Management</h2>
            </div>
            <!-- Search & Filter -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mb-2">
                            <input type="text" class="form-control" placeholder="Search Company..." v-model="search">
                        </div>

                        <div class="col-md-3 mb-2">
                            <select class="form-select" v-model="statusFilter">
                                <option value="">All Status</option>
                                <option value="Pending">Pending</option>
                                <option value="Approved">Approved</option>
                                <option value="Rejected">Rejected</option>
                                <option value="Blocked">Blocked</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Company Table -->
            <div class="card shadow-sm">
                <div class="card-header">
                    Registered Companies
                </div>
                <div class="card-body table-responsive">
                    <table class="table align-middle">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Company</th>
                                <th>Email</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(company, index) in filteredCompanies" :key="company.company_id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ company.company_name }}</td>
                                <td>{{ company.email }}</td>
                                <td>
                                    <span class="badge" :class="statusClass(company.status)">
                                        {{ company.status }}
                                    </span>
                                </td>
                                <td>
                                    <router-link :to="`/admin/company/${company.company_id}`"
                                        class="btn btn-primary btn-sm">
                                        View
                                    </router-link>
                                </td>
                            </tr>
                            <tr v-if="filteredCompanies.length == 0">
                                <td colspan="5" class="text-center text-muted">
                                    No companies found.
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
.card {
    border: none;
    border-radius: 15px;
}
.table th {
    font-weight: 600;
}
.badge {
    padding: 8px 12px;
    font-size: .8rem;
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
.dark-theme input,
.dark-theme select {
    background: #222;
    color: white;
    border-color: #444;
}
.dark-theme input::placeholder {
    color: #bbb;
}
</style>

<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"

import Navbar from "@/components/Navbar.vue"
import AdminSlidebar from "@/components/AdminSlidebar.vue"

const token = localStorage.getItem("admintoken")
const companies = ref([])
const search = ref("")
const statusFilter = ref("")
const fetchCompanies = async () => {
    try {
        const response = await axios.get(
            "http://127.0.0.1:5000/api/admin/companies",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )
        companies.value = response.data
    }
    catch (error) {
        console.error(error)
    }
}

const filteredCompanies = computed(() => {
    return companies.value.filter(company => {
        const searchMatch =
            company.company_name.toLowerCase().includes(search.value.toLowerCase())

        const statusMatch =
            statusFilter.value == "" ||
            company.status == statusFilter.value

        return searchMatch && statusMatch
    })
})

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
    fetchCompanies()
})
</script>