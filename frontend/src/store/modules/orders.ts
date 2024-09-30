import { Module } from 'vuex';
import ApiService, { Order } from '@/api';

interface OrdersState {
    orders: Order[];
    loading: boolean;
    error: string | null;
}

const ordersModule: Module<OrdersState, any> = {
    namespaced: true,
    state: {
        orders: [],
        loading: false,
        error: null,
    },
    mutations: {
        setOrders(state, orders: Order[]) {
            state.orders = orders;
        },
        addOrder(state, order: Order) {
            state.orders.push(order);
        },
        removeOrder(state, id: number) {
            state.orders = state.orders.filter(order => order.id !== id);
        },
        setLoading(state, loading: boolean) {
            state.loading = loading;
        },
        setError(state, error: string | null) {
            state.error = error;
        },
    },
    actions: {
        async fetchOrders({ commit }) {
            commit('setLoading', true);
            try {
                const orders = await ApiService.getOrders();
                commit('setOrders', orders);
                commit('setError', null);
            } catch (error) {
                commit('setError', 'Failed to fetch orders');
            } finally {
                commit('setLoading', false);
            }
        },
        async createOrder({ commit }, orderData: { customer_id: number, items: { id: number, quantity: number }[] }) {
            commit('setLoading', true);
            try {
                const newOrder = await ApiService.createOrder(orderData);
                commit('addOrder', newOrder);
                commit('setError', null);
            } catch (error) {
                commit('setError', 'Failed to create order');
            } finally {
                commit('setLoading', false);
            }
        },
        async deleteOrder({ commit }, id: number) {
            commit('setLoading', true);
            try {
                await ApiService.deleteOrder(id);
                commit('removeOrder', id);
                commit('setError', null);
            } catch (error) {
                commit('setError', 'Failed to delete order');
            } finally {
                commit('setLoading', false);
            }
        },
    },
    getters: {
        getOrderById: (state) => (id: number) => {
            return state.orders.find(order => order.id === id);
        },
    },
};

export default ordersModule;