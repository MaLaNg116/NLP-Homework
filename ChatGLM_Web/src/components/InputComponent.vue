<script setup>
import {ref, watch} from "vue";
import "Animate.css";
import {ElMessage} from "element-plus";
import {useChatStore} from "@/stores/chat.js";
import {useConfigStore} from "@/stores/config.js";
import {storeToRefs} from "pinia";
import axios from "axios";
import {fetchEventSource} from '@microsoft/fetch-event-source';

const URL = "http://127.0.0.1:5000"

const { use_stream, language, max_length, top_p, temperature, model, task } = storeToRefs(useConfigStore());

const chatStore = useChatStore();

const content = ref('');
const isValue = ref(false);

const handleInput = (event) => {
  content.value = event.target.innerText;
}

watch(content, (newValue) => {
  if (newValue !== '') {
    isValue.value = true;
  } else {
    isValue.value = false;
  }
})

// 三元组挖掘函数（不使用流）
async function triadsMiningNoStream() {
  await axios.post(URL + '/ke1',
      {
        "src_text": content.value,
        "model": model.value,
        "language": ((language.value === true) ? "Chinese" : "English"),
        "stream": use_stream.value,
        "max_length": max_length.value,
        "temperature": temperature.value,
        "top_p": top_p.value
      }
  ).then((res) => {
    chatStore.increment(res.data.data.result, 'good-bro');
    chatStore.loading()
  }).catch((err) => {
    console.log(err);
    ElMessage({
      message: 'Oops! Something went wrong.',
      type: 'error',
    })
    chatStore.loading()
  })
}

// 三元组挖掘函数（使用流）
function triadsMiningStream() {
  chatStore.increment("", "good-bro")
  fetchEventSource(URL + `/ke1`, {
    method: 'POST',
    headers: {
      "Content-Type": "application/json"
    },
    //请求体，用于给后台的数据
    body: JSON.stringify({
      "src_text": content.value,
      "model": model.value,
      "language": ((language.value === true) ? "Chinese" : "English"),
      "stream": use_stream.value,
      "max_length": max_length.value,
      "temperature": temperature.value,
      "top_p": top_p.value
    }),
    onmessage(event) {
      //服务返回的数据
      console.log(event.data)
      chatStore.update_last(event.data)
    },
    onerror(event) {
      // 服务异常
      console.log("服务异常", event)
      chatStore.set_loadingFalse()
    },
    onclose() {
      // 服务关闭
      console.log("服务关闭");
      chatStore.set_loadingFalse()
    },
  })
}

// 发送消息
async function handleSend() {
  if (content.value !== '') {
    console.log(content.value);
    isValue.value = false;
    chatStore.increment(content.value, 'me');
    chatStore.loading()
    if (use_stream.value === false) {
      await triadsMiningNoStream()
    } else {
      await triadsMiningStream()
    }
  } else {
    ElMessage({
      message: '不能发送空消息哦',
      type: 'warning',
    })
  }
}

function clearContent() {
  content.value = '';
}

</script>

<template>
  <div class="input-container">
    <div contenteditable class="input-area" @input="handleInput" @keydown.enter="handleSend" @keyup.enter="clearContent"
         v-text="content"></div>
    <img class="animated-label" v-show="isValue" src="@/assets/send.png" alt="send_btn" @click="(()=>{
      handleSend()
      clearContent()
   })"/>
  </div>
</template>

<style scoped>
.input-container {
  padding: 10px 20px;
  min-height: 50px;
  max-height: 120px;
  width: 550px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: grid;
  grid-template-columns: 8fr 1fr;


  .input-area {
    width: 100%;
    margin-top: 2px;
    max-height: 100px;
    overflow-y: visible;
    overflow-x: hidden;
    word-wrap: break-word;
  }

  .input-area:focus {
    outline: none;
  }

  .input-area::-webkit-scrollbar {
    display: none;
  }

  img {
    justify-self: end;
    width: 30px;
    height: auto;
    cursor: pointer;
  }
}

@keyframes fadeInOut {
  0% {
    opacity: 0;
  }
  60% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.animated-label {
  transform: scale(1.8);
  transition: ease-in-out;
  animation: fadeInOut 1.8s infinite;
}

</style>