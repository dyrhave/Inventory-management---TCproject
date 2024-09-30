<template>
  <aside class="bg-gray-800 text-white w-64 space-y-6 py-7 px-2 absolute inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition duration-200 ease-in-out">
    <nav>
      <router-link to="/dashboard" class="block py-2.5 px-4 rounded transition duration-200 hover:bg-gray-700">Dashboard</router-link>
      <router-link to="/customers" class="block py-2.5 px-4 rounded transition duration-200 hover:bg-gray-700">Customers</router-link>
      <router-link to="/inventory" class="block py-2.5 px-4 rounded transition duration-200 hover:bg-gray-700">Inventory</router-link>
      <router-link to="/orders" class="block py-2.5 px-4 rounded transition duration-200 hover:bg-gray-700">Orders</router-link>
    </nav>
  </aside>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Sidebar'
})
</script>