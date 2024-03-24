import web
import random
import linecache
import os

urls = (
    '/', 'index'
)

def start():
    """启动应用程序。"""
    app = web.application(urls, globals())
    app.run()

# 获取一言内容
def get_hitokoto(filename, hitokoto_id):
    line = linecache.getline(filename, hitokoto_id)
    return line.strip()

class index:
    def GET(self):
        # 获取文件总行数
        if os.path.isfile("hitokoto.txt") == False:
            with open('hitokoto.txt', 'w') as f:
                f.write("这是一条测试一言，请前往Python安装目录下的Lib\site-packages\\todayhitokoto\hitokoto.txt修改")
        with open("hitokoto.txt", 'r') as f:
            total_lines = sum(1 for line in f)
        # 生成一个随机的行号
        hitokoto_id = random.randint(1, total_lines)
        return get_hitokoto("hitokoto.txt", hitokoto_id)  