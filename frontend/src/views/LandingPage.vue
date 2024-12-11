<template>
    <div class="landing-page">
      <div class="login-container">
        <h1>Employee Management System</h1>
        <LoginForm />
      </div>
    </div>
  </template>
  
  <script>
  import LoginForm from "@/components/LoginForm.vue";
  
  export default {
    name: "LandingPage",
    components: {
      LoginForm,
    },
  };
  </script>
  
  <style scoped>

    html, body {
    height: 100%;
    margin: 0; /* Remove default margin */
    }

  .landing-page {
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
    font-family: Arial, sans-serif;
  }
  
  .login-container {
    text-align: center;
    background: #fff;
    padding: 2rem;
    background-color: #e6f0ff; /* Light sky blue */
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    color: #333;
  }
  
  h1 {
    margin-bottom: 1.5rem;
  }
  </style>
  