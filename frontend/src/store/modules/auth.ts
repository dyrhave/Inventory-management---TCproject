import { Module } from 'vuex'
import { RootState } from '@/store'
import api from '@/api'

interface AuthState {
    token: string | null
    user: any | null
}

const auth: Module<AuthState, RootState> = {
    namespaced: true,
    state: {
        token: localStorage.getItem('token'),
        user: null
    },
    mutations: {
        setToken(state, token) {
            state.token = token
            if (token) {
                localStorage.setItem('token', token)
            } else {
                localStorage.removeItem('token')
            }
        },
    },
    actions: {
        async loginUser({ commit }, { username, password }) {
            const token = await api.login(username, password)
            commit('setToken', token)
            api.setAuthToken(token)
        },
        async logoutUser({ commit }) {
            commit('setToken', null)
            commit('setUser', null)
            api.clearAuthToken()
        }
    },
    getters: {
        isAuthenticated: (state) => !!state.token,
        currentUser: (state) => state.user
    }
}

export default auth