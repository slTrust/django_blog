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
    from PIL import Image
    img = Image.new("RGB",(270,40),color=get_random_color())
    with open('validCode.png','wb') as f:
        img.save(f,'png')

    with open('validCode.png','rb') as f:
        data = f.read()

    return HttpResponse(data)

