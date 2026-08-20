<template>
    <Navbar />
    <div class="dashboard">
        <CompSlidebar />
        <main class="dashboard-content">
            <div class="page-header mb-4">
                <div>
                    <h2 class="fw-bold mb-1">Placement Report</h2>
                    <p class="text-muted mb-0">Generate and download your monthly placement analytics report.</p>
                </div>
            </div>
            <div class="report-card shadow-sm">
                <div class="report-icon">
                    <i class="bi bi-file-earmark-bar-graph"></i>
                </div>
                <div class="report-content">
                    <h3>Monthly Placement Report</h3>
                    <p class="text-muted">Get a detailed report containing job applications, interviews, selections and placement statistics for your company.</p>
                    <div class="report-features">
                        <span><i class="bi bi-check-circle-fill"></i> Application Statistics</span>
                        <span><i class="bi bi-check-circle-fill"></i> Interview Analytics</span>
                        <span><i class="bi bi-check-circle-fill"></i> Selection Report</span>
                        <span><i class="bi bi-check-circle-fill"></i> Placement Summary</span>
                    </div>
                    <button class="btn btn-primary generate-btn mt-4" @click="generateReport" :disabled="loading">
                        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                        <i v-else class="bi bi-gear-fill me-2"></i>
                        {{ loading ? "Generating Report..." : "Generate Monthly Report" }}
                    </button>
                </div>
            </div>
            <div v-if="reportReady" class="success-card shadow-sm mt-4">
                <div class="success-info">
                    <div class="success-icon">
                        <i class="bi bi-check-lg"></i>
                    </div>
                    <div>
                        <h5 class="mb-1">Report Generated Successfully</h5>
                        <p class="mb-0">Your monthly placement report is ready to download.</p>
                    </div>
                </div>
                <button class="btn btn-success download-btn" @click="downloadReport">
                    <i class="bi bi-download me-2"></i>
                    Download Report
                </button>
            </div>
        </main>
    </div>
</template>
<style>
.dashboard{
    display:flex;
}
.dashboard-content{
    flex:1;
    margin-left:260px;
    padding:35px;
    min-height:100vh;
}
.page-header h2{
    color:#212529;
}
.report-card{
    background:white;
    border-radius:18px;
    padding:40px;
    display:flex;
    align-items:center;
    gap:40px;
    border:1px solid #eee;
}
.report-icon{
    width:150px;
    height:150px;
    min-width:150px;
    border-radius:25px;
    background:linear-gradient(135deg,#0d6efd,#6610f2);
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:65px;
}
.report-content{
    flex:1;
}
.report-content h3{
    font-weight:700;
    margin-bottom:12px;
}
.report-content p{
    max-width:750px;
    line-height:1.7;
}
.report-features{
    display:flex;
    flex-wrap:wrap;
    gap:15px 25px;
    margin-top:20px;
}
.report-features span{
    font-weight:500;
}
.report-features i{
    color:#198754;
    margin-right:7px;
}
.generate-btn{
    padding:11px 22px;
    border-radius:9px;
}
.success-card{
    background:#eaf8f0;
    border:1px solid #badbcc;
    border-radius:15px;
    padding:22px 25px;
    display:flex;
    align-items:center;
    justify-content:space-between;
}
.success-info{
    display:flex;
    align-items:center;
    gap:15px;
}
.success-icon{
    width:50px;
    height:50px;
    border-radius:50%;
    background:#198754;
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:25px;
}
.download-btn{
    padding:10px 20px;
    border-radius:8px;
}
.dark-theme .dashboard-content{
    background:#121212;
}
.dark-theme .page-header h2{
    color:white;
}
.dark-theme .report-card{
    background:#1e1e1e;
    color:white;
    border-color:#333;
}
.dark-theme .report-card .text-muted{
    color:#bdbdbd !important;
}
.dark-theme .success-card{
    background:#173528;
    color:white;
    border-color:#285943;
}
.dark-theme .success-card p{
    color:#cfcfcf;
}
@media(max-width:768px){
    .dashboard-content{
        margin-left:0;
        padding:20px;
    }
    .report-card{
        flex-direction:column;
        text-align:center;
        padding:25px;
    }
    .report-features{
        justify-content:center;
    }
    .success-card{
        flex-direction:column;
        gap:20px;
        text-align:center;
    }
}
</style>
<script setup>

import { ref } from "vue";
import axios from "axios";
import CompSlidebar from "./CompSlidebar.vue";


const loading = ref(false);
const reportReady = ref(false);
const taskId = ref(null);


const generateReport = async () => {

    const token = localStorage.getItem("companytoken");

    try {

        loading.value = true;
        reportReady.value = false;

        const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/api/company/report`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        taskId.value = response.data.task_id;

        checkTaskStatus();

    } catch (error) {

        console.log(error);

        loading.value = false;
    }
};


const checkTaskStatus = () => {

    const interval = setInterval(async () => {

        const token = localStorage.getItem("companytoken");

        try {

            const response = await axios.get(
                `${import.meta.env.VITE_API_URL}/api/task/${taskId.value}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            if (response.data.status === "SUCCESS") {

                clearInterval(interval);

                loading.value = false;
                reportReady.value = true;
            }

            if (response.data.status === "FAILURE") {

                clearInterval(interval);

                loading.value = false;

                alert("Report generation failed");
            }

        } catch (error) {

            clearInterval(interval);

            loading.value = false;

            console.log(error);
        }

    }, 2000);
};


const downloadReport = async () => {

    const token = localStorage.getItem("companytoken");

    try {

        const response = await axios.get(
            `${import.meta.env.VITE_API_URL}/api/company/report/download`,
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

        link.setAttribute(
            "download",
            "placement_report.html"
        );

        document.body.appendChild(link);

        link.click();

        link.remove();

        window.URL.revokeObjectURL(url);

    } catch (error) {

        console.log(error);
    }
};

</script>