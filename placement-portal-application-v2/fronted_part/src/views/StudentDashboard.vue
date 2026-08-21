<template>
	<Navbar />
	<StudSidebar />

	<div class="main-content">
		<div class="container-fluid">

			<!-- Welcome Banner -->
			<div class="welcome-banner shadow-sm mb-4">
				<div class="welcome-text">
					<p class="welcome-small">Student Dashboard</p>

					<h1>
						Welcome back, {{ student.name }} 👋
					</h1>

					<p>
						Stay updated with the latest job opportunities and
						placement activities.
					</p>

					<div class="student-email">
						<i class="bi bi-envelope"></i>
						{{ student.email }}
					</div>
				</div>

				<div class="welcome-icon">
					<i class="bi bi-mortarboard-fill"></i>
				</div>
			</div>


			<!-- Statistics -->
			<div class="row g-4 mb-5">

				<div
					class="col-12 col-sm-6 col-lg-3"
					v-for="(card, index) in cards"
					:key="card.id"
				>
					<div
						class="stat-card"
						:class="'card-color-' + (index + 1)"
					>

						<div class="stat-icon">
							<i
								:class="
									index === 0
										? 'bi bi-briefcase-fill'
										: index === 1
										? 'bi bi-send-fill'
										: index === 2
										? 'bi bi-check-circle-fill'
										: 'bi bi-person-check-fill'
								"
							></i>
						</div>

						<div class="stat-content">
							<p>{{ card.title }}</p>
							<h2>{{ card.value }}</h2>
						</div>

						<div class="stat-decoration"></div>
					</div>
				</div>

			</div>


			<!-- Recent Jobs Header -->
			<div class="section-header">

				<div>
					<p class="section-subtitle">OPPORTUNITIES</p>
					<h3>Recent Jobs</h3>
				</div>

				<button
					@click="$router.push('/BrowserJobs')"
					class="view-all-btn"
				>
					View All Jobs
					<i class="bi bi-arrow-right"></i>
				</button>

			</div>


			<!-- Jobs -->
			<div class="jobs-container shadow-sm">

				<div class="table-responsive">

					<table class="table jobs-table">

						<thead>
							<tr>
								<th>Company</th>
								<th>Job Position</th>
								<th>Location</th>
								<th>Deadline</th>
								<th class="text-center">Action</th>
							</tr>
						</thead>

						<tbody>

							<template
								v-for="job in jobs"
								:key="job.id"
							>

								<tr
									v-if="job.approve_status === 'Approved'"
									class="job-row"
								>

									<td>
										<div class="company-info">
											<div class="company-logo">
												{{ job.company?.charAt(0)?.toUpperCase() }}
											</div>

											<strong>
												{{ job.company }}
											</strong>
										</div>
									</td>

									<td>
										<div class="job-title">
											{{ job.title }}
										</div>

										<small>
											<i class="bi bi-briefcase"></i>
											Job Opportunity
										</small>
									</td>

									<td>
										<span class="location">
											<i class="bi bi-geo-alt-fill"></i>
											{{ job.location }}
										</span>
									</td>

									<td>
										<span class="deadline">
											<i class="bi bi-calendar-event"></i>
											{{ job.deadline }}
										</span>
									</td>

									<td class="text-center">

										<button
											@click="$router.push('/BrowserJobs')"
											class="apply-btn"
										>
											Apply
											<i class="bi bi-arrow-right"></i>
										</button>

									</td>

								</tr>

							</template>

						</tbody>

					</table>

				</div>

				<!-- Empty Jobs -->
				<div
					v-if="
						jobs.filter(
							job => job.approve_status === 'Approved'
						).length === 0
					"
					class="empty-state"
				>

					<i class="bi bi-briefcase"></i>

					<h5>No jobs available</h5>

					<p>
						New job opportunities will appear here.
					</p>

				</div>

			</div>

		</div>
	</div>
</template>


<style scoped>

/* =========================
   MAIN CONTENT
========================= */

.main-content {
    margin-left: 260px;
    width: calc(100% - 260px);

    padding: 30px;
    min-height: 100vh;

    background: #f6f8fc;

    transition: all 0.3s ease;

    box-sizing: border-box;
}


/* =========================
   WELCOME BANNER
========================= */

.welcome-banner {
	position: relative;
	overflow: hidden;

	display: flex;
	align-items: center;
	justify-content: space-between;

	padding: 35px 40px;

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

.welcome-small {
	margin-bottom: 5px;

	font-size: 13px;
	font-weight: 600;

	letter-spacing: 1.5px;

	text-transform: uppercase;

	opacity: 0.8;
}

.welcome-banner h1 {
	margin: 0;

	font-size: 32px;

	font-weight: 700;
}

.welcome-banner p {
	margin: 10px 0 15px;

	max-width: 600px;

	color: rgba(255,255,255,0.85);
}

.student-email {
	display: inline-flex;
	align-items: center;
	gap: 8px;

	padding: 8px 14px;

	border-radius: 30px;

	background: rgba(255,255,255,0.15);

	font-size: 14px;
}

.welcome-icon {
	position: relative;
	z-index: 2;

	width: 110px;
	height: 110px;

	display: flex;
	align-items: center;
	justify-content: center;

	border-radius: 50%;

	background: rgba(255,255,255,0.15);

	font-size: 55px;
}

.welcome-banner::after {
	content: "";

	position: absolute;

	width: 220px;
	height: 220px;

	right: 40px;
	bottom: -130px;

	border-radius: 50%;

	background: rgba(255,255,255,0.08);
}


/* =========================
   STAT CARDS
========================= */

.stat-card {
	position: relative;

	overflow: hidden;

	display: flex;
	align-items: center;

	min-height: 145px;

	padding: 25px;

	border-radius: 18px;

	background: white;

	box-shadow:
		0 5px 20px rgba(0,0,0,0.06);

	transition:
		transform 0.25s ease,
		box-shadow 0.25s ease;
}

.stat-card:hover {
	transform: translateY(-6px);

	box-shadow:
		0 12px 30px rgba(0,0,0,0.12);
}

.stat-icon {
	width: 60px;
	height: 60px;

	display: flex;
	align-items: center;
	justify-content: center;

	border-radius: 15px;

	font-size: 25px;

	margin-right: 18px;
}

.stat-content p {
	margin: 0 0 5px;

	color: #6b7280;

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

	opacity: 0.08;
}


/* Card Colors */

.card-color-1 .stat-icon {
	background: #dbeafe;
	color: #2563eb;
}

.card-color-1 .stat-decoration {
	background: #2563eb;
}

.card-color-2 .stat-icon {
	background: #ede9fe;
	color: #7c3aed;
}

.card-color-2 .stat-decoration {
	background: #7c3aed;
}

.card-color-3 .stat-icon {
	background: #dcfce7;
	color: #16a34a;
}

.card-color-3 .stat-decoration {
	background: #16a34a;
}

.card-color-4 .stat-icon {
	background: #fef3c7;
	color: #d97706;
}

.card-color-4 .stat-decoration {
	background: #d97706;
}


/* =========================
   SECTION HEADER
========================= */

.section-header {
	display: flex;

	align-items: center;
	justify-content: space-between;

	margin-bottom: 18px;
}

.section-subtitle {
	margin: 0;

	color: #6366f1;

	font-size: 12px;
	font-weight: 700;

	letter-spacing: 1.5px;
}

.section-header h3 {
	margin: 4px 0 0;

	color: #111827;

	font-size: 25px;
	font-weight: 700;
}

.view-all-btn {
	border: none;

	background: transparent;

	color: #4f46e5;

	font-weight: 600;

	cursor: pointer;

	transition: 0.2s;
}

.view-all-btn:hover {
	color: #312e81;
}


/* =========================
   JOB TABLE
========================= */

.jobs-container {
	overflow: hidden;

	background: white;

	border-radius: 18px;
}

.jobs-table {
	margin: 0;

	min-width: 850px;
}

.jobs-table thead {
	background: #f8fafc;
}

.jobs-table th {
	padding: 18px;

	border: none;

	color: #64748b;

	font-size: 13px;

	font-weight: 600;

	text-transform: uppercase;
}

.jobs-table td {
	padding: 18px;

	border-color: #f1f5f9;

	vertical-align: middle;
}

.job-row {
	transition: background 0.2s ease;
}

.job-row:hover {
	background: #f8faff;
}


/* Company */

.company-info {
	display: flex;
	align-items: center;

	gap: 12px;
}

.company-logo {
	width: 42px;
	height: 42px;

	display: flex;
	align-items: center;
	justify-content: center;

	border-radius: 12px;

	background: #eef2ff;

	color: #4f46e5;

	font-size: 17px;
	font-weight: 700;
}

.company-info strong {
	color: #1e293b;
}


/* Job */

.job-title {
	color: #1e293b;

	font-weight: 600;
}

.job-title + small {
	display: block;

	margin-top: 5px;

	color: #94a3b8;
}


/* Location */

.location {
	color: #475569;

	font-size: 14px;
}

.location i {
	margin-right: 5px;

	color: #6366f1;
}


/* Deadline */

.deadline {
	color: #475569;

	font-size: 14px;
}

.deadline i {
	margin-right: 5px;

	color: #f59e0b;
}


/* Apply Button */

.apply-btn {
	display: inline-flex;

	align-items: center;
	gap: 7px;

	padding: 8px 16px;

	border: none;

	border-radius: 8px;

	background: #4f46e5;

	color: white;

	font-size: 13px;
	font-weight: 600;

	transition: all 0.2s ease;
}

.apply-btn:hover {
	background: #3730a3;

	transform: translateY(-2px);

	box-shadow: 0 5px 12px rgba(79,70,229,0.25);
}


/* =========================
   EMPTY STATE
========================= */

.empty-state {
	padding: 60px 20px;

	text-align: center;

	color: #94a3b8;
}

.empty-state i {
	font-size: 45px;

	margin-bottom: 10px;
}

.empty-state h5 {
	color: #475569;
}

.empty-state p {
	margin: 0;
}


/* =========================
   TABLET
========================= */

@media (max-width: 991px) {

.main-content {
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

/* =========================
   MOBILE
========================= */

@media (max-width: 767px) {

    .main-content {
        margin-left: 80px;
        width: calc(100% - 80px);

        padding: 15px;

        box-sizing: border-box;
    }

    .welcome-banner {
        padding: 25px;
        border-radius: 16px;
    }

    .welcome-banner h1 {
        font-size: 22px;
    }

    .welcome-banner p {
        font-size: 13px;
    }

    .welcome-icon {
        display: none;
    }

    .student-email {
        font-size: 12px;
    }

    .stat-card {
        min-height: 125px;
        padding: 20px;
    }

    .stat-icon {
        width: 50px;
        height: 50px;
        font-size: 21px;
    }

    .stat-content h2 {
        font-size: 25px;
    }

    .section-header {
        align-items: flex-end;
    }

    .section-header h3 {
        font-size: 21px;
    }

    .view-all-btn {
        font-size: 12px;
    }

    .jobs-table {
        min-width: 700px;
    }
}


/* =========================
   SMALL MOBILE
========================= */

@media (max-width: 480px) {

    .main-content {
        margin-left: 80px;
        width: calc(100% - 80px);

        padding: 10px;

        box-sizing: border-box;
    }

    .welcome-banner {
        padding: 20px;
    }

    .welcome-banner h1 {
        font-size: 20px;
    }

    .section-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

    .stat-card {
        min-height: 110px;
    }
}
</style>


<script setup>

import Navbar from "@/components/Navbar.vue"
import StudSidebar from "@/components/StudSidebar.vue"

import { ref, onMounted } from "vue"
import axios from "axios"


const student = ref({})
const jobs = ref([])
const cards = ref([])


onMounted(async () => {

	const token = localStorage.getItem("studenttoken")

	try {

		const res = await axios.get(
			`${import.meta.env.VITE_API_URL}/api/student/dashboard`,
			{
				headers: {
					Authorization: `Bearer ${token}`
				}
			}
		)

		student.value = res.data.student

		jobs.value = res.data.jobs

		cards.value = res.data.cards

	} catch (error) {

		console.log(error)
		console.log(error.response)

	}

})

</script>