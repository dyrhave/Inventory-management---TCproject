<template>
  <div>
    <Bar
        v-if="chartData.datasets[0].data.length > 0"
        :data="chartData"
        :options="chartOptions"
    />
    <p v-else class="text-center text-gray-500 py-4">No data available for chart</p>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue';
import {Bar} from 'vue-chartjs';
import {Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
});

const chartData = ref({
  labels: [],
  datasets: [{
    label: 'Order Total',
    data: [],
    backgroundColor: '#4F46E5',
  }]
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Total (DKK)'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Order ID'
      }
    }
  }
};

watch(() => props.data, (newData) => {
  chartData.value.labels = newData.map(item => `#${item.id}`);
  chartData.value.datasets[0].data = newData.map(item => item.total);
}, {immediate: true, deep: true});
</script>