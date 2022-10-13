from glob import glob
from captcha.image import ImageCaptcha
import random
import string

def generate_captcha(lenght):
    # letters_and_digits = string.ascii_lowercase + string.digits
    digits = string.digits
    
    rand_string = ''.join(random.sample(digits, lenght))

    pattern=rand_string

    image_captcha = ImageCaptcha(width=300, height=200)

    image_captcha.write(pattern, "./storage/captcha.png")

    return rand_string