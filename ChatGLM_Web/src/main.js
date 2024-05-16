import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

//导入函数
import hljs from 'highlight.js';
//导入样式
import 'highlight.js/styles/an-old-hope.css'

const app = createApp(App)

app.use(createPinia())
app.use(ElementPlus)
app.use(router)

app.directive('hljs', el => {
    let blocks = el.querySelectorAll('pre code');
    Array.prototype.forEach.call(blocks, hljs.highlightBlock);
})

app.mount('#app')
