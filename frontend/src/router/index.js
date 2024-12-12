import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "@/views/LandingPage.vue";
import HomePage from "@/views/HomePage.vue"; 
import CompanyPage from "@/views/CompanyPage.vue"; // Import CompanyPage
import DepartmentPage from "@/views/DepartmentPage.vue"; // Import DepartmentPage
import EmployeesPage from "@/views/EmployeesPage.vue";
import UserAccountPage from "@/views/UserAccountPage.vue";

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/home",
    name: "HomePage",
    component: HomePage,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem("token")) {
        next({ name: "LandingPage" });
      } else {
        next();
      }
    },
  },
  {
    path: "/companies",
    name: "CompanyPage",
    component: CompanyPage,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem("token")) {
        next({ name: "LandingPage" });
      } else {
        next();
      }
    },
  },
  {
    path: "/departments",
    name: "DepartmentPage",
    component: DepartmentPage,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem("token")) {
        next({ name: "LandingPage" });
      } else {
        next();
      }
    },
  },
  {
    path: "/account",
    name: "UserAccountPage",
    component: UserAccountPage,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem("token")) {
        next({ name: "LandingPage" });
      } else {
        next();
      }
    },
  },
  {
    path: "/employees",
    name: "EmployeesPage",
    component: EmployeesPage,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem("token")) {
        next({ name: "LandingPage" });
      } else {
        next();
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
