<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Inventory Management</h1>
    <div v-if="loading" class="text-center">
      <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto"></div>
    </div>
    <div v-else>
      <button @click="showAddForm = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4">
        Add New Item
      </button>

      <div v-if="showAddForm" class="mb-4 p-4 border rounded">
        <h2 class="text-xl font-bold mb-2">Add New Item</h2>
        <form @submit.prevent="addItem">
          <input v-model="newItem.name" placeholder="Name" class="border p-2 mb-2 w-full">
          <input v-model.number="newItem.price" type="number" placeholder="Price" class="border p-2 mb-2 w-full">
          <input v-model.number="newItem.quantity" type="number" placeholder="Quantity" class="border p-2 mb-2 w-full">
          <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Add</button>
          <button @click="showAddForm = false" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded ml-2">Cancel</button>
        </form>
      </div>

      <table class="min-w-full table-auto">
        <thead>
        <tr>
          <th class="px-4 py-2">Name</th>
          <th class="px-4 py-2">Price</th>
          <th class="px-4 py-2">Quantity</th>
          <th class="px-4 py-2">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in items" :key="item.id">
          <td class="border px-4 py-2">{{ item.name }}</td>
          <td class="border px-4 py-2">{{ item.price }}</td>
          <td class="border px-4 py-2">{{ item.quantity }}</td>
          <td class="border px-4 py-2">
            <button @click="editItem(item)" class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-1 px-2 rounded mr-2">Edit</button>
            <button @click="deleteItem(item.id)" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded">Delete</button>
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
import { InventoryItem } from '@/api'

export default defineComponent({
  name: 'InventoryView',
  data() {
    return {
      showAddForm: false,
      newItem: {
        name: '',
        price: 0,
        quantity: 0
      }
    }
  },
  computed: {
    ...mapState('inventory', ['items', 'loading', 'error'])
  },
  methods: {
    ...mapActions('inventory', ['fetchItems', 'addInventoryItem', 'updateInventoryItem', 'deleteInventoryItem']),
    async addNewItem() {
      await this.addInventoryItem(this.newItem)
      this.showAddForm = false
      this.newItem = { name: '', price: 0, quantity: 0 }
    },
    async editInventoryItem(item: InventoryItem) {
      // Implement edit functionality
      console.log('Edit item:', item)
    },
    async deleteInventoryItem(id: number) {
      if (confirm('Are you sure you want to delete this item?')) {
        await this.deleteInventoryItem(id)
      }
    }
  },
  mounted() {
    this.fetchItems()
  }
})
</script>