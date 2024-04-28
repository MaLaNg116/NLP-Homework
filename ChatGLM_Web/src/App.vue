<script setup>
import 'animate.css';
import {ref, watch} from "vue";
import AsideComponent from "@/components/AsideComponent.vue";
import InputComponent from "@/components/InputComponent.vue";
import ChatDetail from "@/components/ChatDetail.vue";
import {useChatStore} from "@/stores/chat.js";
import {storeToRefs} from "pinia";

const chat_box = ref(false);
setTimeout(() => {
  chat_box.value = true;
}, 600);

const { chat_list, isLoading, isUpdating } = storeToRefs(useChatStore());
const scrollContainer = ref(null);

watch(isLoading, () => {
  setTimeout(() => {
    scrollContainer.value.scrollTo({
      top: scrollContainer.value.scrollHeight,
      behavior: 'smooth'
    })
  }, 100)
})

// 处理流式输出下滑
let tmp = 0
watch(isUpdating, () => {
  tmp++
  if (tmp === 10){
    scrollContainer.value.scrollTo({
      top: scrollContainer.value.scrollHeight,
      behavior: 'smooth'
    })
    tmp = 0
  }
})
</script>

<template>
  <div class="container">
    <div v-if="chat_box" class="chat-box">
      <div class="header">
        <img src="@/assets/logo1.png" style="width:auto; height: 50px" alt="logo"/>
      </div>
      <div class="aside">
        <AsideComponent/>
      </div>
      <div class="main">
        <div class="text-area" ref="scrollContainer">
          <ChatDetail v-for="(item, index) in chat_list" :key="index" :content="item.content" :type="item.type"/>
          <div v-show="isLoading" class="loading">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
        <div class="input-area">
          <InputComponent/>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  height: 100vh;
  width: 100%;
  animation: fadeIn;
  animation-duration: 0.6s;
  background-image: url("@/assets/background.png");
  background-size: 100% 100%;
  display: flex;
  justify-content: center;
  align-items: center;

  .chat-box {
    animation: slideInDown;
    animation-duration: 0.6s;
    transition: ease-in-out;
    height: 80%;
    width: 65%;
    background-color: rgba(242, 242, 242, 0.95);
    border-radius: 10px;
    display: grid;
    grid-template-columns: 1.3fr 3fr;
    grid-template-rows: 0.5fr 4fr 1fr;
    grid-template-areas:
      "header header"
      "aside main"
      "aside main";

    .header {
      grid-area: header;
      border-radius: 10px 10px 0 0;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: rgba(6, 146, 120, 0.95);
    }

    .aside {
      grid-area: aside;
      border-radius: 0 0 0 10px;
    }

    .main {
      grid-area: main;
      border-radius: 0 0 10px 10px;
      display: grid;
      grid-template-columns: 1fr;
      grid-template-rows: 3fr 1fr;
      grid-template-areas:
        "text-area"
        "input-area";

      .text-area {
        max-height: 400px;
        padding-top: 40px;
        grid-area: text-area;
        border-radius: 0 0 0 10px;
        display: grid;
        grid-template-columns: 1fr;
        align-self: start;
        grid-gap: 30px;
        overflow-y: auto;

        .loading {
          padding: 20px;
          justify-self: center;
          display: flex;
          justify-content: space-between;
          width: 100px; /* 根据需要调整宽度 */

          .dot {
            width: 10px;
            height: 10px;
            background-color: rgb(40, 40, 40);
            border-radius: 50%;
            animation: dot-jump 1.2s infinite;
          }

          .dot:nth-child(2) {
            animation-delay: 0.4s; /* 第二个点的延迟 */
          }

          .dot:nth-child(3) {
            animation-delay: 0.8s; /* 第三个点的延迟 */
          }
        }
      }
      .text-area::-webkit-scrollbar {
        width: 4px; /* 滚动条宽度 */
        height: auto; /* 滚动条高度 */
      }

      .text-area::-webkit-scrollbar-thumb {
        border-radius: 5px; /* 滑块圆角 */
        background: #535353; /* 滑块背景色 */
        -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2); /* 滑块阴影 */
      }

      .text-area::-webkit-scrollbar-track {
        border-radius: 5px; /* 轨道圆角 */
        background: #EDEDED; /* 轨道背景色 */
        -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2); /* 轨道阴影 */
      }

      .input-area {
        grid-area: input-area;
        border-radius: 0 0 10px 10px;
        display: flex;
        justify-content: center;
        align-items: center;
      }
    }
  }
}

@keyframes dot-jump {
  0%, 60% {
    transform: translateY(0);
  }
  80% {
    transform: translateY(-10px); /* 调整跳动的距离 */
  }
  100% {
    transform: translateY(0);
  }
}
</style>
