<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Customer List</h2>
    <button @click="openAddCustomerForm" class="bg-blue-500 text-white px-4 py-2 rounded mb-4">Add New Customer</button>
    <table class="min-w-full bg-white">
      <thead>
      <tr>
        <th class="text-left py-2 px-3 border-b">Name</th>
        <th class="text-left py-2 px-3 border-b">Email</th>
        <th class="text-left py-2 px-3 border-b">Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="customer in customers" :key="customer.id">
        <td class="py-2 px-3 border-b">{{ customer.name }}</td>
        <td class="py-2 px-3 border-b">{{ customer.email }}</td>
        <td class="py-2 px-3 border-b">
          <button @click="editCustomer(customer)" class="text-blue-500 mr-2">Edit</button>
          <button @click="deleteCustomer(customer.id)" class="text-red-500">Delete</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useStore } from 'vuex'
import { Customer } from '@/api'

export default defineComponent({
  name: 'CustomerList',
  setup() {
    const store = useStore()

    const customers = computed(() => store.state.customers.customers)

    const openAddCustomerForm = () => {
      // add function later
    }

    const editCustomer = (customer: Customer) => {
      // add function later
    }

    const deleteCustomer = (id: number) => {
      store.dispatch('customers/deleteCustomer', id)
    }

    const fetchCustomers = async () => {
      await store.dispatch('customers/fetchCustomers')
    }

    fetchCustomers()

    return {
      customers,
      openAddCustomerForm,
      editCustomer,
      deleteCustomer
    }
  }
})
</script>