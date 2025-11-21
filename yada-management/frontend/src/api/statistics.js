import request from '@/utils/request'

// 获取工作台数据
export function getDashboardData() {
  return request({
    url: '/statistics/dashboard',
    method: 'get'
  })
}

// 获取业务统计图表
export function getBusinessChart() {
  return request({
    url: '/statistics/business-chart',
    method: 'get'
  })
}
