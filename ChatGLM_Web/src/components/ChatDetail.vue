<script setup>
import {computed, ref} from "vue";
import GPT_Avatar from "@/assets/gpt_avatar.png"
import me_Avatar from "@/assets/my_avatar.png"

const data = defineProps(['content', 'type'])
const isGoodBro = computed(() => data.type === 'good-bro')
const fit = ref('fill')
const size = ref(43)
</script>

<template>
  <div v-if="isGoodBro" class="good-bro">
    <el-avatar :size="size" :fit='fit' :src="GPT_Avatar" shape='square'>
    </el-avatar>
    <div class="chat-content">
      {{data.content}}
    </div>
  </div>
  <div v-if="!isGoodBro" class="me">
    <div class="chat-content">
      {{data.content}}
    </div>
    <el-avatar :size="size" :fit='fit' :src="me_Avatar" shape='square'>
    </el-avatar>
  </div>
</template>

<style scoped>
.good-bro {
  padding-left: 30px;
  width: 100%;
  height: auto;
  display: flex;
  justify-content: flex-start;
  align-items: stretch;

  .chat-content{
    white-space: pre-wrap;
    padding: 10px 15px;
    max-width: 400px;
    margin-left: 10px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
}

.me {
  padding-right: 30px;
  width: 100%;
  height: auto;
  display: flex;
  justify-content: flex-end;
  align-items: stretch;

  .chat-content{
    padding: 10px 15px;
    max-width: 400px;
    margin-right: 10px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
}
</style>