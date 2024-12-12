<template>
  <div class="home-page">
    <AppNavbar />
    <div class="summary-dashboard">
      <div class="summary-item">
        <h3>Companies</h3>
        <p>{{ numberOfCompanies }}</p>
        <router-link to="/companies">View Companies</router-link>
      </div>
      <div class="summary-item">
        <h3>Departments</h3>
        <p>{{ numberOfDepartments }}</p>
      </div>
      <div class="summary-item">
        <h3>Employees</h3>
        <p>{{ numberOfEmployees }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavbar from "@/components/AppNavbar.vue"; // Importing Navbar component

export default {
  name: "HomePage",
  components: {
    AppNavbar,
  },
  data() {
    return {
      numberOfCompanies: 0,
      numberOfDepartments: 0,
      numberOfEmployees: 0,
    };
  },
  created() {
    this.fetchSummaryData();
  },
  methods: {
    async fetchSummaryData() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          console.error('No token found in localStorage');
          return;
        }

        const addAuthHeader = (fetchUrl) => {
          return fetch(fetchUrl, {
            headers: {
              'Authorization': `Token ${token}`
            }
          });
        };

        const [companies, departments, employees] = await Promise.all([
          addAuthHeader(`${process.env.VUE_APP_API_URL}/companies/`).then((res) => res.json()),
          addAuthHeader(`${process.env.VUE_APP_API_URL}/departments/`).then((res) => res.json()),
          addAuthHeader(`${process.env.VUE_APP_API_URL}/employees/`).then((res) => res.json()),
        ]);

        this.numberOfCompanies = companies.length;
        this.numberOfDepartments = departments.length;
        this.numberOfEmployees = employees.length;
      } catch (error) {
        console.error("Error fetching summary data:", error);
      }
    },
  },
};
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.summary-dashboard {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.summary-item {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  width: 30%;
}

h3 {
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  .summary-dashboard {
    flex-direction: column;
    align-items: center;
  }
  .summary-item {
    width: 100%;
    margin-bottom: 15px;
  }
}
</style>
