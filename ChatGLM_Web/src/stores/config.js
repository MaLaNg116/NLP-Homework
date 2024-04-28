import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useConfigStore = defineStore('configs', () => {
    const use_stream = ref(false)
    const language = ref(true)
    const max_length = ref(8192)
    const top_p = ref(0.80)
    const temperature = ref(0.80)
    const model = ref('GPT-3.5')
    const model_list = ref([
        {
            value: 'GPT-3.5',
            label: 'GPT-3.5-turbo',
        },
        {
            value: 'GLM-3',
            label: 'ChatGLM3-6b',
        }
    ])
    const task = ref('Triads Mining')
    const task_list = ref([
        {
            value: 'dialogue_scoring',
            label: 'Dialogue Scoring',
        },
        {
            value: 'ke1',
            label: 'Triads Mining',
        }
    ])

    return { use_stream, language, max_length, top_p, temperature, model, model_list, task, task_list }
})