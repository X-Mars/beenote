<template>
  <el-scrollbar wrap-class="scrollbar-wrapper">
    <el-menu
      :show-timeout="200"
      :default-active="$route.path"
      :collapse="isCollapse"
      mode="vertical"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
      <sidebar-item v-for="route in permission_routers" :key="route.path" :item="route" :base-path="route.path"/>
    </el-menu>
  </el-scrollbar>
</template>

<script>
import { mapGetters } from 'vuex'
import SidebarItem from './SidebarItem'
import { getNoteBook } from '@/api/bee'


export default {
  components: { SidebarItem },
  computed: {
    ...mapGetters([
      'permission_routers',
      'sidebar'
    ]),
    isCollapse() {
      return !this.sidebar.opened
    }
  },
  mounted() {
    // 从后台获取笔记本信息（包含笔记），并添加路由到侧边栏。
    getNoteBook().then(res => {
      this.$store.dispatch('setNotebookInfo', res.data)
      var routes = this.permission_routers
      var notebookInfo = res.data
      for(var routeIndex in routes){
        if(routes[routeIndex].redirect == 'meum'){
          for(var notebookIndex in notebookInfo){
            if(notebookInfo[notebookIndex].children.name != routes[routeIndex].name){
              notebookInfo[notebookIndex].children.component = eval(res.data[notebookIndex].children.component)
              notebookInfo[notebookIndex].children.meta = eval(res.data[notebookIndex].children.meta)
              routes[routeIndex].children.push(notebookInfo[notebookIndex].children)
            }
          }
        }
      }
    })
  },
  methods: {
  }
}
</script>
