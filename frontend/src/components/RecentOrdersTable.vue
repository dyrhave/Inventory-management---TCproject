<template>
  <div class="bg-white rounded-lg shadow overflow-hidden">
    <h2 class="text-xl font-semibold p-6">{{ title }}</h2>
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
      <tr>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order ID</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
      </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
      <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50">
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{{ order.id }}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ order.customer }}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ formatDate(order.date) }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ formatCurrency(order.total) }}
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: 'Recent Orders'
  },
  orders: {
    type: Array,
    required: true
  }
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('da-DK');
};

const formatCurrency = (value) => {
  return value.toLocaleString('da-DK', {style: 'currency', currency: 'DKK'});
};
</script>