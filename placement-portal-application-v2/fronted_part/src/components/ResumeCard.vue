<template>
    <Navbar/>
    <div class="card profile-card shadow-sm mt-4">

        <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">
                <i class="bi bi-file-earmark-pdf me-2"></i>
                Resume
            </h5>

        </div>

        <div class="card-body">

            <div v-if="resume.file_name" class="resume-info">

                <div class="d-flex justify-content-between align-items-center flex-wrap">

                    <div>

                        <h6 class="mb-1">
                            {{ resume.file_name }}
                        </h6>

                        <small class="text-muted">
                            Uploaded on {{ resume.uploaded_at }}
                        </small>

                    </div>

                    <button
                        class="btn btn-success mt-2 mt-md-0"
                        @click="downloadResume"
                    >
                        <i class="bi bi-download"></i>
                        Download
                    </button>

                </div>

            </div>

            <div
                v-else
                class="text-center py-4"
            >

                <i class="bi bi-file-earmark-x display-4 text-secondary"></i>

                <p class="mt-3 text-muted">
                    No Resume Uploaded
                </p>

            </div>

            <hr>

            <label class="form-label fw-semibold">
                Upload New Resume
            </label>

            <input
                type="file"
                class="form-control"
                accept=".pdf,.doc,.docx"
                @change="selectResume"
            >

            <small class="text-muted d-block mt-2">
                Supported formats: PDF, DOC, DOCX (Max 2 MB)
            </small>

            <div class="text-end mt-3">

                <button
                    class="btn btn-primary"
                    @click="uploadResume"
                >
                    <i class="bi bi-upload"></i>
                    Upload Resume
                </button>

            </div>

        </div>

    </div>
</template>

<style scoped>
.profile-card{
    border:none;
    border-radius:15px;
    transition:.3s;
}

.profile-card:hover{
    transform:translateY(-4px);
}

.resume-info{
    background:#f8f9fa;
    border-radius:12px;
    padding:18px;
}

/* Dark Theme */

.dark-theme .resume-info{
    background:#242424;
}

.dark-theme .profile-card{
    background:#1e1e1e;
    color:white;
    border:1px solid #333;
}

.dark-theme .card-header{
    background:#181818;
    color:white;
    border-bottom:1px solid #333;
}

.dark-theme .text-muted{
    color:#bdbdbd !important;
}

.form-control{
    border-radius:10px;
}

.btn{
    border-radius:10px;
}
</style>

<script setup>
import { ref} from "vue"
import axios from "axios"
import Navbar from "./Navbar.vue"

const selectedFile = ref(null)

const resume = ref({
    file_name: "",
    uploaded_at: ""
})

const token = localStorage.getItem("studenttoken")

const selectResume = (event) => {

    selectedFile.value = event.target.files[0]

}
const fetchResume = async () => {
    try {
        const response = await axios.get(
            `${import.meta.env.VITE_API_URL}/api/student/resume`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )
        resume.value = response.data
    }
    catch (error) {
        console.log(error)
    }
}
const uploadResume = async () => {
    if (!selectedFile.value) {
        alert("Please select a resume.")
        return
    }
    const formData = new FormData()
    formData.append("resume", selectedFile.value)
    try {
        await axios.post(
            `${import.meta.env.VITE_API_URL}/api/student/resume`,
            formData,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "multipart/form-data"
                }
            }
        )
        alert("Resume uploaded successfully.")
        fetchResume()
    }
    catch (error) {
        console.log(error)
    }
}
const downloadResume = async () => {
    const token = localStorage.getItem("token");
    try{
    const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/student/resume/download`,
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
    }
}
</script>
