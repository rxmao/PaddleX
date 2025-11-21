<template>
  <div class="business-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>业务列表</span>
          <el-button type="primary"><el-icon><Plus /></el-icon>新增业务</el-button>
        </div>
      </template>

      <el-empty description="业务管理功能开发中..." />
    </el-card>
  </div>
</template>

<script setup>
import { Plus } from '@element-plus/icons-vue'
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
