<template>
  <div class="company-list">
    <AppNavbar />
    <div v-for="company in companies" :key="company.id" class="company-card">
      <h3>{{ company.name }}</h3>
      <div class="button-container">
        <button v-if="userRole === 'admin' || userRole === 'manager'" @click="editCompany(company)" class="edit-button">Edit</button>
        <button v-if="userRole === 'admin'" @click="deleteCompany(company)" class="delete-button">Delete</button>
        <button @click="viewCompany(company)" class="view-button">View</button>
      </div>
    </div>

    <!-- View Modal -->
    <div v-if="showViewModal" class="modal">
      <div class="modal-content">
        <h3>{{ selectedCompany.name }}</h3>
        <p><strong>Number of Departments:</strong> {{ selectedCompany.num_departments }}</p>
        <p><strong>Number of Employees:</strong> {{ selectedCompany.num_employees }}</p>
        <button @click="closeModal('view')">Close</button>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h3>Edit Company</h3>
        <form @submit.prevent="updateCompany">
          <div class="form-group">
            <label for="companyName">Company Name</label>
            <input
              type="text"
              id="companyName"
              v-model="companyName"
              placeholder="Enter company name"
              required
            />
          </div>
          <p class="info-message">Other attributes are updated dynamically and cannot be edited.</p>
          <button type="submit">Save Changes</button>
          <button @click="closeModal('edit')">Cancel</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavbar from "@/components/AppNavbar.vue";

export default {
  name: "CompanyPage",
  components: {
    AppNavbar,
  },
  data() {
    return {
      companies: [],
      userRole: localStorage.getItem("userRole"),
      showViewModal: false,
      showEditModal: false,
      selectedCompany: null,
      companyName: "",
    };
  },
  created() {
    this.fetchCompanies();
  },
  methods: {
    async fetchCompanies() {
      const token = localStorage.getItem("token");
      const response = await fetch(`${process.env.VUE_APP_API_URL}/companies/`, {
        headers: {
          "Authorization": `Token ${token}`,
        },
      });
      const data = await response.json();
      this.companies = data;
    },
    viewCompany(company) {
      this.selectedCompany = company;
      this.showViewModal = true;
    },
    closeModal(modalType) {
      if (modalType === 'view') {
        this.showViewModal = false;
      } else if (modalType === 'edit') {
        this.showEditModal = false;
      }
    },
    editCompany(company) {
      this.selectedCompany = company;
      this.companyName = company.name;
      this.showEditModal = true;
    },
    async updateCompany() {
      const token = localStorage.getItem("token");
      const response = await fetch(`${process.env.VUE_APP_API_URL}/companies/${this.selectedCompany.id}/update/`, {
        method: "PUT",
        headers: {
          "Authorization": `Token ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: this.companyName }),
      });

      if (response.ok) {
        alert('Company updated successfully');
        this.fetchCompanies();  // Refresh the list after update
        this.closeModal('edit');
      }
    },
    async deleteCompany(company) {
      if (confirm(`Are you sure you want to delete ${company.name}?`)) {
        const response = await fetch(`${process.env.VUE_APP_API_URL}/companies/${company.id}/delete/`, {
          method: "DELETE",
          headers: {
            "Authorization": `Token ${localStorage.getItem("token")}`,
          },
        });

        if (response.ok) {
          alert('Company deleted successfully');
          this.fetchCompanies();  // Refresh the list after deletion
        }
      }
    },
  },
};
</script>

<style scoped>
.company-card {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  margin-bottom: 10px;
  background-color: #f4f4f4;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.button-container {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 16px;
  font-size: 1rem;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-button {
  background-color: #e53e3e;
}

.view-button {
  background-color: #3498db;
}

.edit-button {
  background-color: #f39c12;
}

button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

/* Modal styles */
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
  max-width: 500px;
  width: 100%;
}

.form-group {
  margin-bottom: 20px;
}

input {
  padding: 10px;
  width: 100%;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #3b82f6;
}

.info-message {
  font-size: 0.9rem;
  color: #555;
}
</style>
