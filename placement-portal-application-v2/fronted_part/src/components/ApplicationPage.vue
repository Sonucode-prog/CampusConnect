<template>
    <Navbar />

    <div class="dashboard">

        <StudentSidebar />

        <main class="dashboard-content">

            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>My Applications</h2>
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

                        <div class="col-md-6 mb-2">
                            <input type="text" class="form-control" placeholder="Search Company or Job..."
                                v-model="search">
                        </div>

                        <div class="col-md-3 mb-2">
                            <select class="form-select" v-model="statusFilter">
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
                    Applied Jobs
                </div>

                <div class="card-body table-responsive">

                    <table class="table align-middle">

                        <thead>

                            <tr>
                                <th>#</th>
                                <th>Company</th>
                                <th>Job</th>
                                <th>Applied On</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>

                        </thead>

                        <tbody>

                            <tr v-for="(application, index) in filteredApplications" :key="application.application_id">

                                <td>{{ index + 1 }}</td>
                                <td>{{ application.company }}</td>
                                <td>{{ application.job_title }}</td>
                                <td>{{ application.applied_at }}</td>

                                <td>

                                    <span class="badge" :class="statusClass(application.status)">
                                        {{ application.status }}
                                    </span>

                                </td>

                                <td>

                                    <router-link :to="`/student/application/${application.application_id}`"
                                        class="btn btn-primary btn-sm">
                                        View
                                    </router-link>

                                </td>

                            </tr>

                            <tr v-if="filteredApplications.length == 0">

                                <td colspan="6" class="text-center">
                                    No Applications Found
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
import StudentSidebar from "@/components/StudSidebar.vue"

const token = localStorage.getItem("studenttoken")

const applications = ref([])
const search = ref("")
const statusFilter = ref("")

const fetchApplications = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:5000/api/student/applications",{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        applications.value = response.data
    } catch(error) {
        console.error(error)
    }
}

const filteredApplications = computed(() => {
    return applications.value.filter(application => {
        const searchMatch = application.company.toLowerCase().includes(search.value.toLowerCase()) || application.job_title.toLowerCase().includes(search.value.toLowerCase())
        const statusMatch = statusFilter.value=="" || application.status===statusFilter.value
        return searchMatch && statusMatch
    })
})

const statusClass = status => {
    switch(status){
        case "Pending":
            return "bg-secondary"
        case "Shortlisted":
            return "bg-info text-dark"
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

        const token = localStorage.getItem("studenttoken");

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
            const token = localStorage.getItem("studenttoken");

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
        const token = localStorage.getItem("studenttoken");

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
        link.download = "student_history.csv";

        document.body.appendChild(link);
        link.click();
        link.remove();

        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error(error);
        alert("CSV download failed");
    }
}

onMounted(() => {
    fetchApplications()
})
</script>