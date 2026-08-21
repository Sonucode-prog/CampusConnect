<template>
    <Navbar />

    <div class="dashboard">

        <!-- Company Sidebar -->
        <CompSlidebar />

        <!-- Main Content -->
        <main class="dashboard-content">

            <!-- =========================
                 WELCOME BANNER
            ========================== -->

            <div class="welcome-banner shadow-sm">

                <div class="welcome-content">

                    <p class="welcome-small">
                        COMPANY DASHBOARD
                    </p>

                    <h1>
                        Welcome, {{ company.company_name }} 👋
                    </h1>

                    <p class="welcome-description">
                        Manage your job postings, track applications,
                        and find the right candidates for your company.
                    </p>

                    <div class="company-email">
                        <i class="bi bi-envelope-fill"></i>
                        {{ company.email }}
                    </div>

                </div>

                <div class="welcome-icon">
                    <i class="bi bi-building"></i>
                </div>

            </div>


            <!-- =========================
                 STATISTICS
            ========================== -->

            <div class="row g-4 statistics-row">

                <!-- Active Jobs -->

                <div class="col-12 col-sm-6 col-lg-3">

                    <div class="stat-card card-blue">

                        <div class="stat-icon">
                            <i class="bi bi-briefcase-fill"></i>
                        </div>

                        <div class="stat-content">

                            <p>Active Jobs</p>

                            <h2>
                                {{ cards.active_jobs || 0 }}
                            </h2>

                        </div>

                        <div class="stat-decoration"></div>

                    </div>

                </div>


                <!-- Applications -->

                <div class="col-12 col-sm-6 col-lg-3">

                    <div class="stat-card card-purple">

                        <div class="stat-icon">
                            <i class="bi bi-file-earmark-text-fill"></i>
                        </div>

                        <div class="stat-content">

                            <p>Applications</p>

                            <h2>
                                {{ cards.applications || 0 }}
                            </h2>

                        </div>

                        <div class="stat-decoration"></div>

                    </div>

                </div>


                <!-- Interviews -->

                <div class="col-12 col-sm-6 col-lg-3">

                    <div class="stat-card card-orange">

                        <div class="stat-icon">
                            <i class="bi bi-calendar-check-fill"></i>
                        </div>

                        <div class="stat-content">

                            <p>Interviews</p>

                            <h2>
                                {{ cards.interviews || 0 }}
                            </h2>

                        </div>

                        <div class="stat-decoration"></div>

                    </div>

                </div>


                <!-- Selected -->

                <div class="col-12 col-sm-6 col-lg-3">

                    <div class="stat-card card-green">

                        <div class="stat-icon">
                            <i class="bi bi-person-check-fill"></i>
                        </div>

                        <div class="stat-content">

                            <p>Selected</p>

                            <h2>
                                {{ cards.selected || 0 }}
                            </h2>

                        </div>

                        <div class="stat-decoration"></div>

                    </div>

                </div>

            </div>


            <!-- =========================
                 RECENT APPLICANTS HEADER
            ========================== -->

            <div class="section-header">

                <div>

                    <p class="section-subtitle">
                        CANDIDATES
                    </p>

                    <h3>
                        Recent Applicants
                    </h3>

                </div>

                <button
                    class="view-all-btn"
                    @click="$router.push('/Applicants')"
                >
                    View All
                    <i class="bi bi-arrow-right"></i>
                </button>

            </div>


            <!-- =========================
                 APPLICANTS TABLE
            ========================== -->

            <div class="applicants-container shadow-sm">

                <div class="table-responsive">

                    <table class="table applicants-table">

                        <thead>

                            <tr>

                                <th>Applicant</th>

                                <th>College</th>

                                <th>Status</th>

                            </tr>

                        </thead>


                        <tbody>

                            <tr
                                v-for="applicant in applicants"
                                :key="applicant.id"
                                class="applicant-row"
                            >

                                <!-- Applicant -->

                                <td>

                                    <div class="applicant-info">

                                        <div class="applicant-avatar">

                                            {{
                                                applicant.name
                                                    ?.charAt(0)
                                                    ?.toUpperCase()
                                            }}

                                        </div>

                                        <div>

                                            <strong>
                                                {{ applicant.name }}
                                            </strong>

                                            <small>
                                                Job Applicant
                                            </small>

                                        </div>

                                    </div>

                                </td>


                                <!-- College -->

                                <td>

                                    <span class="college-name">

                                        <i class="bi bi-mortarboard-fill"></i>

                                        {{ applicant.college }}

                                    </span>

                                </td>


                                <!-- Status -->

                                <td>

                                    <span
                                        class="status-badge"
                                        :class="statusClass(applicant.status)"
                                    >

                                        <i
                                            :class="
                                                statusIcon(
                                                    applicant.status
                                                )
                                            "
                                        ></i>

                                        {{ applicant.status }}

                                    </span>

                                </td>

                            </tr>

                        </tbody>

                    </table>

                </div>


                <!-- Empty State -->

                <div
                    v-if="applicants.length === 0"
                    class="empty-state"
                >

                    <i class="bi bi-people"></i>

                    <h5>
                        No applicants yet
                    </h5>

                    <p>
                        Applications from students will appear here.
                    </p>

                </div>

            </div>

        </main>

    </div>

</template>


<script setup>

import { ref, onMounted } from "vue"
import axios from "axios"

import Navbar from "@/components/Navbar.vue"
import CompSlidebar from "@/components/CompSlidebar.vue"


/* =========================
   AUTH TOKEN
========================= */

const token = localStorage.getItem("companytoken")


/* =========================
   STATE
========================= */

const company = ref({})

const cards = ref({
    active_jobs: 0,
    applications: 0,
    interviews: 0,
    selected: 0
})

const applicants = ref([])


/* =========================
   FETCH DASHBOARD
========================= */

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

    } catch (error) {

        console.log(error)

    }

}


/* =========================
   STATUS CLASS
========================= */

const statusClass = (status) => {

    switch (status) {

        case "Selected":
            return "status-selected"

        case "Interview":
            return "status-interview"

        case "Rejected":
            return "status-rejected"

        default:
            return "status-pending"

    }

}


/* =========================
   STATUS ICON
========================= */

const statusIcon = (status) => {

    switch (status) {

        case "Selected":
            return "bi bi-check-circle-fill"

        case "Interview":
            return "bi bi-calendar-check-fill"

        case "Rejected":
            return "bi bi-x-circle-fill"

        default:
            return "bi bi-clock-fill"

    }

}


/* =========================
   LOAD DASHBOARD
========================= */

onMounted(() => {

    fetchDashboard()

})

</script>


<style scoped>

/* =====================================================
   MAIN DASHBOARD
===================================================== */

.dashboard {

    min-height: 100vh;

    background: #f6f8fc;

}


.dashboard-content {

    margin-left: 260px;

    width: calc(100% - 260px);

    min-height: 100vh;

    padding: 30px;

    box-sizing: border-box;

    transition: all 0.3s ease;

}


/* =====================================================
   WELCOME BANNER
===================================================== */

.welcome-banner {

    position: relative;

    overflow: hidden;

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 35px 40px;

    margin-bottom: 30px;

    border-radius: 20px;

    color: white;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #4f46e5,
            #7c3aed
        );

}


.welcome-content {

    position: relative;

    z-index: 2;

}


.welcome-small {

    margin: 0 0 5px;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1.5px;

    opacity: .8;

}


.welcome-banner h1 {

    margin: 0;

    font-size: 30px;

    font-weight: 700;

}


.welcome-description {

    max-width: 620px;

    margin: 10px 0 15px;

    color: rgba(255,255,255,.85);

    font-size: 14px;

}


.company-email {

    display: inline-flex;

    align-items: center;

    gap: 8px;

    padding: 8px 14px;

    border-radius: 30px;

    background: rgba(255,255,255,.15);

    font-size: 13px;

}


.welcome-icon {

    position: relative;

    z-index: 2;

    width: 105px;

    height: 105px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    background: rgba(255,255,255,.15);

    font-size: 50px;

}


.welcome-banner::after {

    content: "";

    position: absolute;

    width: 230px;

    height: 230px;

    right: 40px;

    bottom: -140px;

    border-radius: 50%;

    background: rgba(255,255,255,.08);

}


/* =====================================================
   STATISTICS
===================================================== */

.statistics-row {

    margin-bottom: 35px;

}


.stat-card {

    position: relative;

    overflow: hidden;

    display: flex;

    align-items: center;

    min-height: 145px;

    padding: 24px;

    border-radius: 18px;

    background: white;

    box-shadow:
        0 5px 20px rgba(0,0,0,.06);

    transition:
        transform .25s ease,
        box-shadow .25s ease;

}


.stat-card:hover {

    transform: translateY(-6px);

    box-shadow:
        0 12px 30px rgba(0,0,0,.12);

}


.stat-icon {

    width: 58px;

    height: 58px;

    display: flex;

    align-items: center;

    justify-content: center;

    flex-shrink: 0;

    margin-right: 18px;

    border-radius: 15px;

    font-size: 24px;

}


.stat-content p {

    margin: 0 0 5px;

    color: #64748b;

    font-size: 14px;

    font-weight: 500;

}


.stat-content h2 {

    margin: 0;

    color: #111827;

    font-size: 30px;

    font-weight: 700;

}


.stat-decoration {

    position: absolute;

    right: -30px;

    bottom: -35px;

    width: 110px;

    height: 110px;

    border-radius: 50%;

    opacity: .08;

}


/* Blue */

.card-blue .stat-icon {

    background: #dbeafe;

    color: #2563eb;

}


.card-blue .stat-decoration {

    background: #2563eb;

}


/* Purple */

.card-purple .stat-icon {

    background: #ede9fe;

    color: #7c3aed;

}


.card-purple .stat-decoration {

    background: #7c3aed;

}


/* Orange */

.card-orange .stat-icon {

    background: #fef3c7;

    color: #d97706;

}


.card-orange .stat-decoration {

    background: #d97706;

}


/* Green */

.card-green .stat-icon {

    background: #dcfce7;

    color: #16a34a;

}


.card-green .stat-decoration {

    background: #16a34a;

}


/* =====================================================
   SECTION HEADER
===================================================== */

.section-header {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-bottom: 18px;

}


.section-subtitle {

    margin: 0;

    color: #6366f1;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1.5px;

}


.section-header h3 {

    margin: 4px 0 0;

    color: #111827;

    font-size: 24px;

    font-weight: 700;

}


.view-all-btn {

    display: inline-flex;

    align-items: center;

    gap: 6px;

    border: none;

    background: transparent;

    color: #4f46e5;

    font-size: 13px;

    font-weight: 600;

    cursor: pointer;

    transition: .2s;

}


.view-all-btn:hover {

    color: #312e81;

    transform: translateX(3px);

}


/* =====================================================
   APPLICANTS TABLE
===================================================== */

.applicants-container {

    overflow: hidden;

    background: white;

    border-radius: 18px;

}


.applicants-table {

    margin: 0;

    min-width: 600px;

}


.applicants-table thead {

    background: #f8fafc;

}


.applicants-table th {

    padding: 17px 20px;

    border: none;

    color: #64748b;

    font-size: 12px;

    font-weight: 600;

    text-transform: uppercase;

}


.applicants-table td {

    padding: 17px 20px;

    border-color: #f1f5f9;

    vertical-align: middle;

}


.applicant-row {

    transition: background .2s ease;

}


.applicant-row:hover {

    background: #f8faff;

}


/* =====================================================
   APPLICANT INFO
===================================================== */

.applicant-info {

    display: flex;

    align-items: center;

    gap: 12px;

}


.applicant-avatar {

    width: 42px;

    height: 42px;

    display: flex;

    align-items: center;

    justify-content: center;

    flex-shrink: 0;

    border-radius: 12px;

    background: #eef2ff;

    color: #4f46e5;

    font-size: 16px;

    font-weight: 700;

}


.applicant-info strong {

    display: block;

    color: #1e293b;

    font-size: 14px;

}


.applicant-info small {

    display: block;

    margin-top: 3px;

    color: #94a3b8;

    font-size: 11px;

}


/* =====================================================
   COLLEGE
===================================================== */

.college-name {

    display: inline-flex;

    align-items: center;

    gap: 7px;

    color: #475569;

    font-size: 13px;

}


.college-name i {

    color: #6366f1;

}


/* =====================================================
   STATUS
===================================================== */

.status-badge {

    display: inline-flex;

    align-items: center;

    gap: 6px;

    padding: 6px 11px;

    border-radius: 20px;

    font-size: 11px;

    font-weight: 600;

}


.status-selected {

    background: #dcfce7;

    color: #15803d;

}


.status-interview {

    background: #fef3c7;

    color: #b45309;

}


.status-rejected {

    background: #fee2e2;

    color: #dc2626;

}


.status-pending {

    background: #e2e8f0;

    color: #475569;

}


/* =====================================================
   EMPTY STATE
===================================================== */

.empty-state {

    padding: 60px 20px;

    text-align: center;

    color: #94a3b8;

}


.empty-state i {

    display: block;

    margin-bottom: 12px;

    font-size: 45px;

}


.empty-state h5 {

    margin-bottom: 5px;

    color: #475569;

}


.empty-state p {

    margin: 0;

    font-size: 13px;

}


/* =====================================================
   TABLET
===================================================== */

@media (max-width: 991px) {

    .dashboard-content {

        margin-left: 220px;

        width: calc(100% - 220px);

        padding: 20px;

    }


    .welcome-banner {

        padding: 30px;

    }


    .welcome-banner h1 {

        font-size: 26px;

    }


    .welcome-icon {

        width: 90px;

        height: 90px;

        font-size: 42px;

    }

}


/* =====================================================
   MOBILE
===================================================== */

@media (max-width: 767px) {

    .dashboard-content {

        margin-left: 80px;

        width: calc(100% - 80px);

        padding: 15px;

    }


    .welcome-banner {

        padding: 22px;

        border-radius: 16px;

    }


    .welcome-banner h1 {

        font-size: 21px;

    }


    .welcome-description {

        font-size: 12px;

    }


    .welcome-icon {

        display: none;

    }


    .company-email {

        font-size: 11px;

    }


    .stat-card {

        min-height: 120px;

        padding: 18px;

    }


    .stat-icon {

        width: 48px;

        height: 48px;

        font-size: 20px;

    }


    .stat-content h2 {

        font-size: 24px;

    }


    .section-header {

        align-items: flex-end;

    }


    .section-header h3 {

        font-size: 20px;

    }


    .view-all-btn {

        font-size: 11px;

    }


    .applicants-table {

        min-width: 600px;

    }

}


/* =====================================================
   SMALL MOBILE
===================================================== */

@media (max-width: 480px) {

    .dashboard-content {

        margin-left: 80px;

        width: calc(100% - 80px);

        padding: 10px;

    }


    .welcome-banner {

        padding: 18px;

    }


    .welcome-banner h1 {

        font-size: 18px;

    }


    .section-header {

        flex-direction: column;

        align-items: flex-start;

        gap: 6px;

    }


    .stat-card {

        min-height: 105px;

        padding: 14px;

    }

}


/* =====================================================
   DARK THEME
===================================================== */

.dark-theme .dashboard {

    background: #0d1117;

}


.dark-theme .welcome-banner {

    background:
        linear-gradient(
            135deg,
            #1e3a8a,
            #3730a3,
            #581c87
        );

}


.dark-theme .stat-card,
.dark-theme .applicants-container {

    background: #1e1e1e;

    color: white;

}


.dark-theme .stat-content h2 {

    color: white;

}


.dark-theme .stat-content p {

    color: #a1a1aa;

}


.dark-theme .section-header h3 {

    color: white;

}


.dark-theme .applicants-table thead {

    background: #181818;

}


.dark-theme .applicants-table th {

    color: #a1a1aa;

}


.dark-theme .applicants-table td {

    border-color: #333;

}


.dark-theme .applicant-info strong {

    color: white;

}


.dark-theme .applicant-row:hover {

    background: #242424;

}


.dark-theme .college-name {

    color: #d1d5db;

}

</style>