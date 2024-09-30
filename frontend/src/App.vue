<template>
  <div class="flex h-screen bg-gray-100">
    <Sidebar />
    <div class="flex-1 flex flex-col overflow-hidden">
      <Header :isLoggedIn="isLoggedIn" @logout="logout" />
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-200 p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import Header from '@/components/Header.vue'
import Sidebar from '@/components/Sidebar.vue'
import api from '@/api'

export default defineComponent({
  name: 'App',
  components: {
    Header,
    Sidebar
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const isLoggedIn = ref(false)

    const fetchData = () => {
      if (isLoggedIn.value) {
        store.dispatch('dashboard/fetchDashboardData')
        store.dispatch('customers/fetchCustomers')
        store.dispatch('inventory/fetchItems')
        store.dispatch('orders/fetchOrders')
      }
    }

    onMounted(() => {
      isLoggedIn.value = !!localStorage.getItem('token')
      fetchData()
    })

    watch(isLoggedIn, (newValue) => {
      if (newValue) {
        fetchData()
      }
    })

    const logout = () => {
      api.logout()
      isLoggedIn.value = false
      router.push('/login')
    }

    return { isLoggedIn, logout }
  }
})
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';
</style>