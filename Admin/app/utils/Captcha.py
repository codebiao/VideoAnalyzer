import random
import io
from PIL import Image, ImageDraw, ImageFont

class Captcha():
    def __init__(self,font_path):

        self.font = ImageFont.truetype(font_path, size=30)
        self.captcha_width = 100
        self.captcha_height = 38
        self.captcha_code_num = 4
        self.captcha_code_width = 25

    def randomColor(self):

        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def getVerifyCode(self):
        try:
            img = Image.new('RGB', (self.captcha_width,self.captcha_height), color=(255,255,255))
            draw = ImageDraw.Draw(img)

            verify_code = ''
            for i in range(self.captcha_code_num):
                random_num = str(random.randint(0, 9))
                random_low_alpha = chr(random.randint(97, 122))
                random_high_alpha = chr(random.randint(65, 90))
                random_char = random.choice([random_num, random_low_alpha, random_high_alpha])

                x = i * self.captcha_code_width+random.randint(2,10)
                y = random.randint(0,10)
                draw.text((x,y),
                          random_char,
                          self.randomColor(),
                          font=self.font)
                # 保存验证码字符串
                verify_code += random_char

            # 噪点噪线
            for i in range(self.captcha_code_num):
                x1 = random.randint(0, self.captcha_width)
                x2 = random.randint(0, self.captcha_width)
                y1 = random.randint(0, self.captcha_height)
                y2 = random.randint(0, self.captcha_height)
                draw.line((x1, y1, x2, y2), fill=self.randomColor())

            for i in range(self.captcha_code_num):
                draw.point([random.randint(0, self.captcha_width), random.randint(0, self.captcha_height)],
                           fill=self.randomColor())
                x = random.randint(0, self.captcha_width)
                y = random.randint(0, self.captcha_height)
                draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.randomColor())

            # img.save("test.png", quality=95)

            f = io.BytesIO()  # 用完之后，BytesIO会自动清掉
            img.save(f, 'png')
            verify_img_byte = f.getvalue()

            return True,verify_code,verify_img_byte

        except Exception as e:
            return False,None,None

if __name__ == '__main__':
    captcha = Captcha(resource_path="../app/resource")
    state, verify_code, verify_img_byte = captcha.getVerifyCode()
    print(state,verify_code)