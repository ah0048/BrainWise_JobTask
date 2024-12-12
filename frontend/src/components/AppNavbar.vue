<template>
  <div class="navbar">
    <div class="nav-links">
      <router-link to="/home" class="nav-item">Home</router-link>
      <router-link to="/companies" class="nav-item">Companies</router-link>
      <router-link to="/departments" class="nav-item">Departments</router-link>
      <router-link to="/employees" class="nav-item">Employees</router-link>
    </div>
    <div class="user-actions">
      <router-link to="/account" class="user-account">My Account</router-link> <!-- Added User Account link -->
      <span class="role">{{ userRole }}</span>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppNavbar",
  data() {
    return {
      userRole: localStorage.getItem("userRole"), // Get the user role from localStorage
    };
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("userRole");
      this.$router.push({ name: "LandingPage" }); // Redirect to login page
    },
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  padding: 15px 30px;
  border-radius: 8px;
  background-color: #4f46e5; /* Darker blue */
  color: white;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 30px;
}

.nav-item {
  text-decoration: none; /* Remove underline */
  color: white;
  font-size: 1rem;
  transition: color 0.3s ease;
}

.nav-item:hover {
  color: #ffeb3b; /* Highlight on hover */
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-account {
  text-decoration: none; /* Remove underline */
  color: white;
  font-size: 1rem;
  transition: color 0.3s ease;
}

.user-account:hover {
  color: #ffeb3b; /* Highlight on hover */
}

button {
  padding: 8px 16px;
  font-size: 1rem;
  color: #fff;
  background-color: #e53e3e;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #c53030; /* Darker red on hover */
}

.role {
  font-size: 1rem;
  color: white;
}
</style>
