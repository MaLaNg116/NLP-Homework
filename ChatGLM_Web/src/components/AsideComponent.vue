<script setup>
import {useConfigStore} from "@/stores/config.js";
import {storeToRefs} from "pinia";

const { use_stream, language, max_length, top_p, temperature, model, task, model_list, task_list } = storeToRefs(useConfigStore());
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
  grid-template-rows: 0.5fr 0.5fr 0.5fr 0.5fr 0.5fr 2fr;
  grid-template-areas:
  "use-stream"
  "max-length"
  "top-p"
  "temperature"
  "model"
  "mission";

  .use-stream {
    padding: 5px 20px;
    grid-area: use-stream;
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
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
}

.box-card::-webkit-scrollbar {
  display: none;
}
</style>