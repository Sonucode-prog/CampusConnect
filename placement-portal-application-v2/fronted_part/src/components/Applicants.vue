<template>
    <Navbar />
    <div class="dashboard">
        <CompSlidebar />
        <main class="dashboard-content">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Applicants</h2>
            </div>
            <button
                class="btn btn-success"
                @click="startExport"
                :disabled="exporting">
                {{ exporting ? "Exporting..." : "Export CSV" }}
            </button>
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-5 mb-2">
                            <input type="text" class="form-control" placeholder="Search Student..." v-model="search">
                        </div>

                        <div class="col-md-3 mb-2">
                            <select class="form-select" v-model="selectedJob">
                                <option value="">All Jobs</option>
                                <option v-for="job in jobs" :key="job.job_id" :value="job.title">
                                    {{ job.title }}
                                </option>
                            </select>
                        </div>

                        <div class="col-md-3 mb-2">
                            <select class="form-select" v-model="selectedStatus">
                                <option value="">All Status</option>
                                <option>Pending</option>
                                <option>Shortlisted</option>
                                <option>Interview</option>
                                <option>Selected</option>
                                <option>Rejected</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card shadow-sm">
                <div class="card-header">
                    Applicant List
                </div>
                <div class="card-body table-responsive">
                    <table class="table align-middle">

                        <thead>

                            <tr>
                                <th>#</th>
                                <th>Student</th>
                                <th>Job</th>
                                <th>CGPA</th>
                                <th>Applied On</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>

                        </thead>

                        <tbody>

                            <tr v-for="(app, index) in filteredApplicants" :key="app.application_id">

                                <td>{{ index + 1 }}</td>
                                <td>{{ app.student_name }}</td>
                                <td>{{ app.job_title }}</td>
                                <td>{{ app.cgpa }}</td>
                                <td>{{ app.applied_at }}</td>

                                <td>

                                    <span class="badge" :class="statusClass(app.status)">
                                        {{ app.status }}
                                    </span>

                                </td>

                                <td>

                                    <router-link :to="`/ApplicationProfile/${app.application_id}`"
                                        class="btn btn-primary btn-sm">
                                        View
                                    </router-link>

                                </td>

                            </tr>

                            <tr v-if="filteredApplicants.length == 0">

                                <td colspan="7" class="text-center">
                                    No Applicants Found
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

const applicants = ref([])
const jobs = ref([])

const search = ref("")
const selectedJob = ref("")
const selectedStatus = ref("")

const fetchApplicants = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:5000/api/applicants", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        applicants.value = response.data.applicants
        jobs.value = response.data.jobs
    } catch (error) {
        console.error(error)
    }
}

const filteredApplicants = computed(() => {
    return applicants.value.filter(app => {
        const searchMatch = app.student_name.toLowerCase().includes(search.value.toLowerCase())
        const jobMatch = selectedJob.value == "" || app.job_title === selectedJob.value
        const statusMatch = selectedStatus.value == "" || app.status === selectedStatus.value
        return searchMatch && jobMatch && statusMatch
    })
})

const statusClass = status => {
    switch (status) {
        case "Pending":
            return "bg-secondary"
        case "Shortlisted":
            return "bg-info"
        case "Interview":
            return "bg-warning text-dark"
        case "Selected":
            return "bg-success"
        case "Rejected":
            return "bg-danger"
        default:
            return "bg-secondary"
    }
}

const exporting = ref(false);

const startExport = async () => {
    try {
        exporting.value = true;

        const token = localStorage.getItem("companytoken");

        const response = await axios.post(
            "http://127.0.0.1:5000/api/export-history",
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        const exportId = response.data.export_id;

        checkExportStatus(exportId);

    } catch (error) {
        console.error(error);
        exporting.value = false;
        alert("Unable to start export");
    }
};

const checkExportStatus = (exportId) => {
    const interval = setInterval(async () => {
        try {
            const token = localStorage.getItem("companytoken");

            const response = await axios.get(
                `http://127.0.0.1:5000/api/export-history/${exportId}/status`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            if (response.data.status === "COMPLETED") {
                clearInterval(interval);
                exporting.value = false;

                downloadCSV(exportId);
            }

            if (response.data.status === "FAILED") {
                clearInterval(interval);
                exporting.value = false;

                alert("CSV export failed");
            }

        } catch (error) {
            clearInterval(interval);
            exporting.value = false;
            console.error(error);
        }
    }, 3000);
};

const downloadCSV = async (exportId) => {
    try {
        const token = localStorage.getItem("companytoken");

        const response = await axios.get(
            `http://127.0.0.1:5000/api/export-history/${exportId}/download`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                },
                responseType: "blob"
            }
        );

        const url = window.URL.createObjectURL(
            new Blob([response.data])
        );

        const link = document.createElement("a");

        link.href = url;
        link.download = "company_history.csv";

        document.body.appendChild(link);
        link.click();
        link.remove();

        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error(error);
        alert("CSV download failed");
    }
};

onMounted(() => {
    fetchApplicants()
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

.badge {
    padding: 7px 12px;
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
</style>