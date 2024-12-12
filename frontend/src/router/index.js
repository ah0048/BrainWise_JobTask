import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "@/views/LandingPage.vue";
import HomePage from "@/views/HomePage.vue"; 
import CompanyPage from "@/views/CompanyPage.vue"; // Import CompanyPage

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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
