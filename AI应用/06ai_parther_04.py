#基于03.py增加保存会话功能

import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

#设置当前时间
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#保存会话信息
def save_session_info():
    if st.session_state.current_session:
            #构建新的会话信息
            session_info = {
                "nickname":st.session_state.nickname,
                "persional":st.session_state.persional,
                "current_session":st.session_state.current_session,
                "message":st.session_state.message
            }
            #如果session文件夹不存在，则创建
            if not os.path.exists("session"):
                os.mkdir("session")
         
            #保存会话信息
            with open(f"session/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:  #创建一个json文件,保存会话信息
                    json.dump(session_info, f, ensure_ascii=False,indent=4)


#加载所有会话列表信息
def load_session_list():
    session_list = []
    #加载seesion目录下的文件
    if os.path.exists("session"):
        file_list = os.listdir("session")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)#排序倒序
    return session_list

#加载指定会回信息
def load_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            #加载会话信息
            with open(f"session/{session_name}.json", "r", encoding="utf-8") as f:  #打开json文件,读取会话信息
                session_data = json.load(f)
                st.session_state.message = session_data["message"]
                st.session_state.nickname = session_data["nickname"]
                st.session_state.persional = session_data["persional"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error(f"加载会话失败:{e}")


#删除会话信息
def delete_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            os.remove(f"session/{session_name}.json")
            if session_name == st.session_state.current_session:
                st.session_state.message = []
                st.session_state.current_session = get_current_time()
    except Exception:
        st.error("删除会话失败")



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

#当前会话标识
if "current_session" not in st.session_state:  
    st.session_state.current_session = get_current_time()


#展示聊天信息
st.text(f"会话名称:{st.session_state.current_session}")
for message in st.session_state.message:  #遍历session_state中的message变量
    st.chat_message(message["role"]).write(message["content"])
    # if message["role"] == "user":  #判断消息的角色
    #     st.chat_message("user").write(message["content"])  #输出用户发送的消息
    # else:
    #     st.chat_message("assistant").write(message["content"])


#左侧的侧边框
with st.sidebar:
    #AI控制面板
    st.header("AI控制面板")

    #新建会话
    if st.button("新建会话",width="stretch",icon="🆕"):
        #1.保存当前会话信息
        save_session_info()

        #2.创建新的会话
        if st.session_state.message:
            st.session_state.message = []
            st.session_state.current_session = get_current_time()
            save_session_info()
            st.rerun()  #重新运行当前页面

    #会话历史
    st.text("会话历史")
    session_list = load_session_list()
    for session in session_list:
        colums = st.columns([4,1])
        with colums[0]:
            #加载会话
            if st.button(session,width="stretch",icon="📄",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)         
                st.rerun()
        with colums[1]:
            #删除会话
            if st.button("",width="stretch",icon="❌",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    #分割线
    st.divider()
    
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
    #保存会话信息
    save_session_info()