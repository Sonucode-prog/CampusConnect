<template>
    <Navbar />
    <div class="dashboard">
        <StudentSidebar />
        <main class="dashboard-content">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Notifications</h2>
                <button class="btn btn-primary" @click="markAllRead">
                    Mark All Read
                </button>
            </div>

            <div v-if="notifications.length==0" class="card shadow-sm">
                <div class="card-body text-center py-5">
                    <h5>No Notifications</h5>
                    <p class="text-muted">You're all caught up!</p>
                </div>
            </div>

            <div v-for="notification in notifications" :key="notification.id" class="card shadow-sm mb-3 notification-card" :class="{unread:!notification.read_status}">
                <div class="card-body d-flex justify-content-between align-items-start">
                    <div>
                        <h6 class="mb-2">
                            <i class="bi bi-bell-fill text-primary me-2"></i>
                            Notification
                        </h6>
                        <p class="mb-2">{{ notification.message }}</p>
                        <small class="text-muted">{{ notification.created_at }}</small>
                    </div>

                    <div>
                        <button v-if="!notification.read_status" class="btn btn-success btn-sm me-2" @click="markRead(notification.id)">
                            Read
                        </button>

                        <button class="btn btn-danger btn-sm" @click="deleteNotification(notification.id)">
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref,onMounted } from "vue"
import axios from "axios"
import Navbar from "@/components/Navbar.vue"
import StudentSidebar from "@/components/StudSidebar.vue"

const token=localStorage.getItem("studenttoken")
const notifications=ref([])

const fetchNotifications=async()=>{
    try{
        const response=await axios.get("http://127.0.0.1:5000/api/student/notifications",{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        notifications.value=response.data
    }catch(error){
        console.error(error)
    }
}

const markRead=async(id)=>{
    try{
        await axios.put(`http://127.0.0.1:5000/api/student/notifications/${id}`,{},{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        fetchNotifications()
    }catch(error){
        console.error(error)
    }
}

const deleteNotification=async(id)=>{
    if(!confirm("Delete this notification?")) return
    try{
        await axios.delete(`http://127.0.0.1:5000/api/student/notifications/${id}`,{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        notifications.value=notifications.value.filter(n=>n.id!==id)
    }catch(error){
        console.error(error)
    }
}

const markAllRead=async()=>{
    try{
        await axios.put("http://127.0.0.1:5000/api/student/notifications/read-all",{},{
            headers:{
                Authorization:`Bearer ${token}`
            }
        })
        fetchNotifications()
    }catch(error){
        console.error(error)
    }
}

onMounted(()=>{
    fetchNotifications()
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

.notification-card{
    border-left:5px solid #0d6efd;
    transition:.3s;
}

.notification-card:hover{
    transform:translateY(-3px);
}

.unread{
    border-left:5px solid #ffc107;
}

.dark-theme .notification-card{
    background:#1e1e1e;
    color:white;
    border:1px solid #333;
}

.dark-theme .notification-card p,
.dark-theme .notification-card h6{
    color:white;
}

.dark-theme .text-muted{
    color:#bdbdbd !important;
}
</style>