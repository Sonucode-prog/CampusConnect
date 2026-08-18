<template>
    <Navbar />
    <div class="dashboard">
        <AdminSlidebar/>
        <main class="dashboard-content">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Student Management</h2>
            </div>
            <!-- Search -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mb-2">
                            <input type="text" class="form-control" placeholder="Search Student..." v-model="search">
                        </div>
                    </div>
                </div>
            </div>

            <!-- Student Table -->
            <div class="card shadow-sm">
                <div class="card-header">
                    Registered Students
                </div>
                <div class="card-body table-responsive">
                    <table class="table align-middle">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Student</th>
                                <th>Email</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(student, index) in filteredStudents" :key="student.student_id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ student.student_name }}</td>
                                <td>{{ student.email }}</td>
                                <td>
                                    <router-link :to="`/admin/student/${student.student_id}`"
                                        class="btn btn-primary btn-sm">
                                        View
                                    </router-link>
                                </td>
                            </tr>
                            <tr v-if="filteredStudents.length == 0">
                                <td colspan="5" class="text-center text-muted">
                                    No students found.
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
import AdminSlidebar from "./AdminSlidebar.vue"

const token = localStorage.getItem("admintoken")
const students = ref([])
const search = ref("")
const fetchStudents = async () => {
    try {
        const response = await axios.get(
            "http://127.0.0.1:5000/api/admin/students",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )
        students.value = response.data
    }
    catch (error) {
        console.error(error)
    }
}

const filteredStudents = computed(() => {
    return students.value.filter(student => {
        const searchMatch =
            student.student_name.toLowerCase().includes(search.value.toLowerCase())

        return searchMatch
    })
})

onMounted(() => {
    fetchStudents()
})
</script>