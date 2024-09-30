<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Customer Management</h1>
    <div v-if="loading" class="text-center">
      <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto"></div>
    </div>
    <div v-else>
      <button @click="showAddForm = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4">
        Add New Customer
      </button>

      <div v-if="showAddForm" class="mb-4 p-4 border rounded">
        <h2 class="text-xl font-bold mb-2">Add New Customer</h2>
        <form @submit.prevent="addNewCustomer">
          <input v-model="newCustomer.name" placeholder="Name" class="border p-2 mb-2 w-full">
          <input v-model="newCustomer.email" type="email" placeholder="Email" class="border p-2 mb-2 w-full">
          <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Add</button>
          <button @click="showAddForm = false" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded ml-2">Cancel</button>
        </form>
      </div>

      <table class="min-w-full table-auto">
        <thead>
        <tr>
          <th class="px-4 py-2">Name</th>
          <th class="px-4 py-2">Email</th>
          <th class="px-4 py-2">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="customer in customers" :key="customer.id">
          <td class="border px-4 py-2">{{ customer.name }}</td>
          <td class="border px-4 py-2">{{ customer.email }}</td>
          <td class="border px-4 py-2">
            <button @click="editCustomerItem(customer)" class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-1 px-2 rounded mr-2">Edit</button>
            <button @click="deleteCustomerItem(customer.id)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded">Delete</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState, mapActions } from 'vuex'
import { Customer } from '@/api'

export default defineComponent({
  name: 'CustomerView',
  data() {
    return {
      showAddForm: false,
      newCustomer: {
        name: '',
        email: ''
      }
    }
  },
  computed: {
    ...mapState('customers', ['customers', 'loading', 'error'])
  },
  methods: {
    ...mapActions('customers', ['fetchCustomers', 'addCustomer', 'updateCustomer', 'deleteCustomer']),
    async addNewCustomer() {
      await this.addCustomer(this.newCustomer)
      this.showAddForm = false
      this.newCustomer = { name: '', email: '' }
    },
    async editCustomerItem(customer: Customer) {
      // add edit functionality later
      console.log('Edit customer:', customer)
    },
    async deleteCustomerItem(id: number) {
      if (confirm('Are you sure you want to delete this customer?')) {
        await this.deleteCustomer(id)
      }
    }
  },
  mounted() {
    this.fetchCustomers()
  }
})
</script>