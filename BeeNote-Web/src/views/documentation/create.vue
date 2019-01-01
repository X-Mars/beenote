<template>
  <div>
    <el-container>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-input
              size="medium"
              placeholder="请输入文章题目"
              v-model="noteData.title">
            </el-input>
          </el-col>

          <el-col v-if="notEdit" :span="4">
            <el-select
              v-model="noteData.notebook"
              allow-create
              default-first-option
              placeholder="请选择笔记本">
              <el-option
                v-for="note in notebookInfo"
                :key="note.id"
                :label="note.name"
                :value="note.id">
              </el-option>
            </el-select>
          </el-col>
          <el-col v-if="notEdit" :span="2">
            <el-button type="primary" @click="createNote()">保存</el-button>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
          <mavon-editor v-if="noteData.type == 'markdown' && notEdit" style="height: 1000px" v-model="noteData.text" :subfield="false" defaultOpen='edit' @save="createNote"/>
          <mavon-editor v-if="noteData.type == 'markdown' && !notEdit" style="height: 100px" v-model="noteData.text" :subfield="false" defaultOpen='preview' :toolbars='{}'/>
          <tinymce v-else-if="noteData.type == 'text' && notEdit" :height="1000" v-model="noteData.text"/>
          <div v-else-if="noteData.type == 'text' && !notEdit" class="editor-content" v-html="noteData.text"/>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import { getNoteBookBase, createNote } from '@/api/bee'
import Tinymce from '@/components/Tinymce'
var mavonEditor = require('mavon-editor')
import 'mavon-editor/dist/css/index.css'

export default {
  name: 'Notebook',
  components: {
    'mavon-editor': mavonEditor.mavonEditor,
    Tinymce
    },
  computed: {
    ...mapGetters([
      'notebook_info',
      'userId'
    ])
  },
  data() {
    return {
      selected_notebook: [],
      notebookId: -1,
      noteData: {
      },
      inputStatus: true,
      notEdit: true,
      beforeEditNoteData: {},
      noteType: '',
      notebookInfo: [],
      
    }
  },
  mounted(){
    console.log(this.userId)
    this.noteData.type = this.$route.params['noteType']
    console.log('noteType')
    console.log(this.noteData.type)
    // 关闭侧边栏
    this.$store.dispatch('closeSideBar', false)
    // 设置标签名称
    if(this.noteData.type == 'text'){
      this.$route.meta.title = '新建普通笔记'   
    }else if (this.noteData.type == 'markdown'){
      this.$route.meta.title = '新建markdown笔记'   
    }
    this.$store.dispatch('editVisitedViews', this.$route)
    // console.log(this.notebook_info)


    // 从后台获取笔记本信息（包含笔记），并将笔记本添加到下拉框。
    getNoteBookBase().then(res => {
      this.notebookInfo = res.data
      console.log(this.notebookInfo)
    })

  },
  methods: {
    createNote(){
      
      var dateTimeNow = new Date();
      this.noteData['create_time'] = dateTimeNow
      this.noteData['update_time'] = dateTimeNow
      this.noteData['user'] = this.userId
      createNote(this.noteData).then(res => {
        console.log(res.data)
        if(res.status == 201){
          this.$message({
            message: '《' + this.noteData.title + '》' + ' 已经保存。',
            type: 'success'
          });
          this.$router.push({
            path:'/meum/notebook/' + res.data.notebook,
          })
        }else {
          this.$message({
            message: '《' + this.noteData.title + '》' + ' 保存失败！',
            type: 'error'
          });
        }
      })
    }
  }
}
</script>

<style>
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }

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

  .card-class:hover {
    background:#D8D8D8;
  }
  
  .card-class:focus {
    background:#D8D8D8;
  }

</style>