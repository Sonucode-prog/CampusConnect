<template>
  <Navbar />

  <div class="dashboard">

    <StudSlidebar />

    <main class="dashboard-content">

      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Browse Jobs</h2>
      </div>

      <div class="card shadow-sm mb-4">

        <div class="card-body">

          <div class="row">

            <div class="col-md-4 mb-2">
              <input type="text" class="form-control" placeholder="Search Job..." v-model="search">
            </div>

            <div class="col-md-4 mb-2">
              <select class="form-select" v-model="typeFilter">
                <option value="">All Job Types</option>
                <option>Full Time</option>
                <option>Internship</option>
                <option>Part Time</option>
                <option>Contract</option>
              </select>
            </div>

            <div class="col-md-4 mb-2">
              <input type="text" class="form-control" placeholder="Location..." v-model="locationFilter">
            </div>

          </div>

        </div>

      </div>

      <div class="row">

        <div class="col-lg-6 mb-4" v-for="job in filteredJobs" :key="job.job_id">

          <div class="card job-card shadow-sm h-100">

            <div class="card-body">

              <div class="d-flex justify-content-between">

                <div>

                  <h4>{{ job.title }}</h4>

                  <h6 class="text-primary">
                    {{ job.company }}
                  </h6>

                </div>

                <span class="badge" :class="job.status == 'Open' ? 'bg-success' : 'bg-danger'">
                  {{ job.status }}
                </span>

              </div>

              <hr>

              <div class="row">

                <div class="col-6 mb-2">
                  <strong>Location</strong>
                  <p>{{ job.location }}</p>
                </div>

                <div class="col-6 mb-2">
                  <strong>Type</strong>
                  <p>{{ job.job_type }}</p>
                </div>

                <div class="col-6 mb-2">
                  <strong>Salary</strong>
                  <p>{{ job.salary }}</p>
                </div>

                <div class="col-6 mb-2">
                  <strong>CGPA</strong>
                  <p>{{ job.cgpa }}</p>
                </div>

                <div class="col-6 mb-2">
                  <strong>Vacancies</strong>
                  <p>{{ job.vacancies }}</p>
                </div>

                <div class="col-6 mb-2">
                  <strong>Deadline</strong>
                  <p>{{ job.deadline }}</p>
                </div>

              </div>

              <p>
                {{ job.description }}
              </p>

              <div class="mt-3">

                <button v-if="job.already_applied" class="btn btn-success w-100" disabled>
                  ✓ Applied
                </button>

                <button v-else-if="job.deadline_passed" class="btn btn-danger w-100" disabled>
                  Deadline Passed
                </button>

                <button v-else-if="job.status == 'Closed'" class="btn btn-secondary w-100" disabled>
                  Job Closed
                </button>

                <button v-else class="btn btn-primary w-100" @click="applyJob(job.job_id)">
                  Apply Now
                </button>

              </div>

            </div>

          </div>

        </div>

        <div v-if="filteredJobs.length == 0" class="text-center mt-5">

          <h4>No Jobs Available</h4>

        </div>

      </div>

    </main>

  </div>

</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"
import Navbar from "@/components/Navbar.vue"
import StudSlidebar from "@/components/StudSidebar.vue"

const token = localStorage.getItem("studenttoken")

const jobs = ref([])
const search = ref("")
const typeFilter = ref("")
const locationFilter = ref("")

const fetchJobs = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:5000/api/student/jobs",{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        jobs.value = response.data
    } catch(error) {
        console.error(error)
    }
}

const filteredJobs = computed(() => {
    return jobs.value.filter(job => {
        const searchMatch = job.title.toLowerCase().includes(search.value.toLowerCase()) || job.company.toLowerCase().includes(search.value.toLowerCase())
        const typeMatch = typeFilter.value=="" || job.job_type===typeFilter.value
        const locationMatch = locationFilter.value=="" || job.location.toLowerCase().includes(locationFilter.value.toLowerCase())
        return searchMatch && typeMatch && locationMatch
    })
})

const applyJob = async(jobId) => {
    try {
        const response = await axios.post(`http://127.0.0.1:5000/api/student/apply/${jobId}`,{},{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })

        alert(response.data.message)

        const job = jobs.value.find(j => j.job_id===jobId)

        if(job){
            job.already_applied = true
        }

    } catch(error) {
        if(error.response){
            alert(error.response.data.message)
        }else{
            alert("Something went wrong.")
        }
    }
}

onMounted(() => {
    fetchJobs()
})
</script>