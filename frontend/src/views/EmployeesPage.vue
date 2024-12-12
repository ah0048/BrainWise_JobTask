<template>
  <div class="employee-list">
    <AppNavbar />
    <div class="header">
      <button
        v-if="userRole === 'admin' || userRole === 'manager'"
        @click="openCreateModal"
        class="create-button"
      >
        Create Employee
      </button>
    </div>
    <div v-for="employee in employees" :key="employee.id" class="employee-card">
      <h3>{{ employee.name }} ({{ employee.designation }})</h3>
      <p>Status: {{ employee.status }}</p>
      <div class="button-container">
        <button @click="viewEmployee(employee)" class="view-button">View</button>
        <button
          v-if="userRole === 'admin' || userRole === 'manager'"
          @click="editEmployee(employee)"
          class="edit-button"
        >
          Edit
        </button>
        <button
          v-if="userRole === 'admin' || userRole === 'manager'"
          @click="deleteEmployee(employee)"
          class="delete-button"
        >
          Delete
        </button>
      </div>
    </div>

    <!-- View Modal -->
    <div v-if="showViewModal" class="modal">
      <div class="modal-content">
        <h3>{{ selectedEmployee.name }}</h3>
        <p><strong>Designation:</strong> {{ selectedEmployee.designation }}</p>
        <p><strong>Email:</strong> {{ selectedEmployee.email }}</p>
        <p><strong>Mobile:</strong> {{ selectedEmployee.mobile_number }}</p>
        <p><strong>Address:</strong> {{ selectedEmployee.address }}</p>
        <p><strong>Company:</strong> {{ selectedEmployee.companyName }}</p>
        <p><strong>Department:</strong> {{ selectedEmployee.departmentName }}</p>
        <p><strong>Status:</strong> {{ selectedEmployee.status }}</p>
        <p><strong>Hired On:</strong> {{ selectedEmployee.hired_on }}</p>
        <p><strong>Days Employed:</strong> {{ selectedEmployee.days_employed }}</p>
        <button @click="closeModal('view')">Close</button>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content wider">
        <h3>Edit Employee</h3>
        <form @submit.prevent="updateEmployee">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" v-model="form.name" required />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="form.email" required />
          </div>
          <div class="form-group">
            <label for="mobile_number">Mobile</label>
            <input type="text" id="mobile_number" v-model="form.mobile_number" required />
          </div>
          <div class="form-group">
            <label for="address">Address</label>
            <textarea id="address" v-model="form.address" required></textarea>
          </div>
          <div class="form-group">
            <label for="designation">Designation</label>
            <input type="text" id="designation" v-model="form.designation" required />
          </div>
          <div class="form-group">
            <label for="status">Status</label>
            <select id="status" v-model="form.status">
              <option v-for="status in allowedStatusOptions" :key="status" :value="status">{{ status }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="hired_on">Hired On</label>
            <input type="text" id="hired_on" v-model="form.hired_on" readonly />
          </div>
          <div class="form-group">
            <label for="days_employed">Days Employed</label>
            <input type="text" id="days_employed" v-model="form.days_employed" readonly />
          </div>
          <button type="submit" :disabled="!canEdit">Update</button>
          <button @click="closeModal('edit')">Cancel</button>
        </form>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="modal">
      <div class="modal-content">
        <h3>Create Employee</h3>
        <form @submit.prevent="createEmployee">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" v-model="form.name" required />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="form.email" required />
          </div>
          <div class="form-group">
            <label for="mobile_number">Mobile</label>
            <input type="text" id="mobile_number" v-model="form.mobile_number" required />
          </div>
          <div class="form-group">
            <label for="address">Address</label>
            <textarea id="address" v-model="form.address" required></textarea>
          </div>
          <div class="form-group">
            <label for="designation">Designation</label>
            <input type="text" id="designation" v-model="form.designation" required />
          </div>
          <div class="form-group">
            <label for="company">Company</label>
            <select 
              id="company" 
              v-model="form.company" 
              @change="onCompanyChange" 
              required
            >
              <option value="">Select a Company</option>
              <option 
                v-for="company in companies" 
                :key="company.id" 
                :value="company.id"
              >
                {{ company.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="department">Department</label>
            <select 
              id="department" 
              v-model="form.department" 
              :disabled="!form.company" 
              required
            >
              <option value="">Select a Department</option>
              <option 
                v-for="dept in filteredDepartments" 
                :key="dept.id" 
                :value="dept.id"
              >
                {{ dept.name }}
              </option>
            </select>
          </div>
          <button type="submit">Create Employee</button>
          <button @click="closeModal('create')">Cancel</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavbar from "@/components/AppNavbar.vue";

export default {
  name: "EmployeePage",
  components: {
    AppNavbar,
  },
  data() {
    return {
      employees: [],
      departments: [],
      companies: [],
      userRole: localStorage.getItem("userRole"),
      showViewModal: false,
      showEditModal: false,
      showCreateModal: false,
      selectedEmployee: null,
      form: {
        name: "",
        email: "",
        mobile_number: "",
        address: "",
        designation: "",
        department: "",
        company: "",
        status: "application_received",
        hired_on: "",
        days_employed: "",
      },
      allowedStatusOptions: [],
      filteredDepartments: [],
      canEdit: true,
    };
  },
  created() {
    this.fetchEmployees();
    this.fetchDepartments();
    this.fetchCompanies();
  },
  methods: {
    async fetchEmployees() {
      const token = localStorage.getItem("token");
      const response = await fetch(`${process.env.VUE_APP_API_URL}/employees/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      const data = await response.json();

      // Fetch department names for each employee
      for (let employee of data) {
        const departmentResponse = await fetch(`${process.env.VUE_APP_API_URL}/departments/${employee.department}/`, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        const departmentData = await departmentResponse.json();
        employee.departmentName = departmentData.name;
      }

      this.employees = data;
    },
    async fetchDepartments() {
      const token = localStorage.getItem("token");
      const response = await fetch(`${process.env.VUE_APP_API_URL}/departments/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      const data = await response.json();
      this.departments = data;
    },
    async fetchCompanies() {
      const token = localStorage.getItem("token");
      const response = await fetch(`${process.env.VUE_APP_API_URL}/companies/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      const data = await response.json();
      this.companies = data;
    },
    async viewEmployee(employee) {
      this.selectedEmployee = { ...employee };

      const token = localStorage.getItem("token");

      // Fetch department name
      if (employee.department) {
        const departmentResponse = await fetch(`${process.env.VUE_APP_API_URL}/departments/${employee.department}/`, {
          method: "GET",
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        const departmentData = await departmentResponse.json();
        this.selectedEmployee.departmentName = departmentData.name;
      }

      // Fetch company name
      if (employee.company) {
        const companyResponse = await fetch(`${process.env.VUE_APP_API_URL}/companies/${employee.company}/`, {
          method: "GET",
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        const companyData = await companyResponse.json();
        this.selectedEmployee.companyName = companyData.name;
      }

      this.showViewModal = true;
    },
    closeModal(modalType) {
      if (modalType === "view") {
        this.showViewModal = false;
      } else if (modalType === "edit") {
        this.showEditModal = false;
      } else if (modalType === "create") {
        this.showCreateModal = false;
      }
    },
    async editEmployee(employee) {
      this.selectedEmployee = { ...employee };
      this.form = {
        name: employee.name,
        email: employee.email,
        mobile_number: employee.mobile_number,
        address: employee.address,
        designation: employee.designation,
        status: employee.status,
        hired_on: employee.hired_on,
        days_employed: employee.days_employed,
      };

      // Set allowed status options based on current status
      if (employee.status === "application_received") {
        this.allowedStatusOptions = ["interview_scheduled", "not_accepted"];
      } else if (employee.status === "interview_scheduled") {
        this.allowedStatusOptions = ["hired", "not_accepted"];
      } else {
        this.allowedStatusOptions = [];
      }

      // Prevent editing if status is "Hired" or "Not Accepted"
      this.canEdit = !(employee.status === "hired" || employee.status === "not_accepted");

      this.showEditModal = true;
    },
    async updateEmployee() {
      const token = localStorage.getItem("token");

      // Create a new object with the fields to update (only the ones that have changed)
      const updatedEmployee = {
        name: this.form.name,
        email: this.form.email,
        mobile_number: this.form.mobile_number,
        address: this.form.address,
        designation: this.form.designation,
        status: this.form.status,
        // We are not sending 'hired_on' or 'days_employed' as they are updated by business logic
      };

      const response = await fetch(`${process.env.VUE_APP_API_URL}/employees/${this.selectedEmployee.id}/update/`, {
        method: "PUT",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedEmployee),
      });

      if (response.ok) {
        alert("Employee updated successfully.");
        this.fetchEmployees(); // Refresh the list after update
        this.closeModal("edit");
      } else {
        alert("Error updating employee.");
      }
    },
    async createEmployee() {
      const token = localStorage.getItem("token");

      // Format the hired_on date before submitting
      this.form.hired_on = this.formatDate(this.form.hired_on);

      const response = await fetch(`${process.env.VUE_APP_API_URL}/employees/create/`, {
        method: "POST",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...this.form,
          company: parseInt(this.form.company),
          department: parseInt(this.form.department)
        }),
      });

      if (response.ok) {
        alert("Employee created successfully.");
        this.fetchEmployees();
        this.closeModal("create");
      } else {
        // Parse the error response to provide more detailed feedback
        const errorData = await response.json();
        alert(`Error creating employee: ${JSON.stringify(errorData)}`);
      }
    },
    async deleteEmployee(employee) {
      if (confirm(`Are you sure you want to delete ${employee.name}?`)) {
        const token = localStorage.getItem("token");
        const response = await fetch(`${process.env.VUE_APP_API_URL}/employees/${employee.id}/delete/`, {
          method: "DELETE",
          headers: {
            Authorization: `Token ${token}`,
          },
        });

        if (response.ok) {
          alert("Employee deleted successfully.");
          this.fetchEmployees();
        } else {
          alert("Error deleting employee.");
        }
      }
    },
    openCreateModal() {
      // Reset form and filtered departments when opening create modal
      this.form = {
        name: "",
        email: "",
        mobile_number: "",
        address: "",
        designation: "",
        department: "",
        company: "",
        status: "application_received",
        hired_on: "",
        days_employed: "",
      };
      this.filteredDepartments = [];
      this.showCreateModal = true;
    },
    onCompanyChange() {
      // Filter departments based on selected company
      this.filteredDepartments = this.departments.filter(
        dept => dept.company === parseInt(this.form.company)
      );
      
      // Reset department selection when company changes
      this.form.department = "";
    },
    formatDate(date) {
      const d = new Date(date);
      let month = '' + (d.getMonth() + 1);
      let day = '' + d.getDate();
      const year = d.getFullYear();

      if (month.length < 2) month = '0' + month;
      if (day.length < 2) day = '0' + day;

      return [year, month, day].join('-');
    },
  },
};
</script>

<style scoped>
.employee-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.create-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.create-button:hover {
  background-color: #45a049;
}

.employee-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f4f4f4;
  border-radius: 8px;
  margin-bottom: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.button-container {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 16px;
  font-size: 1rem;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

button:hover {
  transform: scale(1.05);
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
}

.view-button {
  background-color: #3498db;
}

.edit-button {
  background-color: #f39c12;
}

.delete-button {
  background-color: #e53e3e;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-content.wider {
  width: 600px; /* Adjust the width as needed */
}

.scrollable {
  max-height: 80vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.info-message {
  font-size: 0.9rem;
  color: #555;
}
</style>