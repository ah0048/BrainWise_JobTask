<template>
    <div class="department-list">
      <AppNavbar />
      <div v-for="department in departments" :key="department.id" class="department-card">
        <h3>{{ department.name }} ({{ department.companyName }})</h3> <!-- Show company name here -->
        <div class="button-container">
          <button v-if="userRole === 'admin' || userRole === 'manager'" @click="editDepartment(department)" class="edit-button">Edit</button>
          <button v-if="userRole === 'admin'" @click="deleteDepartment(department)" class="delete-button">Delete</button>
          <button @click="viewDepartment(department)" class="view-button">View</button>
        </div>
      </div>
  
      <!-- View Modal -->
      <div v-if="showViewModal" class="modal">
        <div class="modal-content">
          <h3>{{ selectedDepartment.name }}</h3>
          <p><strong>Company:</strong> {{ selectedDepartment.companyName }}</p> <!-- Show company name here -->
          <p><strong>Number of Employees:</strong> {{ selectedDepartment.num_employees }}</p>
          <button @click="closeModal('view')">Close</button>
        </div>
      </div>
  
      <!-- Edit Modal -->
      <div v-if="showEditModal" class="modal">
        <div class="modal-content">
          <h3>Edit Department</h3>
          <form @submit.prevent="updateDepartment">
            <div class="form-group">
              <label for="departmentName">Department Name</label>
              <input
                type="text"
                id="departmentName"
                v-model="departmentName"
                placeholder="Enter department name"
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
    name: "DepartmentPage",
    components: {
      AppNavbar,
    },
    data() {
      return {
        departments: [],
        userRole: localStorage.getItem("userRole"),
        showViewModal: false,
        showEditModal: false,
        selectedDepartment: null,
        departmentName: "",
      };
    },
    created() {
      this.fetchDepartments();
    },
    methods: {
      async fetchDepartments() {
        const token = localStorage.getItem("token");
        const response = await fetch(`${process.env.VUE_APP_API_URL}/departments/`, {
          headers: {
            "Authorization": `Token ${token}`,
          },
        });
        const data = await response.json();
        
        // Fetch company names for each department
        for (let department of data) {
          const companyResponse = await fetch(`${process.env.VUE_APP_API_URL}/companies/${department.company}/`, {
            headers: {
              "Authorization": `Token ${token}`,
            },
          });
          const companyData = await companyResponse.json();
          department.companyName = companyData.name;  // Add company name to department
        }
        
        this.departments = data;
      },
      viewDepartment(department) {
        this.selectedDepartment = department;
        this.showViewModal = true;
      },
      closeModal(modalType) {
        if (modalType === 'view') {
          this.showViewModal = false;
        } else if (modalType === 'edit') {
          this.showEditModal = false;
        }
      },
      editDepartment(department) {
        this.selectedDepartment = department;
        this.departmentName = department.name;
        this.showEditModal = true;
      },
      async updateDepartment() {
        const token = localStorage.getItem("token");
        const response = await fetch(`${process.env.VUE_APP_API_URL}/departments/${this.selectedDepartment.id}/update/`, {
          method: "PUT",
          headers: {
            "Authorization": `Token ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ company: this.selectedDepartment.company,
                                    name: this.departmentName 
                                }),
        });
  
        if (response.ok) {
          alert('Department updated successfully');
          this.fetchDepartments();  // Refresh the list after update
          this.closeModal('edit');
        }
      },
      async deleteDepartment(department) {
        if (confirm(`Are you sure you want to delete ${department.name}?`)) {
          const response = await fetch(`${process.env.VUE_APP_API_URL}/departments/${department.id}/delete/`, {
            method: "DELETE",
            headers: {
              "Authorization": `Token ${localStorage.getItem("token")}`,
            },
          });
  
          if (response.ok) {
            alert('Department deleted successfully');
            this.fetchDepartments();  // Refresh the list after deletion
          }
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .department-card {
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
  