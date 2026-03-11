# #读文件
# #1.打开文件
# f = open(r"C:\Users\苏铭\Desktop\文件操作入门.txt", 'r', encoding='utf-8')

# #2.读取文件
# # content = f.read()  #读取所有内容
# # print(content)

# content = f.readline()#读取一行
# for line in content:
#     print(line.strip())

# #3.关闭文件
# f.close()


# #写文件
# #1.打开文件
# f = open(r"C:\Users\苏铭\Desktop\文件操作入门.txt", 'w', encoding='utf-8')

# #2.写入文件
# f.write("静夜思(李白)\n\n")
# f.write("床前明月光,\n")
# f.write("疑是地上霜,\n")
# f.write("举头望明月,\n")
# f.write("低头思故乡.\n")
   

#3.关闭文件



# # f.close()
# #==========================释放资源=========================================
# #写文件
# #1.打开文件
# f = open(r"C:\Users\苏铭\Desktop\文件操作入门.txt", 'w', encoding='utf-8')

# try:
#     #2.写入文件
#     f.write("静夜思(李白)\n\n")
#     f.write("床前明月光,\n")
#     f.write("疑是地上霜,\n")
#     f.write("举头望明月,\n")
#     f.write("低头思故乡.\n")
   
# finally:
#     #3.关闭文件
#     f.close()

#==========================with语句=========================================
#写文件
#1.打开文件
with open(r"C:\Users\苏铭\Desktop\文件操作入门.txt", 'w', encoding='utf-8') as f:
    #2.写入文件
    f.write("静夜思(李白)\n\n")
    f.write("床前明月光,\n")
    f.write("疑是地上霜,\n")
    f.write("举头望明月,\n")
    f.write("低头思故乡.\n")
    

