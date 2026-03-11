import json

#写入json文件
user = {
    "name": "帅哥",
    "age": 18,
    "gender": "男",
    "hobby": ["football", "swimming"]
}

with open(r"D:\python进阶\AI应用\resources\user.json", 'w', encoding='utf-8') as f:
    #ensure_ascii默认为True,中文会变成unicode编码;False:中文会原样输出
    #indent缩进(格式化)
    json.dump(user, f,ensure_ascii=False,indent=4)#json.dump()方法将字典写入文件


#读取json文件
with open(r"D:\python进阶\AI应用\resources\user.json", 'r', encoding='utf-8') as f:
    user = json.load(f)#json.load()方法将json文件读取为字典
    print(user) #字典类型