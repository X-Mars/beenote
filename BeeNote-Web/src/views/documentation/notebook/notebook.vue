<template>
  <div>
    <el-container>
      <el-aside width="200px">
        <el-row>
          <el-col v-for="(note, nodeIndex) in selected_notebook.note" :key="note.id" :span="24">
            <el-card :body-style="{ padding: '0px' }" @click.native="noteData = note; changeNote(note.id, nodeIndex)" class="card-class">
              <div style="padding: 15px;">
                <span style="text-align: center;">{{ note.title }}</span>
                <div class="bottom clearfix">
                  <time class="time">{{ note.create_time }}</time>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-aside>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-input
              size="medium"
              v-model="noteData.title">
            </el-input>
          </el-col>
          <el-col :span="2">
            <el-button v-if="!notEdit" type="primary" @click="notEdit = true">编辑</el-button>
          </el-col>
          <el-col v-if="notEdit" :span="2">
            <el-button type="primary" @click="saveNote()">保存</el-button>
          </el-col>
          <el-col v-if="notEdit" :span="2">
            <el-button type="primary" @click="notEdit = false; noteData = Object.assign({}, beforeEditNoteData)">取消</el-button>
          </el-col>
        </el-row>
        <!-- <div class="markdown-editor"> -->
        <el-row :gutter="20">
          <el-col :span="24">
          <mavon-editor v-if="noteData.type == 'markdown' && notEdit" style="height: 1000px" v-model="noteData.text" :subfield="false" defaultOpen='edit' @save="saveNote"/>
          <mavon-editor v-if="noteData.type == 'markdown' && !notEdit" style="height: 100px" v-model="noteData.text" :subfield="false" defaultOpen='preview' :toolbars='{}'/>
          <tinymce v-else-if="noteData.type == 'text' && notEdit" :height="1000" v-model="noteData.text"/>
          <div v-else-if="noteData.type == 'text' && !notEdit" class="editor-content" v-html="noteData.text"/>
          </el-col>
        </el-row>
        <!-- </div> -->
      </el-main>
    </el-container>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import { getNoteBookById, saveNoteById, getNoteById } from '@/api/bee'
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
      'notebook_info'
    ])
  },
  data() {
    return {
      selected_notebook: [],
      notebookId: -1,
      noteData: {
      },
      inputStatus: true,
      notEdit: false,
      beforeEditNoteData: {}
    }
  },
  mounted(){
    this.notebookId = this.$route.params['notebookId']
    console.log('notebookId')
    console.log(this.notebookId)
    // 关闭侧边栏
    this.$store.dispatch('closeSideBar', false)
    // 设置标签名称
    this.$route.meta.title = this.notebookId
    this.$store.dispatch('editVisitedViews', this.$route)
    // console.log(this.notebook_info)

    // 如果已经从后台获取到了笔记本信息，直接遍历
    // 反之通过笔记本ID获取笔记本信息
    if(this.notebook_info.length > 0){
      for (var notebook_index in this.notebook_info){
        // console.log(this.notebook_info[notebook_index])
        if(this.notebook_info[notebook_index].id == this.notebookId){
          // console.log(this.notebook_info[notebook_index])
          // 设置已选中的笔记本
          this.selected_notebook = this.notebook_info[notebook_index]
          // 设置 已选中笔记本 中的 第一个笔记 默认打开笔记
          this.noteData = this.selected_notebook.note[0]
          this.beforeEditNoteData = Object.assign({}, this.selected_notebook.note[0])
          // 设置标签名称
          this.$route.meta.title = this.selected_notebook.note[0].title
          this.$store.dispatch('editVisitedViews', this.$route)
        }
      }
    }else {
      getNoteBookById(this.notebookId).then(res => {
        // 设置已选中的笔记本
        this.selected_notebook = res.data
        // 设置 已选中笔记本 中的 第一个笔记 默认打开笔记
        this.noteData = this.selected_notebook.note[0]
        this.beforeEditNoteData = Object.assign({}, this.selected_notebook.note[0])
        // 设置标签名称
        this.$route.meta.title = this.selected_notebook.note[0].title
        this.$store.dispatch('editVisitedViews', this.$route)
      })
    }

  },
  methods: {
    changeNote(noteId, nodeIndex){
      // 从后台通过笔记ID获取笔记内容
      getNoteById(noteId).then(res => {
        console.log(res.data)
        this.nodeIndex = nodeIndex
        // 设置已选中笔记的数据
        this.selected_notebook.note[nodeIndex] = res.data
        this.beforeEditNoteData = Object.assign({}, this.selected_notebook.note[0])
        // 设置标签名称
        this.$route.meta.title = res.data.title
        this.$store.dispatch('editVisitedViews', this.$route)
      })
      
    },

    saveNote(value, render){

      this.noteData['update_time'] = new Date()
      saveNoteById(this.noteData.id, this.noteData).then(res => {
        console.log(res)
        console.log(res.data)
        if(res.status == 200){
          this.$message({
            message: '《' + res.data.title + '》' + ' 更新成功。',
            type: 'success'
          });
          this.noteData = res.data
          this.notEdit = false
          // 设置已选中笔记的数据
          this.selected_notebook.note[this.nodeIndex] = res.data
          this.beforeEditNoteData = Object.assign({}, res.data)
        }else {
          this.$message({
            message: '《' + this.noteData.title + '》' + '更新失败！',
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