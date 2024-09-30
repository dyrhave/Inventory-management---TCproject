import { Module } from 'vuex'
import { RootState } from '@/store'
import ApiService, { DashboardData } from '@/api'


interface DashboardState {
    data: DashboardData | null
    loading: boolean
    error: string | null
}

const dashboard: Module<DashboardState, RootState> = {
    namespaced: true,
    state: {
        data: null,
        loading: false,
        error: null
    },
    mutations: {
        setDashboardData(state, data: DashboardData) {
            state.data = data
        },
        setLoading(state, loading: boolean) {
            state.loading = loading
        },
        setError(state, error: string | null) {
            state.error = error
        }
    },
    actions: {
        async fetchDashboardData({ commit }) {
            commit('setLoading', true)
            try {
                const data = await ApiService.getDashboardData()
                commit('setDashboardData', data)
                commit('setError', null)
            } catch (error) {
                commit('setError', 'Failed to fetch dashboard data')
            }
            commit('setLoading', false)
        }
    },
    getters: {
        getDashboardData: (state) => state.data,
        isLoading: (state) => state.loading,
        getError: (state) => state.error
    }
}

export default dashboard