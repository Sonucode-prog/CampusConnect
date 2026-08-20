<template>
	<Navbar />
	<StudSidebar />
	<div class="main-content">
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-10 p-4">
					<h2>Welcome {{ student.name }}</h2>
					<h2>Email ID : {{ student.email }}</h2>
					<div class="row mt-4">
						<div class="col-md-3" v-for="card in cards" :key="card.id">
							<div class="card shadow">
								<div class="card-body">
									<h6>{{ card.title }}</h6>

									<h2>{{ card.value }}</h2>
								</div>
							</div>
						</div>
					</div>

					<h3 class="mt-5">
						Recent Jobs

					</h3>
					<table class="table table-striped">

						<thead>
							<tr>

								<th>Company</th>
								<th>Job</th>
								<th>Location</th>
								<th>Deadline</th>
								<th>Action</th>
							</tr>
						</thead>

						<tbody v-for="job in jobs" :key="job.id">							
							<tr v-if="job.approve_status == 'Approved'">
								<td>{{ job.company }}</td>
								<td>{{ job.title }}</td>
								<td>{{ job.location }}</td>
								<td>{{ job.deadline }}</td>

								<td>
									<button @click="$router.push('/BrowserJobs')" class="btn btn-primary btn-sm">
										Apply
									</button>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>
</template>
<style>
.main-content {
	margin-left: 260px;
	padding: 20px;
	transition: .3s;
}
</style>

<script setup>
import Navbar from "@/components/Navbar.vue"
import { ref, onMounted } from "vue"
import axios from "axios"
import StudSidebar from "@/components/StudSidebar.vue"


const student = ref({})

const jobs = ref([])

const cards = ref([])

onMounted(async () => {

	const token = localStorage.getItem("studenttoken")
	try {
		const res = await axios.get(`${import.meta.env.VITE_API_URL}/api/student/dashboard`, {

			headers: {
				Authorization: `Bearer ${token}`
			}

		})

		student.value = res.data.student

		jobs.value = res.data.jobs

		cards.value = res.data.cards

	} catch (error) {
		console.log(error)
		console.log(error.response)
	}

})
</script>
