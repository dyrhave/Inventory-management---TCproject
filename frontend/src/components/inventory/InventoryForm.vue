<template>
  <form @submit.prevent="submitForm" class="max-w-md mx-auto">
    <div class="mb-4">
      <label for="name" class="block mb-2">Name</label>
      <input v-model="form.name" id="name" type="text" required class="w-full px-3 py-2 border rounded">
    </div>
    <div class="mb-4">
      <label for="price" class="block mb-2">Price</label>
      <input v-model.number="form.price" id="price" type="number" step="0.01" required class="w-full px-3 py-2 border rounded">
    </div>
    <div class="mb-4">
      <label for="quantity" class="block mb-2">Quantity</label>
      <input v-model.number="form.quantity" id="quantity" type="number" required class="w-full px-3 py-2 border rounded">
    </div>
    <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">{{ isEditing ? 'Update' : 'Add' }} Item</button>
  </form>
</template>

<script lang="ts">
import { defineComponent, reactive, PropType } from 'vue'
import { useStore } from 'vuex'
import { InventoryItem } from '@/api'

export default defineComponent({
  name: 'InventoryForm',
  props: {
    item: {
      type: Object as PropType<InventoryItem>,
      default: null
    }
  },
  setup(props) {
    const store = useStore()
    const isEditing = !!props.item

    const form = reactive({
      name: props.item?.name || '',
      price: props.item?.price || 0,
      quantity: props.item?.quantity || 0
    })

    const submitForm = () => {
      if (isEditing) {
        store.dispatch('inventory/updateInventoryItem', { id: props.item!.id, ...form })
      } else {
        store.dispatch('inventory/addInventoryItem', form)
      }
    }

    return {
      form,
      isEditing,
      submitForm
    }
  }
})
</script>