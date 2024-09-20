<template>
  <div class="min-h-screen bg-gray-100 p-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

      <div v-if="loading" class="text-center">
        <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto"></div>
      </div>

      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong class="font-bold">Error:</strong>
        <span class="block sm:inline">{{ error }}</span>
      </div>

      <template v-else-if="dashboardData">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div v-for="(value, key) in dashboardData.stats" :key="key" class="bg-white rounded-lg shadow p-6 flex items-center">
            <component :is="getIcon(key)" class="w-6 h-6" :class="getIconColor(key)"/>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">{{ getStatLabel(key) }}</p>
              <p class="text-2xl font-semibold text-gray-900">{{ value }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6 mb-8">
          <h2 class="text-xl font-semibold mb-4">Ordre Oversigt</h2>
          <BarChart :data="chartData" />
        </div>

        <div class="bg-white rounded-lg shadow overflow-hidden">
          <h2 class="text-xl font-semibold p-6">Seneste Ordrer</h2>
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
            <tr v-for="order in dashboardData.recent_orders" :key="order.id" class="hover:bg-gray-50">
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

      <div v-else class="text-center text-gray-500">No data available</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Users, Package, ShoppingCart } from 'lucide-vue-next';
import api from '../api';
// import StatCard from '../components/StatCard.vue';
import BarChart from '../components/BarChart.vue';
// import RecentOrdersTable from '../components/RecentOrdersTable.vue';

const router = useRouter();
const dashboardData = ref(null);
const loading = ref(true);
const error = ref(null);

const chartData = computed(() => {
  if (!dashboardData.value || !dashboardData.value.recent_orders) return [];
  return dashboardData.value.recent_orders.map(order => ({
    id: order.id,
    total: order.total
  }));
});

const fetchDashboardData = async () => {
  try {
    if (!localStorage.getItem('token')) {
      router.push('/login');
      return;
    }
    api.setAuthToken(localStorage.getItem('token'));
    const data = await api.getDashboardData();
    if (data && data.recent_orders) {
      dashboardData.value = data;
    } else {
      throw new Error('Invalid data structure');
    }
  } catch (err) {
    if (err.response && err.response.status === 401) {
      router.push('/login');
    } else {
      error.value = 'Failed to load dashboard data';
      console.error(err);
    }
  } finally {
    loading.value = false;
  }
};

const getIcon = (key) => {
  switch (key) {
    case 'customer_count': return Users;
    case 'inventory_count': return Package;
    case 'order_count': return ShoppingCart;
    default: return null;
  }
};

const getIconColor = (key) => {
  switch (key) {
    case 'customer_count': return 'text-blue-500';
    case 'inventory_count': return 'text-green-500';
    case 'order_count': return 'text-purple-500';
    default: return '';
  }
};

const getStatLabel = (key) => {
  switch (key) {
    case 'customer_count': return 'Alle Kunder';
    case 'inventory_count': return 'Alle Lager Produkter';
    case 'order_count': return 'Alle Ordrer';
    default: return key;
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('da-DK');
};

const formatCurrency = (value) => {
  return value.toLocaleString('da-DK', {style: 'currency', currency: 'DKK'});
};

onMounted(fetchDashboardData);
</script>