# 实验一检查材料

## 操作指令

调用cli
```sh
./build/bin/Debug/main -m chatglm-ggml.bin -i
```

环境变量
```sh
set MODEL=../chatglm-ggml.bin
```

拉起API Server
```sh
uvicorn openai_api:app --host 127.0.0.1 --port 6006
```

## 演示例子

**担任编剧**
> 我要你担任编剧。您将为长篇电影或能够吸引观众的网络连续剧开发引人入胜且富有创意的剧本。从想出有趣的角色、故事的背景、角色之间的对话等开始。一旦你的角色发展完成——创造一个充满曲折的激动人心的故事情节，让观众一直悬念到最后。我的第一个要求是“我需要写一部以巴黎为背景的浪漫剧情电影”。  

> I want you to serve as a screenwriter. You'll develop engaging and creative scripts for feature-length movies or web series that will captivate an audience. Start by coming up with interesting characters, the setting of the story, dialog between characters, etc. Once your character development is complete - create an exciting storyline full of twists and turns that will keep the audience in suspense until the end. My first request was "I need to write a romantic drama movie set in Paris".

**充当诗人**
> 我要你扮演诗人。你将创作出能唤起情感并具有触动人心的力量的诗歌。写任何主题或主题，但要确保您的文字以优美而有意义的方式传达您试图表达的感觉。您还可以想出一些短小的诗句，这些诗句仍然足够强大，可以在读者的脑海中留下印记。我的第一个请求是“我需要一首关于爱情的诗”。  

> I want you to play the poet. You will create poems that evoke emotion and have the power to touch the heart. Write about any subject or theme, but make sure your words convey the feeling you are trying to express in a beautiful and meaningful way. You can also come up with short verses that are still powerful enough to leave a mark on the reader's mind. My first request was "I need a poem about love".

**充当Rapper**
> 我想让你扮演中文说唱歌手。您将想出强大而有意义的歌词、节拍和节奏，让听众“惊叹”。你的歌词应该有一个有趣的含义和信息，人们也可以联系起来。在选择节拍时，请确保它既朗朗上口又与你的文字相关，这样当它们组合在一起时，每次都会发出爆炸声！我的第一个请求是“我需要一首关于在你自己身上寻找力量的说唱歌曲。”  

> I want you to play the role of a rapper. You will come up with powerful and meaningful lyrics, beats and rhythms that will "wow" the audience. Your lyrics should have an interesting meaning and message that people can relate to. When choosing a beat, make sure it's both catchy and relevant to your words so that when they come together, they go off with a bang every time! My first request is "I need a rap song about finding strength in yourself."

## 常识知识挖掘Prompt

> 提取给定文本中的生活常识知识三元组，每个三元组的格式应为（头实体；关系；尾实体）。文本类型不限制。确保提取的三元组精简明了，涵盖广泛的常识知识。关系部分应包含逻辑关系，如“多吃洋葱有益高血压”应提取为（吃洋葱；有益；高血压）。提取的三元组数量应尽可能多，且提取的文本长度应尽量精简概括。在提取知识三元组时可以考虑上下文信息，并且不需要在输出中包含额外的解释性文本或示例。文本来源无明显偏好。在处理复杂句子或模糊关系时，请提供一个最有可能的三元组。第一段文本是“世界上最大的猴是狒狒，最小的猴子是倭狨。”  

> Extract triads of general life knowledge from a given text, each of which should be in the format (head entity; relationship; tail entity). There is no restriction on the text type. Ensure that the extracted triples are concise and cover a wide range of general knowledge. Relationships should contain logical relationships, e.g. "Eating more onions is good for high blood pressure" should be extracted as (eating onions; good; high blood pressure). The number of triads extracted should be as large as possible, and the length of the extracted text should be as concise and general as possible. Contextual information can be taken into account when extracting knowledge triples and there is no need to include additional explanatory text or examples in the output. There is no clear preference for text sources. When dealing with complex sentences or fuzzy relationships, please provide one of the most likely triples. The first text is "The largest monkey in the world is the baboon and the smallest is the bonneted marmoset."