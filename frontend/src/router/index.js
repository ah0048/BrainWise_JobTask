import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "@/views/LandingPage.vue";
import HomePage from "@/views/HomePage.vue"; // Import HomePage
// import store from "@/store"; // Import Vuex store for role-based route guard

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
      // Check if the user is authenticated (check if token exists in localStorage)
      if (!localStorage.getItem("token")) {
        next({ name: "LandingPage" }); // Redirect to login page if not authenticated
      } else {
        next(); // Proceed to the HomePage if authenticated
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
