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
  name: 'Menu',
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
