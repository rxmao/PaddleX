import request from '@/utils/request'

// 获取业务列表
export function getBusinessList(params) {
  return request({
    url: '/business',
    method: 'get',
    params
  })
}

// 获取业务详情
export function getBusinessDetail(id) {
  return request({
    url: `/business/${id}`,
    method: 'get'
  })
}

// 创建业务
export function createBusiness(data) {
  return request({
    url: '/business',
    method: 'post',
    data
  })
}

// 更新业务
export function updateBusiness(id, data) {
  return request({
    url: `/business/${id}`,
    method: 'put',
    data
  })
}

// 删除业务
export function deleteBusiness(id) {
  return request({
    url: `/business/${id}`,
    method: 'delete'
  })
}
