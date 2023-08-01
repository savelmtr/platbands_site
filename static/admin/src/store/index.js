import { createStore } from 'vuex'

export default createStore({
  state: {
    sidebarVisible: true,
    accessToken: null
  },
  mutations: {
    toggleSidebar(state) {
      state.sidebarVisible = !state.sidebarVisible
    },
    setToken(state, token) {
      state.accessToken = token
    }
  },
  actions: {},
  modules: {},
})