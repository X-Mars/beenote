<template>
  <div>
    <el-row>
      <el-col v-for="o in 2" :key="o" :span="24">
        <el-card :body-style="{ padding: '0px' }">
          <div style="padding: 15px;">
            <span style="text-align: center;">好吃的汉堡</span>
            <div class="bottom clearfix">
              <time class="time">2018-12-28 </time>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import { getNoteBook } from '@/api/bee'

export default {
  name: 'List',
  data() {
    return {
      loginForm: {
        username: 'admin',
        password: 'admin'
      }
    }
  },
  mounted(){
  },
  methods: {
  }
}
</script>

<style>
  .time {
    font-size: 13px;
    color: #999;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .clearfix:before,

  .clearfix:after {
      display: table;
      content: "";
  }
  
  .clearfix:after {
      clear: both
  }
</style>