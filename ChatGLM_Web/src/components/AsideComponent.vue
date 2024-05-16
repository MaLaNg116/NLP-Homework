<script setup>
import {computed, watch} from "vue";
import {useConfigStore} from "@/stores/config.js";
import {useChatStore} from "@/stores/chat.js";
import {storeToRefs} from "pinia";
import {ElMessage, ElMessageBox} from 'element-plus'

const { use_stream, language, max_length, top_p, temperature, model, task, model_list, task_list } = storeToRefs(useConfigStore());
const { chat_list } = storeToRefs(useChatStore());

// 清空聊天记录，方便导出三元组
function tripleChat() {
  chat_list.value = [
    {
      "content": "<p>你好，我是你的常识知识三元组挖掘助手，请提供你需要处理的文本。</p>",
      "type": "good-bro",
    }]
}

// 恢复正常聊天模式
function normalChat() {
  chat_list.value = [
    {
      "content": "<p>你好，我是你的人工智能助手，有什么可以帮你的吗？</p>",
      "type": "good-bro",
    }]
}

watch(task, (value, oldValue) => {
  if (task.value != "ke1") {
    normalChat()
  }
  else{
    ElMessageBox.confirm(
        'Switch to Triads Mining task will causes the history to be deleted. Continue?',
        'Warning',
        {
          confirmButtonText: 'OK',
          cancelButtonText: 'Cancel',
          type: 'warning',
        }
    )
        .then(() => {
          ElMessage({
            type: 'success',
            message: 'Switch completed',
          })
          tripleChat()
        })
        .catch(() => {
          ElMessage({
            type: 'info',
            message: 'Switch canceled',
          })
          task.value = oldValue
        })
  }
})

//控制导出按钮
const export_button = computed(() => {
  return task.value == "ke1"
})

// 导出JSON
function exportJSON() {
  if (chat_list.value.length === 1) {
    ElMessage({
      message: 'No data to export',
      type: 'warning',
    })
  }
  else{
    let data = chat_list.value.filter((item, index) => index !== 0)
    // 定义正则表达式
    const pattern = /<pre><code class="json language-json">(.*?)<\/code><\/pre>/s;
    // 匹配并提取三元组
    let full_data = []
    data.map((item) => {
      if ((item.type === 'good-bro') && (pattern.exec(item.content))){
        console.log(pattern.exec(item.content)[1])
        const match = JSON.parse(pattern.exec(item.content)[1]);
        if (match) {
          if (match["Triad"]){
            match["Triad"].map((item) => {
              full_data.push(item)
            })
          }
          else if(match["Trial"]){
            match["Trial"].map((item) => {
              full_data.push(item)
            })
          }
        }
      }
    });
    console.log(full_data)
    // 创建隐藏的可下载链接
    const a = document.createElement('a');
    a.style.display = 'none';
    document.body.appendChild(a);
    const blob = new Blob([JSON.stringify(full_data)], {type: 'application/json'});
    a.href = URL.createObjectURL(blob);
    a.download = 'Triads.json';
    a.click();
  }
}

</script>

<template>
    <div class="box-card">
      <div class="use-stream">
        <el-switch
            v-model="use_stream"
            size="large"
            inline-prompt
            style="--el-switch-on-color: #91c885; --el-switch-off-color: #fd9d9e"
            active-text="Stream"
            inactive-text="No Stream"
        />
        <el-switch
            v-model="language"
            size="large"
            inline-prompt
            style="--el-switch-on-color: #91c885; --el-switch-off-color: #fd9d9e"
            active-text="Chinese"
            inactive-text="English"
        />
      </div>
      <div class="max-length">
        <span class="demonstration">max_length</span>
        <el-slider v-model="max_length" :size="'small'" :max="32768"/>
      </div>
      <div class="top-p">
        <span class="demonstration">top_p</span>
        <el-slider v-model="top_p" :size="'small'" :max="1.00" :step="0.01"/>
      </div>
      <div class="temperature">
        <span class="demonstration">temperature</span>
        <el-slider v-model="temperature" :size="'small'" :max="1.00" :step="0.01"/>
      </div>
      <div class="model">
        <p>model</p>
        <el-select
            v-model="model"
            placeholder="Select"
            style="width: 240px"
        >
          <el-option
              v-for="item in model_list"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
      </div>
      <div class="mission">
        <p>task name</p>
        <el-select
            v-model="task"
            placeholder="Select"
            style="width: 240px"
        >
          <el-option
              v-for="item in task_list"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
          <template #footer>
            <span>Coming soon...</span>
          </template>
        </el-select>
      </div>
      <div class="export-json">
        <el-button @click="exportJSON" v-show="export_button" type="primary" plain>Export JSON</el-button>
      </div>
    </div>
</template>

<style scoped>
.box-card {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  padding: 10px;
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 0.5fr 0.5fr 0.5fr 0.5fr 0.5fr 1fr 1fr;
  grid-template-areas:
  "use-stream"
  "max-length"
  "top-p"
  "temperature"
  "model"
  "mission"
  "export-json";

  .use-stream {
    padding: 5px 20px;
    grid-area: use-stream;
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
  }

  .el-slider {
    --el-slider-main-bg-color: #fd9d9e;
    --el-slider-runway-bg-color: #91c885;
  }

  .max-length {
    padding: 5px 20px;
    align-items: center;
    grid-area: max-length;
  }

  .top-p {
    padding: 5px 20px;
    align-items: center;
    grid-area: top-p;
  }

  .temperature {
    padding: 5px 20px;
    align-items: center;
    grid-area: temperature;
  }

  .model {
    padding: 5px 20px;
    align-items: center;
    grid-area: model;
  }

  .mission {
    padding: 5px 20px;
    align-items: center;
    grid-area: mission;
  }

  .export-json {
    padding: 5px 20px;
    display: flex;
    align-items: center;
    grid-area: export-json;
    justify-content: center;
  }
}

.box-card::-webkit-scrollbar {
  display: none;
}
</style>