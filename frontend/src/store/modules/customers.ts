import { Module } from 'vuex'
import { RootState } from '@/store'
import ApiService, { Customer } from '@/api'

interface CustomerState {
    customers: Customer[]
    loading: boolean
    error: string | null
}

const customers: Module<CustomerState, RootState> = {
    namespaced: true,
    state: {
        customers: [],
        loading: false,
        error: null
    },
    mutations: {
        setCustomers(state, customers: Customer[]) {
            state.customers = customers
        },
        addCustomer(state, customer: Customer) {
            state.customers.push(customer)
        },
        updateCustomer(state, updatedCustomer: Customer) {
            const index = state.customers.findIndex(c => c.id === updatedCustomer.id)
            if (index !== -1) {
                state.customers[index] = updatedCustomer
            }
        },
        removeCustomer(state, id: number) {
            state.customers = state.customers.filter(c => c.id !== id)
        },
        setLoading(state, loading: boolean) {
            state.loading = loading
        },
        setError(state, error: string | null) {
            state.error = error
        }
    },
    actions: {
        async fetchCustomers({ commit }) {
            commit('setLoading', true)
            try {
                const customers = await ApiService.getCustomers()
                commit('setCustomers', customers)
                commit('setError', null)
            } catch (error) {
                commit('setError', 'Failed to fetch customers')
            }
            commit('setLoading', false)
        },
        async addCustomer({ commit }, customer: Omit<Customer, 'id'>) {
            commit('setLoading', true)
            try {
                const newCustomer = await ApiService.createCustomer(customer)
                commit('addCustomer', newCustomer)
                commit('setError', null)
            } catch (error) {
                commit('setError', 'Failed to add customer')
            }
            commit('setLoading', false)
        },
        async updateCustomer({ commit }, { id, customer }: { id: number, customer: Partial<Customer> }) {
            commit('setLoading', true)
            try {
                await ApiService.updateCustomer(id, customer)
                commit('updateCustomer', { id, ...customer })
                commit('setError', null)
            } catch (error) {
                commit('setError', 'Failed to update customer')
            }
            commit('setLoading', false)
        },
        async deleteCustomer({ commit }, id: number) {
            commit('setLoading', true)
            try {
                await ApiService.deleteCustomer(id)
                commit('removeCustomer', id)
                commit('setError', null)
            } catch (error) {
                commit('setError', 'Failed to delete customer')
            }
            commit('setLoading', false)
        }
    },
    getters: {
        getCustomers: (state) => state.customers,
        isLoading: (state) => state.loading,
        getError: (state) => state.error
    }
}

export default customers