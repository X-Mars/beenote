<template>
  <div>
    <el-container>
      <el-aside width="200px">
        <list></list>
      </el-aside>
      <el-main>Main</el-main>
    </el-container>
  </div>
</template>

<script>

import list from './list'

export default {
  name: '最新文档',
  components: {
    list
  },
  data() {
    return {
      data: {}
    }
  }
}
</script>
