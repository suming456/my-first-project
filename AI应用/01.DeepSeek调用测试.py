# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

#创建与AI大模型交互的客户端对象 (DEEPSEEK_API_KEY 环境变量的名字，值就是DeepSeek的API——KEY)
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")


#与AI大模型进行交互
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个温柔青春的AI助理x,会用温柔阳光的语气回答问题"},
        {"role": "user", "content": "你是谁?"},
    ],
    stream=False    #设置为False，表示返回一个完整的结果
)

#输出大模型返回的结果
print(response.choices[0].message.content)