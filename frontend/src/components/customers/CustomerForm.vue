<template>
  <form @submit.prevent="submitForm" class="max-w-md mx-auto">
    <div class="mb-4">
      <label for="name" class="block mb-2">Name</label>
      <input v-model="form.name" id="name" type="text" required class="w-full px-3 py-2 border rounded">
    </div>
    <div class="mb-4">
      <label for="email" class="block mb-2">Email</label>
      <input v-model="form.email" id="email" type="email" required class="w-full px-3 py-2 border rounded">
    </div>
    <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">{{ isEditing ? 'Update' : 'Add' }} Customer</button>
  </form>
</template>

<script lang="ts">
import { defineComponent, reactive, PropType } from 'vue'
import { useStore } from 'vuex'
import { Customer } from '@/api'

export default defineComponent({
  name: 'CustomerForm',
  props: {
    customer: {
      type: Object as PropType<Customer>,
      default: null
    }
  },
  setup(props) {
    const store = useStore()
    const isEditing = !!props.customer

    const form = reactive({
      name: props.customer?.name || '',
      email: props.customer?.email || ''
    })

    const submitForm = () => {
      if (isEditing) {
        store.dispatch('customers/updateCustomer', { id: props.customer!.id, ...form })
      } else {
        store.dispatch('customers/addCustomer', form)
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