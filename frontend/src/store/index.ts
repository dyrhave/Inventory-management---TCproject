import { createStore } from 'vuex'
import customers from "@/store/modules/customers";
import inventory from "@/store/modules/inventory";
import dashboard from "@/store/modules/dashboard";
import orders from "@/store/modules/orders"
import auth from './modules/auth'

export interface RootState {

}

export default createStore({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    inventory,
    customers,
    dashboard,
    orders,
    auth
  }
})
