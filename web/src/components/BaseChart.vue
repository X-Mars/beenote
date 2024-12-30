<template>
  <div ref="chartRef" :style="{ height: height, width: width }" />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'

const props = withDefaults(defineProps<{
  option: EChartsOption
  height?: string
  width?: string
}>(), {
  height: '300px',
  width: '100%'
})

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const initChart = () => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  chart.setOption(props.option)
}

watch(() => props.option, (newOption) => {
  chart?.setOption(newOption)
}, { deep: true })

onMounted(() => {
  initChart()
  window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
  window.removeEventListener('resize', () => chart?.resize())
  chart?.dispose()
})
</script> 