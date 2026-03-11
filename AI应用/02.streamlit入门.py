import streamlit as st


#设置页面的配置项

st.set_page_config(
    page_title="streamlit入门",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.douyin.com',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# daddy!"
    }
)

#大标题
st.title("Streamlit 入门演示")
st.header("Streamlit 一级标题")
st.subheader("Streamlit 二级标题")

#段落文字
st.write("超级无敌吊炸天")
st.write("你美爆炸了")

#图片
st.image(r"C:\Users\苏铭\Pictures\辉夜姬.png",width=300)

#音频
st.audio(r"C:\Users\苏铭\Music\你美爆炸了.m4a")

#视频
st.video(r"C:\Users\苏铭\Videos\share_c78d27d823c99350ed54d0a089b228cc1769931611899.mp4")

#logo
st.logo(r"C:\Users\苏铭\Pictures\辉夜姬.png")

#表格
student_data = {
"姓名": ["王林", "李慕婉", "贝罗", "莫厉海", "石萧"],
"学号": ["20260001", "20260002", "20260003", "20260004", "20260005"],
"语文": [98, 90, 59, 29, 80],
"数学": [88, 78, 65, 70, 39],
"英语": [99, 89, 87, 59, 62],
"总分": [285, 257, 211, 158, 181]
}
st.table(student_data)

#输入框
name = st.text_input("请输入姓名:")
st.write(f"您输入的姓名为:{name}")

#密码输入框
password = st.text_input("请输入密码:",type="password")
st.write(f"您输入的密码为:{password}")

#单选按钮
gender = st.radio("请输入您的性别:",["男","女","未知"],index=2)
st.write(f"您的性别为:{gender}")