<template>
    <Navbar />
    <div class="dashboard">
        <StudentSidebar />
        <main class="dashboard-content">
            <button class="btn btn-outline-primary mb-4" @click="$router.back()">
                ← Back
            </button>

            <div class="card shadow-sm">
                <div class="card-body">
                    <h2>{{ application.job_title }}</h2>
                    <h5 class="text-primary">{{ application.company_name }}</h5>
                    <span class="badge" :class="statusClass(application.status)">
                        {{ application.status }}
                    </span>
                </div>
            </div>

            <div class="card shadow-sm mt-4">
                <div class="card-header">
                    Company Information
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <strong>Industry</strong>
                            <p>{{ application.industry }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong>Location</strong>
                            <p>{{ application.location }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card shadow-sm mt-4">
                <div class="card-header">
                    Job Information
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <strong>Job Type</strong>
                            <p>{{ application.job_type }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong>Salary</strong>
                            <p>{{ application.salary }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong>Experience</strong>
                            <p>{{ application.experience }}</p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <strong>Deadline</strong>
                            <p>{{ application.deadline }}</p>
                        </div>
                        <div class="col-12">
                            <strong>Required Skills</strong>
                            <p>{{ application.skills }}</p>
                        </div>
                        <div class="col-12 mt-2">
                            <strong>Job Description</strong>
                            <p>{{ application.description }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card shadow-sm mt-4">
                <div class="card-header">
                    Application Status
                </div>
                <div class="card-body">

                    <div class="mb-4">
                        <div class="progress" style="height:10px;">
                            <div class="progress-bar" :style="{width:progressWidth}"></div>
                        </div>
                    </div>

                    <div class="row text-center">
                        <div class="col">Applied</div>
                        <div class="col">Shortlisted</div>
                        <div class="col">Interview</div>
                        <div class="col">{{ application.status=="Rejected" ? "Rejected" : "Selected" }}</div>
                    </div>

                    <hr>

                    <p><strong>Applied On :</strong> {{ application.applied_at }}</p>
                    <p><strong>Current Status :</strong> {{ application.status }}</p>

                </div>
            </div>

        </main>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import axios from "axios"
import Navbar from "@/components/Navbar.vue"
import StudentSidebar from "@/components/StudSidebar.vue"

const route = useRoute()
const token = localStorage.getItem("studenttoken")

const application = ref({})

const fetchApplication = async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:5000/api/student/application/${route.params.id}`,{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        application.value = response.data
    } catch(error) {
        console.error(error)
    }
}

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

const progressWidth = computed(() => {
    switch(application.value.status){
        case "Pending":
            return "25%"
        case "Shortlisted":
            return "50%"
        case "Interview":
            return "75%"
        case "Selected":
            return "100%"
        case "Rejected":
            return "100%"
        default:
            return "25%"
    }
})

onMounted(() => {
    fetchApplication()
})
</script>
<style>
.dashboard{
    display:flex;
}

.dashboard-content{
    flex:1;
    margin-left:260px;
    padding:30px;
}

.card{
    border:none;
    border-radius:15px;
}

.progress{
    border-radius:20px;
}

.progress-bar{
    transition:.5s;
}

.badge{
    padding:8px 15px;
    font-size:14px;
}

.dark-theme .card{
    background:#1e1e1e;
    color:white;
    border:1px solid #333;
}

.dark-theme .card-header{
    background:#181818;
    color:white;
    border-bottom:1px solid #333;
}

.dark-theme p,
.dark-theme strong,
.dark-theme h2,
.dark-theme h5{
    color:white;
}

.dark-theme .progress{
    background:#333;
}
</style>

