<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Inventory List</h2>
    <button @click="openAddInventoryForm" class="bg-blue-500 text-white px-4 py-2 rounded mb-4">Add New Item</button>
    <table class="min-w-full bg-white">
      <thead>
      <tr>
        <th class="text-left py-2 px-3 border-b">Name</th>
        <th class="text-left py-2 px-3 border-b">Price</th>
        <th class="text-left py-2 px-3 border-b">Quantity</th>
        <th class="text-left py-2 px-3 border-b">Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in inventoryItems" :key="item.id">
        <td class="py-2 px-3 border-b">{{ item.name }}</td>
        <td class="py-2 px-3 border-b">{{ item.price }}</td>
        <td class="py-2 px-3 border-b">{{ item.quantity }}</td>
        <td class="py-2 px-3 border-b">
          <button @click="editItem(item)" class="text-blue-500 mr-2">Edit</button>
          <button @click="deleteItem(item.id)" class="text-red-500">Delete</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useStore } from 'vuex'
import { InventoryItem } from '@/api'  // Correct import from api

export default defineComponent({
  name: 'InventoryList',
  setup() {
    const store = useStore()

    const inventoryItems = computed(() => store.state.inventory.items)

    const openAddInventoryForm = () => {
      // add inventory logic later
    }

    const editItem = (item: InventoryItem) => {
      // add inventory logic later
    }

    const deleteItem = (id: number) => {
      store.dispatch('inventory/deleteInventoryItem', id)
    }

    return {
      inventoryItems,
      openAddInventoryForm,
      editItem,
      deleteItem
    }
  }
})
</script>