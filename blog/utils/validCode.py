#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import random
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_valid_code_img(request):


    # 方式一
    # with open('lufei.jpg',"rb") as f:
    #     data = f.read()

    # 方式二 pip install pillow
    # from PIL import Image
    # img = Image.new("RGB",(270,40),color=get_random_color())
    # with open('validCode.png','wb') as f:
    #     img.save(f,'png')
    #
    # with open('validCode.png','rb') as f:
    #     data = f.read()

    # 方式三 避免文件读取操作  用内存更快
    # from PIL import Image
    # from io import BytesIO
    # img = Image.new("RGB", (270, 40), color=get_random_color())
    #
    # f = BytesIO()
    # img.save(f,'png')
    # data = f.getvalue()

    # 方式四  图片验证码的文字
    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO
    img = Image.new("RGB", (270, 40), color=get_random_color())

    draw = ImageDraw.Draw(img)
    # draw.text()  # 画字
    # draw.line()  # 画线
    # draw.point() # 画点

    # 指定字体
    kumo_font = ImageFont.truetype("static/font/kumo.ttf",size=32)

    # 随机内容
    valid_code_str = ''
    for i in range(5):
        random_num=chr(random.randint(0,9))
        random_low_alpha =  chr(random.randint(95, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char =random.choice([random_num,random_low_alpha,random_upper_alpha])

        # draw.text((0,5),'python',get_random_color(),font=kumo_font)
        draw.text((i*50,5),random_char,get_random_color(),font=kumo_font)
        valid_code_str += random_char
    # 躁线
    # width=270
    # height=40
    # for i in range(10):
    #     x1=random.randint(0,width)
    #     x2=random.randint(0,width)
    #     y1=random.randint(0,height)
    #     y2=random.randint(0,height)
    #     draw.line((x1,y1,x2,y2),fill=get_random_color())
    #
    # for i in range(100):
    #     draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    print(valid_code_str) # 打印随机字符
    request.session['valid_code_str'] = valid_code_str
    '''
    1。生成随机字符串 xxxx
    2。设置个cookie {"sessionid":xxxx}
    3。django-session里存储
        session-key session-data
        xxxx    {"valid_code_str":"12345"}
    '''

    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    return data