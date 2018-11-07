from django.shortcuts import render,HttpResponse

# Create your views here.

def login(request):
    return render(request,'login.html')

# 返回图片验证码
import random
def get_validCode_img(request):

    def get_random_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

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

    for i in range(5):
        random_num=chr(random.randint(0,9))
        random_low_alpha =  chr(random.randint(95, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char =random.choice([random_num,random_low_alpha,random_upper_alpha])

        # draw.text((0,5),'python',get_random_color(),font=kumo_font)
        draw.text((i*50,5),random_char,get_random_color(),font=kumo_font)

    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()

    return HttpResponse(data)

