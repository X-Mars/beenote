<template>
  <div class="oauth-config-container">
    <el-tabs v-model="activeTab">
      <!-- 企业微信配置 -->
      <el-tab-pane label="企业微信配置" name="wecom">
        <div class="config-tips">
          <p>配置说明：</p>
          <p>1. 请先前往 <el-link href="https://work.weixin.qq.com/wework_admin/frame#profile" type="primary" target="_blank">企业微信管理后台</el-link> 获取相关配置</p>
          <p>2. 回调域名请填写：{{ baseUrl }}/oauth/callback</p>
          <p>3. 授权范围请选择：企业内部开发 - 通讯录</p>
        </div>

        <div class="tab-header">
          <el-button 
            type="primary" 
            @click="handleAdd('wecom')"
            :disabled="wecomConfigs.length >= 1"
          >
            <el-icon><Plus /></el-icon>新建配置
          </el-button>
        </div>
        
        <el-table :data="wecomConfigs" v-loading="loading.wecom">
          <el-table-column prop="corp_id" label="企业ID"  width="300" />
          <el-table-column prop="agent_id" label="应用ID"  width="200" />
          <el-table-column prop="secret" label="应用密钥" show-overflow-tooltip />
          <el-table-column prop="redirect_uri" label="回调域名" show-overflow-tooltip>
            <template #default="{ row }">
              <el-link 
                type="primary" 
                :href="row.redirect_uri" 
                target="_blank"
                :underline="false"
              >
                {{ row.redirect_uri }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="enabled" label="状态" width="100">
            <template #default="{ row }">
              <el-switch
                v-model="row.enabled"
                @change="handleStatusChange('wecom', row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" :icon="Edit" @click="handleEdit('wecom', row)">
                  编辑
                </el-button>
                <el-button type="danger" :icon="Delete" @click="handleDelete('wecom', row)">
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 飞书配置 -->
      <el-tab-pane label="飞书配置" name="feishu">
        <div class="config-tips">
          <p>配置说明：</p>
          <p>1. 请先前往 <el-link href="https://open.feishu.cn/app" type="primary" target="_blank">飞书开放平台</el-link> 获取相关配置</p>
          <p>2. 回调域名请填写：{{ baseUrl }}/oauth/callback</p>
          <p>3. 权限请选择：获取用户基本信息</p>
        </div>

        <div class="tab-header">
          <el-button 
            type="primary" 
            @click="handleAdd('feishu')"
            :disabled="feishuConfigs.length >= 1"
          >
            <el-icon><Plus /></el-icon>新建配置
          </el-button>
        </div>
        
        <el-table :data="feishuConfigs" v-loading="loading.feishu">
          <el-table-column prop="app_id" label="应用ID" />
          <el-table-column prop="app_secret" label="应用密钥" show-overflow-tooltip />
          <el-table-column prop="redirect_uri" label="回调域名" show-overflow-tooltip>
            <template #default="{ row }">
              <el-link 
                type="primary" 
                :href="row.redirect_uri" 
                target="_blank"
                :underline="false"
              >
                {{ row.redirect_uri }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="enabled" label="状态" width="100">
            <template #default="{ row }">
              <el-switch
                v-model="row.enabled"
                @change="handleStatusChange('feishu', row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" :icon="Edit" @click="handleEdit('feishu', row)">
                  编辑
                </el-button>
                <el-button type="danger" :icon="Delete" @click="handleDelete('feishu', row)">
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 钉钉配置 -->
      <el-tab-pane label="钉钉配置" name="dingtalk">
        <div class="config-tips">
          <p>配置说明：</p>
          <p>1. 请先前往 <el-link href="https://open-dev.dingtalk.com/fe/app#/corp/app" type="primary" target="_blank">钉钉开放平台</el-link> 获取相关配置</p>
          <p>2. 回调域名请填写：{{ baseUrl }}/oauth/callback</p>
          <p>3. 权限请选择：通讯录个人信息读权限</p>
        </div>

        <div class="tab-header">
          <el-button 
            type="primary" 
            @click="handleAdd('dingtalk')"
            :disabled="dingtalkConfigs.length >= 1"
          >
            <el-icon><Plus /></el-icon>新建配置
          </el-button>
        </div>
        
        <el-table :data="dingtalkConfigs" v-loading="loading.dingtalk">
          <el-table-column prop="app_id" label="APP ID" width="350" />
          <el-table-column prop="client_id" label="Client ID" width="200" />
          <el-table-column prop="client_secret" label="Client Secret" show-overflow-tooltip />
          <el-table-column prop="redirect_uri" label="回调域名" show-overflow-tooltip>
            <template #default="{ row }">
              <el-link 
                type="primary" 
                :href="row.redirect_uri" 
                target="_blank"
                :underline="false"
              >
                {{ row.redirect_uri }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="enabled" label="状态" width="100">
            <template #default="{ row }">
              <el-switch
                v-model="row.enabled"
                @change="handleStatusChange('dingtalk', row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" :icon="Edit" @click="handleEdit('dingtalk', row)">
                  编辑
                </el-button>
                <el-button type="danger" :icon="Delete" @click="handleDelete('dingtalk', row)">
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- GitHub配置 -->
      <el-tab-pane label="GitHub配置" name="github">
        <div class="config-tips">
          <p>配置说明：</p>
          <p>1. 请先前往 <el-link href="https://github.com/settings/developers" type="primary" target="_blank">GitHub开发者设置</el-link> 获取相关配置</p>
          <p>2. 回调域名请填写：{{ baseUrl }}/oauth/callback</p>
          <p>3. 权限范围请选择：read:user, user:email</p>
        </div>

        <div class="tab-header">
          <el-button 
            type="primary" 
            @click="handleAdd('github')"
            :disabled="githubConfigs.length >= 1"
          >
            <el-icon><Plus /></el-icon>新建配置
          </el-button>
        </div>
        
        <el-table :data="githubConfigs" v-loading="loading.github">
          <el-table-column prop="client_id" label="Client ID"/>
          <el-table-column prop="client_secret" label="Client Secret" show-overflow-tooltip />
          <el-table-column prop="redirect_uri" label="回调域名" show-overflow-tooltip>
            <template #default="{ row }">
              <el-link 
                type="primary" 
                :href="row.redirect_uri" 
                target="_blank"
                :underline="false"
              >
                {{ row.redirect_uri }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="enabled" label="状态" width="100">
            <template #default="{ row }">
              <el-switch
                v-model="row.enabled"
                @change="handleStatusChange('github', row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" :icon="Edit" @click="handleEdit('github', row)">
                  编辑
                </el-button>
                <el-button type="danger" :icon="Delete" @click="handleDelete('github', row)">
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- Google配置 -->
      <el-tab-pane label="Google配置" name="google">
        <div class="config-tips">
          <p>配置说明：</p>
          <p>1. 请先前往 <el-link href="https://console.cloud.google.com/apis/credentials" type="primary" target="_blank">Google Cloud Console</el-link> 获取相关配置</p>
          <p>2. 回调域名请填写：{{ baseUrl }}/oauth/callback</p>
          <p>3. 权限范围请选择：openid, email, profile</p>
        </div>

        <div class="tab-header">
          <el-button 
            type="primary" 
            @click="handleAdd('google')"
            :disabled="googleConfigs.length >= 1"
          >
            <el-icon><Plus /></el-icon>新建配置
          </el-button>
        </div>
        
        <el-table :data="googleConfigs" v-loading="loading.google">
          <el-table-column prop="client_id" label="Client ID"/>
          <el-table-column prop="client_secret" label="Client Secret" show-overflow-tooltip />
          <el-table-column prop="redirect_uri" label="回调域名" show-overflow-tooltip>
            <template #default="{ row }">
              <el-link 
                type="primary" 
                :href="row.redirect_uri" 
                target="_blank"
                :underline="false"
              >
                {{ row.redirect_uri }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="enabled" label="状态" width="100">
            <template #default="{ row }">
              <el-switch
                v-model="row.enabled"
                @change="handleStatusChange('google', row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" :icon="Edit" @click="handleEdit('google', row)">
                  编辑
                </el-button>
                <el-button type="danger" :icon="Delete" @click="handleDelete('google', row)">
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- GitLab配置 -->
      <el-tab-pane label="GitLab配置" name="gitlab">
        <div class="config-tips">
          <p>配置说明：</p>
          <p>1. 请先前往 GitLab 实例的应用设置页面获取相关配置（对于公共 GitLab，地址为：<el-link href="https://gitlab.com/-/profile/applications" type="primary" target="_blank">GitLab 应用设置</el-link>）</p>
          <p>2. 回调域名请填写：{{ baseUrl }}/oauth/callback</p>
          <p>3. 权限范围请选择：api, read_user, profile, email</p>
          <p>4. 对于私有化部署的 GitLab，请填写完整的 GitLab 服务器地址（例如：https://gitlab.example.com）</p>
        </div>

        <div class="tab-header">
          <el-button 
            type="primary" 
            @click="handleAdd('gitlab')"
            :disabled="gitlabConfigs.length >= 1"
          >
            <el-icon><Plus /></el-icon>新建配置
          </el-button>
        </div>
        
        <el-table :data="gitlabConfigs" v-loading="loading.gitlab">
          <el-table-column prop="client_id" label="Client ID"/>
          <el-table-column prop="client_secret" label="Client Secret" show-overflow-tooltip />
          <el-table-column prop="redirect_uri" label="回调域名" show-overflow-tooltip>
            <template #default="{ row }">
              <el-link 
                type="primary" 
                :href="row.redirect_uri" 
                target="_blank"
                :underline="false"
              >
                {{ row.redirect_uri }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="enabled" label="状态" width="100">
            <template #default="{ row }">
              <el-switch
                v-model="row.enabled"
                @change="handleStatusChange('gitlab', row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" :icon="Edit" @click="handleEdit('gitlab', row)">
                  编辑
                </el-button>
                <el-button type="danger" :icon="Delete" @click="handleDelete('gitlab', row)">
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- Gitee配置 -->
      <el-tab-pane label="Gitee配置" name="gitee">
        <div class="config-tips">
          <p>配置说明：</p>
          <p>1. 请先前往 <el-link href="https://gitee.com/oauth/applications" type="primary" target="_blank">Gitee应用管理</el-link> 获取相关配置</p>
          <p>2. 回调域名请填写：{{ baseUrl }}/oauth/callback</p>
          <p>3. 权限范围请选择：user_info, emails</p>
        </div>

        <div class="tab-header">
          <el-button 
            type="primary" 
            @click="handleAdd('gitee')"
            :disabled="giteeConfigs.length >= 1"
          >
            <el-icon><Plus /></el-icon>新建配置
          </el-button>
        </div>
        
        <el-table :data="giteeConfigs" v-loading="loading.gitee">
          <el-table-column prop="client_id" label="Client ID"/>
          <el-table-column prop="client_secret" label="Client Secret" show-overflow-tooltip />
          <el-table-column prop="redirect_uri" label="回调域名" show-overflow-tooltip>
            <template #default="{ row }">
              <el-link 
                type="primary" 
                :href="row.redirect_uri" 
                target="_blank"
                :underline="false"
              >
                {{ row.redirect_uri }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="enabled" label="状态" width="100">
            <template #default="{ row }">
              <el-switch
                v-model="row.enabled"
                @change="handleStatusChange('gitee', row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" :icon="Edit" @click="handleEdit('gitee', row)">
                  编辑
                </el-button>
                <el-button type="danger" :icon="Delete" @click="handleDelete('gitee', row)">
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- 配置表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="formTitle"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
      >
        <template v-if="activeTab === 'wecom'">
          <el-form-item label="企业ID" prop="corp_id">
            <el-input v-model="form.corp_id" />
          </el-form-item>
          <el-form-item label="应用ID" prop="agent_id">
            <el-input v-model="form.agent_id" />
          </el-form-item>
          <el-form-item label="应用密钥" prop="secret">
            <el-input v-model="form.secret" type="password" show-password />
          </el-form-item>
          <el-form-item label="回调域名" prop="redirect_uri">
            <el-input 
              v-model="form.redirect_uri" 
              placeholder="留空将自动使用当前域名"
            />
          </el-form-item>
        </template>

        <template v-if="activeTab === 'feishu'">
          <el-form-item label="应用ID" prop="app_id">
            <el-input v-model="form.app_id" />
          </el-form-item>
          <el-form-item label="应用密钥" prop="app_secret">
            <el-input v-model="form.app_secret" type="password" show-password />
          </el-form-item>
          <el-form-item label="回调域名" prop="redirect_uri">
            <el-input 
              v-model="form.redirect_uri" 
              placeholder="留空将自动使用当前域名"
            />
          </el-form-item>
        </template>

        <template v-if="activeTab === 'dingtalk'">
          <el-form-item label="Client ID" prop="client_id">
            <el-input v-model="form.client_id" />
          </el-form-item>
          <el-form-item label="Client Secret" prop="client_secret">
            <el-input v-model="form.client_secret" type="password" show-password />
          </el-form-item>
          <el-form-item label="APP ID" prop="app_id">
            <el-input v-model="form.app_id" />
          </el-form-item>
          <el-form-item label="回调域名" prop="redirect_uri">
            <el-input 
              v-model="form.redirect_uri" 
              placeholder="留空将自动使用当前域名"
            />
          </el-form-item>
        </template>

        <template v-if="activeTab === 'github'">
          <el-form-item label="Client ID" prop="client_id">
            <el-input v-model="form.client_id" />
          </el-form-item>
          <el-form-item label="Client Secret" prop="client_secret">
            <el-input v-model="form.client_secret" type="password" show-password />
          </el-form-item>
          <el-form-item label="回调域名" prop="redirect_uri">
            <el-input 
              v-model="form.redirect_uri" 
              placeholder="留空将自动使用当前域名"
            />
          </el-form-item>
        </template>

        <template v-if="activeTab === 'google'">
          <el-form-item label="Client ID" prop="client_id">
            <el-input v-model="form.client_id" />
          </el-form-item>
          <el-form-item label="Client Secret" prop="client_secret">
            <el-input v-model="form.client_secret" type="password" show-password />
          </el-form-item>
          <el-form-item label="回调域名" prop="redirect_uri">
            <el-input 
              v-model="form.redirect_uri" 
              placeholder="留空将自动使用当前域名"
            />
          </el-form-item>
        </template>

        <template v-if="activeTab === 'gitlab'">
          <el-form-item label="GitLab 地址" prop="gitlab_server">
            <el-input
              v-model="form.gitlab_server"
              placeholder="例如：https://gitlab.example.com"
            />
          </el-form-item>
          <el-form-item label="Client ID" prop="client_id">
            <el-input v-model="form.client_id" />
          </el-form-item>
          <el-form-item label="Client Secret" prop="client_secret">
            <el-input v-model="form.client_secret" type="password" show-password />
          </el-form-item>
          <el-form-item label="回调域名" prop="redirect_uri">
            <el-input 
              v-model="form.redirect_uri" 
              placeholder="留空将自动使用当前域名"
            />
          </el-form-item>
        </template>

        <template v-if="activeTab === 'gitee'">
          <el-form-item label="Client ID" prop="client_id">
            <el-input v-model="form.client_id" />
          </el-form-item>
          <el-form-item label="Client Secret" prop="client_secret">
            <el-input v-model="form.client_secret" type="password" show-password />
          </el-form-item>
          <el-form-item label="回调域名" prop="redirect_uri">
            <el-input 
              v-model="form.redirect_uri" 
              placeholder="留空将自动使用当前域名"
            />
          </el-form-item>
        </template>

        <el-form-item label="状态" prop="enabled">
          <el-switch v-model="form.enabled" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { configApi } from '@/api/config'
import type { WeComConfig, FeiShuConfig, DingTalkConfig, GitHubConfig, GoogleConfig, GitLabConfig, GiteeConfig } from '@/api/config'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

// 检查权限
if (userStore.user?.role !== 'superuser') {
  ElMessage.error('只有超级管理员可以访问此页面')
  router.push('/')
}

const activeTab = ref('wecom')
const dialogVisible = ref(false)
const submitting = ref(false)
const currentConfig = ref<any>(null)
const formRef = ref<FormInstance>()

const wecomConfigs = ref<WeComConfig[]>([])
const feishuConfigs = ref<FeiShuConfig[]>([])
const dingtalkConfigs = ref<DingTalkConfig[]>([])
const githubConfigs = ref<GitHubConfig[]>([])
const googleConfigs = ref<GoogleConfig[]>([])
const gitlabConfigs = ref<GitLabConfig[]>([])
const giteeConfigs = ref<GiteeConfig[]>([])

const loading = ref({
  wecom: false,
  feishu: false,
  dingtalk: false,
  github: false,
  google: false,
  gitlab: false,
  gitee: false
} as const)

const form = ref<any>({
  corp_id: '',
  agent_id: '',
  secret: '',
  app_id: '',
  app_secret: '',
  client_id: '',
  client_secret: '',
  redirect_uri: '',
  gitlab_server: 'https://gitlab.com',
  enabled: true
})

// 表单标题
const formTitle = computed(() => {
  const action = currentConfig.value ? '编辑' : '新建'
  const type = {
    wecom: '企业微信',
    feishu: '飞书',
    dingtalk: '钉钉',
    github: 'GitHub',
    google: 'Google',
    gitlab: 'GitLab',
    gitee: 'Gitee'
  }[activeTab.value]
  return `${action}${type}配置`
})

// 表单验证规则
const rules = {
  corp_id: [{ required: true, message: '请输入企业ID', trigger: 'blur' }],
  agent_id: [{ required: true, message: '请输入应用ID', trigger: 'blur' }],
  secret: [{ required: true, message: '请输入应用密钥', trigger: 'blur' }],
  app_id: [{ required: true, message: '请输入应用ID', trigger: 'blur' }],
  app_secret: [{ required: true, message: '请输入应用密钥', trigger: 'blur' }],
  client_id: [{ required: true, message: '请输入Client ID', trigger: 'blur' }],
  client_secret: [{ required: true, message: '请输入Client Secret', trigger: 'blur' }]
}

// 加载配置数据
const fetchConfigs = async () => {
  try {
    loading.value[activeTab.value as keyof typeof loading.value] = true
    switch (activeTab.value) {
      case 'wecom': {
        const wecomRes = await configApi.getWeComConfigs()
        wecomConfigs.value = wecomRes.data
        break
      }
      case 'feishu': {
        const feishuRes = await configApi.getFeiShuConfigs()
        feishuConfigs.value = feishuRes.data
        break
      }
      case 'dingtalk': {
        const dingtalkRes = await configApi.getDingTalkConfigs()
        dingtalkConfigs.value = dingtalkRes.data
        break
      }
      case 'github': {
        const githubRes = await configApi.getGitHubConfigs()
        githubConfigs.value = githubRes.data
        break
      }
      case 'google': {
        const googleRes = await configApi.getGoogleConfigs()
        googleConfigs.value = googleRes.data
        break
      }
      case 'gitlab': {
        const gitlabRes = await configApi.getGitLabConfigs()
        gitlabConfigs.value = gitlabRes.data
        break
      }
      case 'gitee': {
        const giteeRes = await configApi.getGiteeConfigs()
        giteeConfigs.value = giteeRes.data
        break
      }
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('获取配置列表失败')
  } finally {
    loading.value[activeTab.value as keyof typeof loading.value] = false
  }
}

// 重置表单
const resetForm = () => {
  form.value = {
    corp_id: '',
    agent_id: '',
    secret: '',
    app_id: '',
    app_secret: '',
    client_id: '',
    client_secret: '',
    redirect_uri: '',
    gitlab_server: 'https://gitlab.com',
    enabled: true
  }
  currentConfig.value = null
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 新建配置
const handleAdd = (type: string) => {
  activeTab.value = type
  resetForm()
  dialogVisible.value = true
}

// 编辑配置
const handleEdit = (type: string, row: any) => {
  activeTab.value = type
  currentConfig.value = row
  Object.assign(form.value, row)
  dialogVisible.value = true
}

// 删除配置
const handleDelete = async (type: string, row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该配置吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    switch (type) {
      case 'wecom':
        await configApi.deleteWeComConfig(row.id)
        break
      case 'feishu':
        await configApi.deleteFeiShuConfig(row.id)
        break
      case 'dingtalk':
        await configApi.deleteDingTalkConfig(row.id)
        break
      case 'github':
        await configApi.deleteGitHubConfig(row.id)
        break
      case 'google':
        await configApi.deleteGoogleConfig(row.id)
        break
      case 'gitlab':
        await configApi.deleteGitLabConfig(row.id)
        break
      case 'gitee':
        await configApi.deleteGiteeConfig(row.id)
        break
    }

    ElMessage.success('删除成功')
    fetchConfigs()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
      ElMessage.error('删除失败')
    }
  }
}

// 更新状态
const handleStatusChange = async (type: string, row: any) => {
  try {
    const data = { enabled: row.enabled }
    switch (type) {
      case 'wecom':
        await configApi.updateWeComConfig(row.id, data)
        break
      case 'feishu':
        await configApi.updateFeiShuConfig(row.id, data)
        break
      case 'dingtalk':
        await configApi.updateDingTalkConfig(row.id, data)
        break
      case 'github':
        await configApi.updateGitHubConfig(row.id, data)
        break
      case 'google':
        await configApi.updateGoogleConfig(row.id, data)
        break
      case 'gitlab':
        await configApi.updateGitLabConfig(row.id, data)
        break
      case 'gitee':
        await configApi.updateGiteeConfig(row.id, data)
        break
    }
    ElMessage.success('更新状态成功')
  } catch (error) {
    console.error(error)
    ElMessage.error('更新状态失败')
    row.enabled = !row.enabled
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const data = { ...form.value }
        
        // 如果回调域名为空，自动填充当前域名
        if (!data.redirect_uri) {
          data.redirect_uri = `${baseUrl.value}/oauth/callback`
        }
        
        if (currentConfig.value) {
          // 更新
          switch (activeTab.value) {
            case 'wecom':
              await configApi.updateWeComConfig(currentConfig.value.id, data)
              break
            case 'feishu':
              await configApi.updateFeiShuConfig(currentConfig.value.id, data)
              break
            case 'dingtalk':
              await configApi.updateDingTalkConfig(currentConfig.value.id, data)
              break
            case 'github':
              await configApi.updateGitHubConfig(currentConfig.value.id, data)
              break
            case 'google':
              await configApi.updateGoogleConfig(currentConfig.value.id, data)
              break
            case 'gitlab':
              await configApi.updateGitLabConfig(currentConfig.value.id, data)
              break
            case 'gitee':
              await configApi.updateGiteeConfig(currentConfig.value.id, data)
              break
          }
          ElMessage.success('更新成功')
        } else {
          // 创建
          switch (activeTab.value) {
            case 'wecom':
              await configApi.createWeComConfig(data)
              break
            case 'feishu':
              await configApi.createFeiShuConfig(data)
              break
            case 'dingtalk':
              await configApi.createDingTalkConfig(data)
              break
            case 'github':
              await configApi.createGitHubConfig(data)
              break
            case 'google':
              await configApi.createGoogleConfig(data)
              break
            case 'gitlab':
              await configApi.createGitLabConfig(data)
              break
            case 'gitee':
              await configApi.createGiteeConfig(data)
              break
          }
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchConfigs()
      } catch (error) {
        console.error(error)
        ElMessage.error('保存失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

// 监听标签页切换
watch(activeTab, () => {
  fetchConfigs()
})

// 初始化
onMounted(() => {
  fetchConfigs()
})

// 获取当前域名
const baseUrl = computed(() => {
  return window.location.origin
})
</script>

<style scoped>
.oauth-config-container {
  padding: 20px;
}

.config-tips {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.config-tips p {
  margin: 8px 0;
  color: #606266;
  font-size: 14px;
}

.config-tips :deep(.el-link) {
  font-weight: bold;
}

.tab-header {
  margin-bottom: 20px;
}

:deep(.el-switch) {
  --el-switch-on-color: var(--el-color-success);
}
</style> 