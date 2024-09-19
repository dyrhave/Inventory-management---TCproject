<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else class="metrics">
      <div class="metric">
        <h2>Alle Kunder</h2>
        <p>{{ dashboardData.totalCustomers }}</p>
      </div>
      <div class="metric">
        <h2>Alle Lager Produkter</h2>
        <p>{{ dashboardData.totalInventory }}</p>
      </div>
      <div class="recent-orders">
        <h2>Seneste Ordrer</h2>
        <ul>
          <li v-for="order in dashboardData.recentOrders" :key="order.id">
            Ordre #{{ order.id }} - {{ order.customer }} - ${{ order.total }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  name: 'DashboardView',
  data() {
    return {
      dashboardData: null,
      loading: true,
      error: null,
    }
  },
  async created() {
    try {
      if (!localStorage.getItem('token')) {
        this.$router.push('/login');
        return;
      }
      this.dashboardData = await api.getDashboardData();
    } catch (err) {
      if (err.response && err.response.status === 401) {
        this.$router.push('/login');
      } else {
        this.error = 'Failed to load dashboard data';
        console.error(err);
      }
    } finally {
      this.loading = false;
    }
  },
};
</script>


<style scoped>
.dashboard {
  padding: 20px;
}

.metrics {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.recent-orders {
  margin-top: 20px;
}
</style>