<template>
  <header class="bg-white shadow">
    <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">ComputeAgain</h1>
      <div class="flex items-center">
        <input type="text" placeholder="Search..." class="mr-4 px-3 py-2 border rounded-md" />
        <button class="bg-blue-500 text-white px-4 py-2 rounded-md">Profile</button>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Header'
})
</script>