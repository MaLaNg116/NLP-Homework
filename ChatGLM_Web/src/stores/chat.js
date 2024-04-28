import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat_content', () => {
    const chat_list = ref([
        {
            "content": "你好，我是你的人工智能助手，有什么可以帮你的吗？",
            "type": "good-bro",
        }])
    const isLoading = ref(false)
    const isUpdating =  ref(false)
    function increment(text, type) {
        chat_list.value.push({ "content": text, "type": type })
    }

    function update_last(text){
        chat_list.value[chat_list.value.length - 1].content += text
        isUpdating.value = !isUpdating.value
    }

    function loading() {
        isLoading.value = !isLoading.value
    }

    function set_loadingFalse(){
        isLoading.value = false
    }

    return { chat_list, isLoading, increment, loading, set_loadingFalse, update_last, isUpdating}
})