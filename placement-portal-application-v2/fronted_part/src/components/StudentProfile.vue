<template>
    
    <Navbar />\
    <StudSidebar />
    <div class="main-content">
        <div class="container py-5">
            <div class="card profile-card shadow">
                <div class="card-body">
                    <div class="row align-items-center">

                        <div class="col-md text-center">

                            <img src="@/assets/dummypic.png" class="profile-img">

                        </div>

                        <div class="col-md-9">

                            <h2>{{ student.full_name }}</h2>

                            <h5 class="text-muted">
                                {{ student.branch }}
                            </h5>

                            <p>{{ student.year }}</p>
                            <p>{{ student.college }}</p>

                            <button class="btn btn-primary me-2" @click="editProfile">
                                Edit Profile
                            </button>

                            <button class="btn btn-outline-primary" @click="downloadResume">
                                Download Resume
                            </button>

                            <button class="btn btn-outline-primary" @click="$router.push('/ResumeCard')">
                                Uploand Resume
                            </button>

                        </div>

                    </div>

                </div>

            </div>

            <div class="row mt-4">

                <div class="col-lg-6">

                    <div class="card profile-card">

                        <div class="card-header">
                            Personal Details
                        </div>

                        <div class="card-body">

                            <p><strong>Username:</strong> {{ student.username }}</p>

                            <p><strong>Email:</strong> {{ student.email }}</p>

                            <p><strong>Phone:</strong> {{ student.phone }}</p>

                        </div>

                    </div>

                </div>

                <div class="col-lg-6">

                    <div class="card profile-card">

                        <div class="card-header">
                            Academic Details
                        </div>

                        <div class="card-body">

                            <p><strong>Branch:</strong> {{ student.branch }}</p>

                            <p><strong>Year:</strong> {{ student.year }}</p>

                            <p><strong>CGPA:</strong> {{ student.cgpa }}</p>

                            <p><strong>Skills:</strong> {{ student.skill }}</p>

                        </div>

                    </div>

                </div>

            </div>


        </div>
    </div>
    
</template>

<style scoped>
.main-content {
    margin-left: 260px;
    padding: 20px;
    transition: .3s;
}

.profile-card {
    border: none;
    border-radius: 15px;
    transition: .3s;
    margin-bottom: 20px;
}

.profile-card:hover {
    transform: translateY(-5px);
}

.profile-img {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    object-fit: cover;
    border: 5px solid #0d6efd;
}

.card-header {
    font-weight: 600;
}

/* Dark Theme */

.dark-theme .profile-card {
    background: #1e1e1e;
    color: white;
    border: 1px solid #333;
}

.dark-theme .card-header {
    background: #181818;
    color: white;
    border-bottom: 1px solid #333;
}

.dark-theme .text-muted {
    color: #cfcfcf !important;
}
</style>

<script setup>
import Navbar from "./Navbar.vue";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import StudSidebar from "./StudSidebar.vue";

const router = useRouter();

const student = ref({
    username: "",
    full_name: "",
    email: "",
    branch: "",
    year: "",
    cgpa: "",
    college:"",
    skill:"",
    number: ""
});

const fetchProfile = async () => {
    try {
        const token = localStorage.getItem("studenttoken");

        const response = await axios.get(
            "http://127.0.0.1:5000/api/student/profile",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        student.value = response.data;
    } catch (error) {
        console.error("Failed to fetch profile:", error);
    }
};

const editProfile = () => {
    router.push("/StudEdit");
};

const downloadResume = async () => {
    const token = localStorage.getItem("studenttoken");
    try {
        const response = await axios.get(
            "http://127.0.0.1:5000/api/student/resume/download",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }, responseType: 'blob' // Important for downloading files without this , Axios assumes the response is JSON
            }
        )
        // Handle the downloaded file (e.g., save it or open it)
        const url = window.URL.createObjectURL(new Blob([response.data])) //create temporary URL and This URL points to the PDF stored temporarily in the browser's memory.
        const link = document.createElement('a') //Create an <a> Element like <a></a>
        link.href = url //is equivalent to <a href="blob:http://localhost:5173/...">
        link.download = "resume.pdf" // Set the desired filename, The download attribute tells the browser to download the file instead of opening it.
        document.body.appendChild(link) // The browser temporarily adds: <body>...</body>
        link.click() //Click the Link Automatically without user
        link.remove(link) //The hidden link is removed from the page because it's no longer needed.
        window.URL.revokeObjectURL(url) //The temporary Blob URL is deleted. Otherwise, it would stay in memory until the page is refreshed.
    }
    catch (error) {
        console.log(error)
        alert("RESUME not uploaded")
    }
}

onMounted(() => {
    fetchProfile();
});
</script>