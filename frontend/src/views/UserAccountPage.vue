<template>
    <div class="user-account">
      <AppNavbar />
      <div class="account-details">
        <h2>My Account</h2>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Role:</strong> {{ user.role }}</p>
        <button @click="openEditModal">Edit</button>
      </div>
  
      <!-- Edit Modal -->
      <div v-if="showEditModal" class="modal">
        <div class="modal-content">
          <h3>Edit Account</h3>
          <form @submit.prevent="updateAccount">
            <div class="form-group">
              <label for="username">Username</label>
              <input type="text" id="username" v-model="form.username" required />
            </div>
            <div class="form-group">
              <label for="email">Email</label>
              <input type="email" id="email" v-model="form.email" required />
            </div>
            <div class="form-group">
              <label for="newPassword">New Password</label>
              <input
                type="password"
                id="newPassword"
                v-model="form.newPassword"
              />
            </div>
            <div class="form-group">
              <label for="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                v-model="form.confirmPassword"
              />
            </div>
            <p v-if="passwordError" class="error">{{ passwordError }}</p>
            <button type="submit">Save Changes</button>
            <button @click="closeEditModal">Cancel</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import AppNavbar from "@/components/AppNavbar.vue";
  
  export default {
    name: "UserAccountPage",
    components: {
      AppNavbar,
    },
    data() {
      return {
        user: {}, // User details
        form: {
          username: "",
          email: "",
          newPassword: "",
          confirmPassword: "",
        },
        passwordError: "",
        showEditModal: false,
      };
    },
    created() {
      this.fetchUserDetails();
    },
    methods: {
      async fetchUserDetails() {
        try {
          const userId = localStorage.getItem("userId");
          const token = localStorage.getItem("token");
          const response = await fetch(
            `${process.env.VUE_APP_API_URL}/users/${userId}/`,
            {
              headers: {
                Authorization: `Token ${token}`,
              },
            }
          );
          const data = await response.json();
          this.user = data;
          this.form.username = data.username;
          this.form.email = data.email;
        } catch (error) {
          console.error("Error fetching user details:", error);
        }
      },
      openEditModal() {
        this.showEditModal = true;
      },
      closeEditModal() {
        this.showEditModal = false;
        this.passwordError = "";
        this.form.newPassword = "";
        this.form.confirmPassword = "";
      },
      async updateAccount() {
        if (
          this.form.newPassword &&
          this.form.newPassword !== this.form.confirmPassword
        ) {
          this.passwordError = "Passwords do not match.";
          return;
        }
  
        try {
          const userId = localStorage.getItem("userId");
          const token = localStorage.getItem("token");
          const response = await fetch(
            `${process.env.VUE_APP_API_URL}/users/${userId}/update/`,
            {
              method: "PUT",
              headers: {
                Authorization: `Token ${token}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                username: this.form.username,
                email: this.form.email,
                password: this.form.newPassword || undefined,
              }),
            }
          );
  
          if (response.ok) {
            alert("Account updated successfully.");
            this.fetchUserDetails(); // Refresh details
            this.closeEditModal();
          } else {
            alert("Error updating account.");
          }
        } catch (error) {
          console.error("Error updating account:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .user-account {
    padding: 20px;
  }
  
  .account-details {
    background: #f4f4f4;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }
  
  button {
    margin-top: 10px;
    padding: 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(0, 0, 0, 0.5);
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .error {
    color: red;
    font-size: 0.9rem;
  }
  </style>
  