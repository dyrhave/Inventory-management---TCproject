<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <MetricCard title="Total Customers" :value="dashboardData?.stats.customer_count || 0" />
      <MetricCard title="Inventory Items" :value="dashboardData?.stats.inventory_count || 0" />
      <MetricCard title="Total Orders" :value="dashboardData?.stats.order_count || 0" />
      <MetricCard title="Revenue (This Month)" :value="formatCurrency(monthlyRevenue)" />
    </div>

    <div class="bg-white p-4 rounded-lg shadow" style="height: 500px; max-height: 400px;">
      <h2 class="text-xl font-semibold mb-4">Revenue Overview</h2>
      <LineChart :chartData="revenueChartData" :options="chartOptions" />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div class="bg-white p-4 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4">Recent Orders</h2>
        <table class="min-w-full">
          <thead>
          <tr>
            <th class="text-left">Order ID</th>
            <th class="text-left">Customer</th>
            <th class="text-left">Date</th>
            <th class="text-right">Total</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="order in dashboardData?.recent_orders" :key="order.id">
            <td>#{{ order.id }}</td>
            <td>{{ order.customer }}</td>
            <td>{{ formatDate(order.date) }}</td>
            <td class="text-right">{{ formatCurrency(order.total) }}</td>
          </tr>
          </tbody>
        </table>
      </div>

      <div class="bg-white p-4 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4">Low Stock Items</h2>
        <table class="min-w-full">
          <thead>
          <tr>
            <th class="text-left">Item</th>
            <th class="text-right">Current Stock</th>
            <th class="text-right">Reorder Level</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="item in lowStockItems" :key="item.id">
            <td>{{ item.name }}</td>
            <td class="text-right">{{ item.quantity }}</td>
            <td class="text-right">{{ item.reorder_level }}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import MetricCard from '@/components/MetricCard.vue'
import LineChart from '@/components/LineChart.vue'
import { DashboardData, InventoryItem } from '@/api'

export default defineComponent({
  name: 'DashboardView',
  components: {
    MetricCard,
    LineChart
  },
  setup() {
    const store = useStore()
    const dashboardData = ref<DashboardData | null>(null)
    const lowStockItems = ref<InventoryItem[]>([])
    const monthlyRevenue = ref(0)

    const formatCurrency = (value: number): string => {
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
    }

    const formatDate = (dateString: string): string => {
      return new Date(dateString).toLocaleDateString()
    }

    const revenueChartData = computed(() => ({
      labels: ['January', 'February', 'March', 'April', 'May', 'June'],
      datasets: [{
        label: 'Monthly Revenue',
        data: [12000, 19000, 3000, 5000, 2000, 3000],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    }))

    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false
    }

    onMounted(async () => {
      await store.dispatch('dashboard/fetchDashboardData')
      await store.dispatch('inventory/fetchItems')

      dashboardData.value = store.state.dashboard.data
      lowStockItems.value = store.state.inventory.items
          .filter((item: InventoryItem) => item.quantity < (item.reorder_level || 10))
          .slice(0, 5)

      // placeholder revenue
      monthlyRevenue.value = dashboardData.value?.recent_orders.reduce((acc, order) => acc + order.total, 0) || 0
    })

    return {
      dashboardData,
      lowStockItems,
      monthlyRevenue,
      formatCurrency,
      formatDate,
      revenueChartData,
      chartOptions
    }
  }
})
</script>