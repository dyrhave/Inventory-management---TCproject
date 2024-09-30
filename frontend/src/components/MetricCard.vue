<template>
  <div class="bg-white p-4 rounded-lg shadow">
    <h2 class="text-lg font-semibold mb-2">{{ title }}</h2>
    <p class="text-3xl font-bold">{{ value }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MetricCard',
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: [Number, String],
      required: true
    }
  }
})
</script>