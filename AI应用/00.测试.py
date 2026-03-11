import os
from openai import OpenAI
import streamlit as st
from datetime import datetime
import json

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def save_seesion_info():
    if st.session_state.current_session:
        session_info = {
            'nickname':st.session_state.nickname,
            "persional":st.session_state.persional,
            "current_session":st.session_state.current_session,
            "message":st.session_state.message    
        }
        if not os.path.exists("session"):
            os.mkdir("session")
        with open(f"session/{st.session_state.current_session}.json","w",encoding="utf-8")as f:
                  json.dump(session_info,f,ensure_ascii=False,indent=4)

def load_session_list():
    session_list = []
    if os.path.exists("session"):
        file_list = os.listdir("session")
        for file in file_list:
            if file.endswith(".json"):
                session_list.append(file[:-5])
    session_list.sort(reverse=True)
    return session_list

def load_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            with open(f"session/{session_name}.json","r",encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.message = session_data["message"]
                st.session_state.nickname = session_data["nickname"]
                st.session_state.persional = session_data["persional"]
                st.session_state.current_session = session_name 
    except Exception as e:
        st.error(f"出现错误:{e}")

def delete_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            os.remove(f"session/{session_name}.json")
            if session_name == st.session_state.current_session:
                st.session_state.message = []
                st.session_state.current_session = get_current_datetime()
    except Exception:
        print("删除失败")

st.set_page_config(
    page_title="AI大模型交互",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={ }
)

st.title("AI伴侣")

if "message" not in st.session_state:
    st.session_state.message = []

for message in st.session_state.message:
    st.chat_message(message["role"]).write(message["content"])


p1 = """
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
if 'nickname' not in st.session_state:
    st.session_state.nickname = '冰冰'

if 'persional' not in st.session_state:
    st.session_state.persional = "纯真温柔的17岁江南女孩" 

if 'current_session' not  in st.session_state:
    st.session_state.current_session = get_current_datetime()

with st.sidebar:
    st.title("AI控制面板")

    if st.button("新建会话",width="stretch"):
        save_seesion_info()
        if st.session_state.message:
            st.session_state.message=[]
            st.session_state.current=get_current_datetime()
            save_seesion_info()
            st.rerun()
        
    st.text("历史会话")
    session_list = load_session_list()
    for session in session_list:
        columns = st.columns([4,1])
        with columns[0]:
            if st.button(session,width="stretch",key=f"load_{session}",type="primary"if session==st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with columns[1]:
            if st.button("",width="stretch",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    st.title("AI伴侣信息")
    nickname = st.text_input("昵称:",value="冰冰",placeholder="请输入伴侣昵称:")
    if nickname:
        st.session_state.nickname = nickname
    
    persional = st.text_input("性格",value="纯真温柔的17岁江南女孩",placeholder="请输入伴侣性格:")
    if persional:
        st.session_state.persional = persional

#创建与AI大模型交互的客户端对象 (DEEPSEEK_API_KEY 环境变量的名字，值就是DeepSeek的API——KEY)
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")


a1 = st.chat_input("请输入你的问题:")
if a1:
    st.chat_message('user').write(a1)
    print("调用AI提示词",a1)
    st.session_state.message.append({"role":"user","content":a1})

    #与AI大模型进行交互
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": p1 % (st.session_state.nickname,st.session_state.persional)},
            *st.session_state.message
        ],
        stream=True
    )

    # #输出大模型返回的结果
    # print(response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # st.session_state.message.append({"role":"assistant","content":response.choices[0].message.content})

    b1 = st.empty()
    full_message = ""
    for a in response:
        if a.choices[0].delta.content is not None:
            full_message+=a.choices[0].delta.content
            b1.chat_message("assistant").write(full_message)
    
    st.session_state.message.append({"role":"assistant","content":full_message})
