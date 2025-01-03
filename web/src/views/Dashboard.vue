<template>
  <div class="dashboard">

    <!-- 数据卡片行 -->
    <el-row :gutter="20">
      <el-col :span="6" v-for="card in cards" :key="card.title">
        <el-card class="data-card" :class="card.type">
          <div class="card-content">
            <div class="card-icon">
              <el-icon><component :is="card.icon" /></el-icon>
            </div>
            <div class="card-info">
              <div class="title">{{ card.title }}</div>
              <div class="value">{{ card.value }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表行 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <h3>笔记趋势</h3>
              <el-radio-group v-model="timeRange" size="small">
                <el-radio-button value="week">本周</el-radio-button>
                <el-radio-button value="month">本月</el-radio-button>
                <el-radio-button value="year">全年</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <base-chart :option="notesChartOption" height="360px" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <h3>分组分布</h3>
            </div>
          </template>
          <base-chart :option="groupPieOption" height="360px" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { getNoteStats, getActiveUsers } from '@/api'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import {
  Document,
  FolderOpened,
  User,
  SwitchButton
} from '@element-plus/icons-vue'
import type { EChartsOption } from 'echarts'
import BaseChart from '@/components/BaseChart.vue'

const router = useRouter()
const userStore = useUserStore()
const user = computed(() => userStore.user)

// 处理退出登录
const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const timeRange = ref('week')

const cards = ref([
  {
    title: '笔记总数',
    value: 0,
    type: 'primary',
    icon: 'Document',
    trend: 0
  },
  {
    title: '分组总数',
    value: 0,
    type: 'success',
    icon: 'FolderOpened',
    trend: 0
  },
  {
    title: '今日活跃',
    value: 0,
    type: 'warning',
    icon: 'User',
    trend: 0
  },
  {
    title: '用户总数',
    value: 0,
    type: 'info',
    icon: 'User',
    trend: 0
  }
])

const fetchStats = async () => {
  try {
    const [statsRes, activeUsersRes] = await Promise.all([
      getNoteStats({ range: timeRange.value }),
      getActiveUsers()
    ])
    
    // 更新笔记和分组数据
    cards.value[0].value = statsRes.data.total_notes
    cards.value[1].value = statsRes.data.total_groups
    
    // 更新活跃用户和用户总数数据
    cards.value[2].value = activeUsersRes.data.active_users
    cards.value[3].value = activeUsersRes.data.total_users

    // 计算笔记增长趋势
    const notes_charts = statsRes.data.notes_charts
    if (notes_charts.length >= 2) {
      const lastDay = notes_charts[notes_charts.length - 1].count
      const prevDay = notes_charts[notes_charts.length - 2].count
      if (prevDay > 0) {
        cards.value[0].trend = Math.round((lastDay - prevDay) / prevDay * 100)
      }
    }

    // 更新图表数据
    notesChartOption.value = {
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderColor: '#eee',
        borderWidth: 1,
        textStyle: {
          color: '#666'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: notes_charts.map(item => {
          if (timeRange.value === 'year') {
            const [year, month] = item.date.split('-')
            return `${year}年${month}月`
          } else if (timeRange.value === 'month') {
            const date = new Date(item.date)
            return `${date.getMonth() + 1}/${date.getDate()}`
          } else {
            const date = new Date(item.date)
            return ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][date.getDay()]
          }
        })
      },
      yAxis: {
        type: 'value',
        axisLine: {
          show: false
        },
        splitLine: {
          lineStyle: {
            color: '#eee'
          }
        }
      },
      series: [{
        name: '笔记数量',
        type: 'line',
        data: notes_charts.map(item => item.count),
        smooth: timeRange.value === 'year'
      }]
    }

    // 更新分组分布图表数据
    groupPieOption.value = {
      color: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399'],
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderColor: '#eee',
        borderWidth: 1,
        textStyle: {
          color: '#666'
        }
      },
      legend: {
        orient: 'vertical',
        right: '5%',
        top: 'center',
        textStyle: {
          color: '#666'
        }
      },
      series: [
        {
          name: '分组分布',
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['40%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 14,
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: statsRes.data.groups_distribution
        }
      ]
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 监听时间范围变化
watch(timeRange, () => {
  fetchStats()
})

onMounted(async () => {
  await userStore.fetchUserInfo()
  fetchStats()
})

// 笔记趋势图表配置
const notesChartOption = ref<EChartsOption>({
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderColor: '#eee',
    borderWidth: 1,
    textStyle: {
      color: '#666'
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    axisLine: {
      lineStyle: {
        color: '#ddd'
      }
    }
  },
  yAxis: {
    type: 'value',
    axisLine: {
      show: false
    },
    splitLine: {
      lineStyle: {
        color: '#eee'
      }
    }
  },
  series: [
    {
      name: '笔记数',
      type: 'line',
      smooth: true,
      data: [15, 22, 18, 30, 25, 35, 28],
      lineStyle: {
        width: 3,
        color: '#409EFF'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            {
              offset: 0,
              color: 'rgba(64, 158, 255, 0.2)'
            },
            {
              offset: 1,
              color: 'rgba(64, 158, 255, 0.05)'
            }
          ]
        }
      },
      symbol: 'circle',
      symbolSize: 8
    }
  ]
})

// 分组分布图表配置
const groupPieOption = ref<EChartsOption>({
  color: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399'],
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c} ({d}%)',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderColor: '#eee',
    borderWidth: 1,
    textStyle: {
      color: '#666'
    }
  },
  legend: {
    orient: 'vertical',
    right: '5%',
    top: 'center',
    textStyle: {
      color: '#666'
    }
  },
  series: [
    {
      name: '分组分布',
      type: 'pie',
      radius: ['50%', '70%'],
      center: ['40%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 35, name: '无数据' },
        { value: 25, name: '学习' },
        { value: 20, name: '生活' },
        { value: 15, name: '娱乐' },
        { value: 5, name: '其他' }
      ]
    }
  ]
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100%;
}

/* 数据卡片样式 */
.data-card {
  margin-bottom: 20px;
  border-radius: 15px;
  border: none;
  transition: transform 0.3s;
}

.data-card:hover {
  transform: translateY(-5px);
}

.card-content {
  display: flex;
  align-items: center;
  padding: 10px;
  justify-content: space-between;
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.primary .card-icon {
  background-color: rgba(64, 158, 255, 0.1);
  color: #409EFF;
}

.success .card-icon {
  background-color: rgba(103, 194, 58, 0.1);
  color: #67C23A;
}

.warning .card-icon {
  background-color: rgba(230, 162, 60, 0.1);
  color: #E6A23C;
}

.info .card-icon {
  background-color: rgba(144, 147, 153, 0.1);
  color: #909399;
}

.card-info {
  text-align: right;
}

.card-info .value {
  font-size: 24px;
  font-weight: bold;
  margin-top: 5px;
}

.card-info .title {
  font-size: 14px;
  color: #909399;
}

/* 图表卡片样式 */
.chart-row {
  margin-bottom: 20px;
}

.chart-card {
  border-radius: 15px;
  border: none;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.chart-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

:deep(.el-radio-button__inner) {
  border-radius: 20px !important;
}

:deep(.el-button) {
  border-radius: 25px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-card__body) {
  padding: 20px;
}

/* 添加用户信息样式 */
.user-info {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.user-dropdown-link {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-right: 10px;
  font-size: 14px;
  color: #606266;
}

.avatar {
  background-color: #409EFF;
  color: #fff;
  font-weight: bold;
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-dropdown-menu__item .el-icon) {
  margin-right: 4px;
}
</style> 