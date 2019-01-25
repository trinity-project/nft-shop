# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random,os
from io import BytesIO
import base64

class Picture(object):
    def __init__(self, text_str, size, background):
        """
        text_str: 验证码显示的字符组成的字符串
        size:  图片大小
        background: 背景颜色
        """
        self.text_list = list(text_str)
        self.size = size
        self.background = background
    
    def create_pic(self):
        """
        创建一张图片
        """
        self.width, self.height = self.size
        self.img = Image.new("RGB", self.size, self.background)
        #实例化画笔
        self.draw = ImageDraw.Draw(self.img)
        
    def create_point(self, num, color):
        """
        num: 画点的数量
        color: 点的颜色
        功能：画点
        """
        for i in range(num):
            self.draw.point(
                (random.randint(0, self.width), random.randint(0,self.height)),
                fill = color
            )
            
    def create_line(self, num, color):
        '''
        num: 线条的数量
        color: 线条的颜色
        功能：画线条
        '''
        for i in range(num):
            self.draw.line(
                [
                    (random.randint(0, self.width), random.randint(0, self.height)),
                    (random.randint(0, self.width), random.randint(0, self.height))
                ],
                fill = color
            )
            
    def create_text(self, font_type, font_size, font_color, length):
        """
        绘制验证码字符
        font_type: 字体
        font_size: 文字大小
        font_color: 文字颜色
        font_num:  字符数量
        """
        font = ImageFont.truetype(font_type,font_size)
        c_chars = random.sample(self.text_list, length)
        strs = "  ".join(c_chars)
        font_width, font_height = font.getsize(strs)
        start_xy = ((self.width - font_width) / 3, (self.height - font_height) / 3)
        self.draw.text(start_xy, strs, font=font, fill=font_color)
        return "".join(c_chars).lower()

    def opera(self):
        """
        功能：给画出来的线条，文字，扭曲一下，缩放一下，位移一下，滤镜一下。
        就是让它看起来有点歪，有点扭。
        """
        params = [
            1 - float(random.randint(1, 2)) / 100,  
            0,
            0,
            0,
            1 - float(random.randint(1, 10)) / 100,
            float(random.randint(1, 2)) / 500,
            0.001,
            float(random.randint(1, 2)) / 500
        ]
        self.img = self.img.transform(self.size, Image.PERSPECTIVE, params)
        self.img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    @staticmethod
    def generate_verify_image(img_type="png"):
        strings = "abcdefghjkmnpqrstwxyz23456789ABCDEFGHJKLMNPQRSTWXYZ"
        size = (120,30)
        background = 'white'
        pic = Picture(strings, size, background)
        pic.create_pic()
        pic.create_point(500, (220,220,220))
        pic.create_line(30, (220,220,220))
        verify_chars = pic.create_text(os.path.join(os.getcwd(),"Arial Narrow Bold Italic.ttf"), 18, (0,0,255), 4)
        pic.opera()
        # pic.img.show()
        mstream = BytesIO()
        pic.img.save(mstream, img_type)
        return verify_chars.lower(), base64.b64encode(mstream.getvalue()).decode("utf-8")
        # return verify_chars,mstream.getvalue().encode('base64')