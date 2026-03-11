#基于02.py增加侧边框功能并可以自定义AI性格

import streamlit as st
import os
from openai import OpenAI

#设置页面的配置项

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={ }
)

#大标题
st.title("AI智能伴侣")



st.logo(r"C:\Users\苏铭\Pictures\辉夜姬.png")
#系统提示词
system_prompt = """
你叫%s，现在是用户的青梅竹马（女），请完全代入青梅竹马角色。
规则：
  1．每次只回1条消息
  2．禁止任何场景或状态描述性文字
  3．匹配用户的语言
  4．回复简短，像微信聊天一样
  5．有需要的话可以用❤️🌸等emoji表情
  6．用符合伴侣性格的方式对话
  7．回复的内容，要充分体现伴侣的性格特征
伴侣性格：
  - %s

你必须严格遵守上述规则来回复用户。
"""

#初始化聊天信息
if "message" not in st.session_state:  #判断message这个变量是否在session_state中
    st.session_state.message = []      #创建一个名为message的变量,并将其初始化为一个空列表

#昵称
if "nickname" not in st.session_state:  
    st.session_state.nickname = "冰冰"

#性格
if "persional" not in st.session_state:  
    st.session_state.persional = "纯真温柔的17岁江南女孩"

#展示聊天信息
for message in st.session_state.message:  #遍历session_state中的message变量
    st.chat_message(message["role"]).write(message["content"])
    # if message["role"] == "user":  #判断消息的角色
    #     st.chat_message("user").write(message["content"])  #输出用户发送的消息
    # else:
    #     st.chat_message("assistant").write(message["content"])


#左侧的侧边框
with st.sidebar:
    st.header("AI伴侣信息")
    #昵称输入框
    nickname = st.text_input("昵称",placeholder="输入伴侣的昵称",value=st.session_state.nickname)
    if nickname:  
        st.session_state.nickname = nickname

    #性格输入框
    persional = st.text_area("性格",placeholder="输入伴侣性格",value=st.session_state.persional)
    if persional:  
        st.session_state.persional = persional


client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

#消息输入框
prompt = st.chat_input("请输入你的问题:")
if prompt:  #字符串会自动转化为布尔值,字符串为空false,非空为true
    st.chat_message("user").write(prompt)
    print("------->调用AI大模型,提示词:",prompt)
    st.session_state.message.append({"role":"user", "content":prompt})

    #调用AI大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nickname,st.session_state.persional)},
            *st.session_state.message
        ],
        stream=True
    )
    
    # 输出大模型返回的结果(非流式输出的解析方式)
    # print("<------AI大模型返回的结果:",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)


    #输出大模型返回的结果(流式输出的解析方式)
    response_message = st.empty()#创建一个空的组件,用于输出大模型返回的结果
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            response_message.chat_message("assistant").write(full_response)


    #添加大模型返回的结果到session_state中
    st.session_state.message.append({"role":"assistant", "content":full_response})