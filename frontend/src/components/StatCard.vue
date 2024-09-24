<template>
  <div class="bg-white rounded-lg shadow p-6 flex items-center">
    <component :is="icon" class="w-6 h-6" :class="iconColor"/>
    <div class="ml-4">
      <p class="text-sm font-medium text-gray-500">{{ label }}</p>
      <p class="text-2xl font-semibold text-gray-900">{{ value }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  icon: {
    type: Object,
    required: true
  },
  iconColor: {
    type: String,
    default: 'text-blue-500'
  },
  label: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  }
});
</script>