<template>
  <Bar v-if="chartData && chartData.labels.length" :chart-data="chartData" :options="chartOptions" />
  <p v-else>No data available for chart</p>
</template>

<script setup>
import { computed } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
});


const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
};
</script>