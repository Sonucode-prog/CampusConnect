import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import LandingPage from '../views/LandingPage.vue'

import AdminDashboard from '../views/AdminDashboard.vue'
import StudentList from '../components/StudentList.vue'
import StudAdminprofile from '@/components/StudAdminprofile.vue'
import CompanyList from '@/components/CompanyList.vue'
import CompanyProfile from '@/components/CompanyProfile.vue'
import AdminManageJobs from '@/components/AdminManageJobs.vue'
import AdminApplicants from '@/components/AdminApplicants.vue'

import CompanyDashboard from '../views/CompanyDashboard.vue'
import CompanyRegister from '../components/CompanyRegister.vue'
import CompProfile from '../components/CompProfile.vue'
import PostJobs from '@/components/PostJobs.vue'
import ManageJobs from '@/components/ManageJobs.vue'
import Applicants from '../components/Applicants.vue'
import ApplicationProfile from '../components/ApplicationProfile.vue'
import CompanyReport from '../components/CompanyReport.vue'


import StudentRegister from '../components/StudentRegister.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import StudentProfile from '@/components/StudentProfile.vue'
import StudEdit from '@/components/StudEdit.vue'
import BrowserJobs from '@/components/BrowserJobs.vue'
import ApplicationPage from '@/components/ApplicationPage.vue'
import ApplicationDetails from '@/components/ApplicationDetails.vue'
import ResumeCard from '@/components/ResumeCard.vue'
import Notification from '@/components/Notification.vue'




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LandingPage,
    },
    
    {
      path: '/AdminDashboard',
      name: 'admin',
      component: () => import('../views/AdminDashboard.vue'),
      // children: [
      //   {
      //     path: '',
      //     name: 'admin-home',
      //     // shows overview inside AdminDashboard's <router-view>
      //     component: () => import('../views/admin/AdminHome.vue'),
      //   },
      //   {
      //     path: 'Companies',
      //     name: 'Admincompanies',
      //     component: () => import('../views/admin/AdminCompanies.vue'),
      //   },
      //   {
      //     path: 'Students',
      //     name: 'Adminstudents',
      //     component: () => import('../views/admin/AdminStudents.vue'),
      //   },
      //   {
      //     path: 'Reports',
      //     name: 'Adminreports',
      //     component: () => import('../views/admin/AdminReports.vue'),
      //   },
      // ],
    },
    {
      path: "/admin/students",
      name: "AdminStudents",
      component: StudentList
    },
    {
      path: "/admin/student/:id",
      name: "AdminStudentProfile",
      component: StudAdminprofile,
      props: true
    },
    {
      path: "/admin/companies",
      name: "AdminCompanies",
      component: CompanyList
    },

    {
      path: "/admin/company/:id",
      name: "AdminCompanyProfile",
      component: CompanyProfile,
      props: true
    },
    {
      path: '/AdminManageJobs',
      name: 'admin-manage-jobs',
      component: () => import('../components/AdminManageJobs.vue')
    },
    {
      path: '/AdminApplicants',
      name:'admin-applicants',
      component: () => import('../components/AdminApplicants.vue')
    },
    {
      path: '/AdminApplicationProfile/:id',
      name: 'admin-applicants-profile',
      component: () => import('../components/AdminApplicationProfile.vue'),
      props: true
    },
    {
      path: '/Login',
      name: 'login',
      component: () => import('../components/Login.vue'),
    },
    {
      path: '/CompanyDashboard',
      name: 'company-dashboard',
      component: () => import('../views/CompanyDashboard.vue'),
    },
    {
      path: '/PostJobs',
      name: '/posting-jobs',
      component: () => import('../components/PostJobs.vue')

    },
    {
      path: '/ManageJobs',
      name: 'manage-jobs',
      component: () => import('../components/ManageJobs.vue')
    },
    {
      path: '/Applicants',
      name:'applicants',
      component: () => import('../components/Applicants.vue')
    },
    {
      path: '/CompanyReport',
      name: 'company-report',
      component: () => import('../components/CompanyReport.vue')
    },
    {
      path: '/ApplicationProfile/:id',
      name: 'applicants-profile',
      component: () => import('../components/ApplicationProfile.vue'),
      props: true
    },

    {
      path: '/CompProfile',
      name: 'comp-profile',
      component: () => import('../components/CompProfile.vue'),
    },
    
    {
      path: '/CompanyRegister',
      name: 'company-register',
      component: () => import('../components/CompanyRegister.vue'),
    },
    {
      path: '/StudentDashboard',
      name: 'student-dashboard',
      component: () => import('../views/StudentDashboard.vue'),
    },
    {
      path: '/BrowserJobs',
      name: 'browser-jobs',
      component: () => import('../components/BrowserJobs.vue'),
    },
    {
      path: '/StudentRegister',
      name: 'student-register',
      component: () => import('../components/StudentRegister.vue'),

    },
    {
      path: '/StudentProfile',
      name: 'student-profile',
      component: () => import('../components/StudentProfile.vue'),
    },
    {
      path: '/StudEdit',
      name: 'stud-edit',
      component: () => import('../components/StudEdit.vue'),
    },
    {
      path: '/ApplicationPage',
      name: 'application-page',
      component: () => import('../components/ApplicationPage.vue'),
    },
    {
      path:"/student/application/:id",
      name:"ApplicationDetails",
      component:ApplicationDetails
    },
    {
      path: '/ResumeCard',
      name: 'resume-card',
      component: () => import('../components/ResumeCard.vue'),
    },
    {
      path: '/Notification',
      name: 'notification',
      component: () => import('../components/Notification.vue'),
    },
    
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
    

  ],
})

export default router
