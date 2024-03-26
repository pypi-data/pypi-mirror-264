import os
import random

def get_discourse():
    """获取文件内容。"""
    # 获取文件总行数
    if os.path.isfile("discourse.txt") == False:
        with open('discourse.txt', 'w', encoding='utf8') as f:
            f.write("这是一条测试一言，请前往运行目录下的discourse.txt文件修改。")
    with open('discourse.txt', 'r', encoding='utf8') as f: 
        lines = f.readlines()
        discourse_id = random.randint(0, len(lines) - 1)
    return lines[discourse_id]