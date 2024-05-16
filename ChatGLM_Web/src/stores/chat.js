import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat_content', () => {
    const chat_list = ref([
        {
            "content": "<p>你好，我是你的常识知识三元组挖掘助手，请提供你需要处理的文本。</p>",
            "type": "good-bro",
        }])
    const isLoading = ref(false)
    const isUpdating =  ref(false)
    function increment(text, type) {
        chat_list.value.push({ "content": text, "type": type })
        console.log(text)
    }

    function update_last(text){
        chat_list.value[chat_list.value.length - 1].content = text
        isUpdating.value = !isUpdating.value
        console.log(text)
    }

    function loading() {
        isLoading.value = !isLoading.value
    }

    function set_loadingFalse(){
        isLoading.value = false
    }

    return { chat_list, isLoading, increment, loading, set_loadingFalse, update_last, isUpdating}
})