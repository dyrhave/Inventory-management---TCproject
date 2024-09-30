import { Module } from 'vuex'
import { RootState } from '@/store'
import ApiService, { InventoryItem } from '@/api'

interface InventoryState {
    items: InventoryItem[]
    loading: boolean
    error: string | null
}

const inventory: Module<InventoryState, RootState> = {
    namespaced: true,
    state: {
        items: [],
        loading: false,
        error: null
    },
    mutations: {
        setItems(state, items: InventoryItem[]) {
            state.items = items
        },
        addItem(state, item: InventoryItem) {
            state.items.push(item)
        },
        updateItem(state, updatedItem: InventoryItem) {
            const index = state.items.findIndex(item => item.id === updatedItem.id)
            if (index !== -1) {
                state.items[index] = updatedItem
            }
        },
        removeItem(state, id: number) {
            state.items = state.items.filter(item => item.id !== id)
        },
        setLoading(state, loading: boolean) {
            state.loading = loading
        },
        setError(state, error: string | null) {
            state.error = error
        }
    },
    actions: {
        async fetchItems({ commit }) {
            commit('setLoading', true)
            try {
                const items = await ApiService.getInventory()
                commit('setItems', items)
                commit('setError', null)
            } catch (error) {
                commit('setError', 'Failed to fetch inventory items')
            }
            commit('setLoading', false)
        },
        async addInventoryItem({ commit }, item: Omit<InventoryItem, 'id'>) {
            commit('setLoading', true)
            try {
                const newItem = await ApiService.createInventoryItem(item)
                commit('addItem', newItem)
                commit('setError', null)
            } catch (error) {
                commit('setError', 'Failed to add inventory item')
            }
            commit('setLoading', false)
        },
        async updateInventoryItem({ commit }, { id, item }: { id: number, item: Partial<InventoryItem> }) {
            commit('setLoading', true)
            try {
                await ApiService.updateInventoryItem(id, item)
                commit('updateItem', { id, ...item })
                commit('setError', null)
            } catch (error) {
                commit('setError', 'Failed to update inventory item')
            }
            commit('setLoading', false)
        },
        async deleteInventoryItem({ commit }, id: number) {
            commit('setLoading', true)
            try {
                await ApiService.deleteInventoryItem(id)
                commit('removeItem', id)
                commit('setError', null)
            } catch (error) {
                commit('setError', 'Failed to delete inventory item')
            }
            commit('setLoading', false)
        }
    },
    getters: {
        getItems: (state) => state.items,
        isLoading: (state) => state.loading,
        getError: (state) => state.error
    }
}

export default inventory