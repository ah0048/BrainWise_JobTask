import { createStore } from "vuex";

export default createStore({
  state: {
    userRole: localStorage.getItem("userRole") || null,
    token: localStorage.getItem("token") || null,
  },
  mutations: {
    setUserRole(state, role) {
      state.userRole = role;
      localStorage.setItem("userRole", role);
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem("token", token);
    },
    logout(state) {
      state.userRole = null;
      state.token = null;
      localStorage.removeItem("userRole");
      localStorage.removeItem("token");
    },
  },
  actions: {
    login({ commit }, { token, role }) {
      commit("setToken", token);
      commit("setUserRole", role);
    },
    logout({ commit }) {
      commit("logout");
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
    getRole: (state) => state.userRole,
  },
});
