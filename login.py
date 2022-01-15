# References - http://zhuanlan.zhihu.com/p/94402506
#              https://www.youtube.com/watch?v=4DrCIVS5U3Y
# Image correction - https://nanonets.com/blog/ocr-with-tesseract/

from selenium import webdriver
import time
from PIL import Image
import pytesseract as tess
# set PATH for tesseract
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# capture captcha and save as png picture
def get_captcha():
    browser.get(loginurl)
    # search for element by id 'imgcode'
    imgtag = browser.find_element_by_id('imgcode')

    # prove get auth code img
    #imgsrc = imgtag.get_attribute('src')
    #print(imgsrc)

    # save the auth code picture screenshot
    imgtag.screenshot('captcha.png')

###
# image processing
# by adjusting the threshold to remove noises on the image
###
def transform_captcha():
    image = Image.open('captcha.png')
    # thresholding
    image = image.convert('L') # transform from P mode to L mode
    count = 160 # set the threshold
    table = []
    for i in range(256):
        if (i < count):
            table.append(0)
        else:
            table.append(1)    
    image = image.point(table, '1')
    image.save('captcha.png')

# recognize captcha
def recognize_captcha():
    image = Image.open('captcha.png')
    captcha = tess.image_to_string(image)
    if (len(captcha) == 6):
        captcha = captcha[0:4]
    return captcha

# login to the webpage
def login(captcha):
    browser.find_element_by_id('loginName').send_keys('13521322704')  # username
    browser.find_element_by_id('loginPwd').send_keys('three17710$')  # password
    browser.find_element_by_id('Verfcode').send_keys(captcha)  # input captcha
    time.sleep(5)
    browser.find_element_by_class_name('btn_login').click()  # click login button
    time.sleep(10)
    if (browser.title == '业绩查询'):
        return True
    else:
        return False

if __name__ == '__main__':
    # instantiate object
    browser = webdriver.Chrome("C:\MyDrivers\webdrivers\chromedriver.exe")
    loginurl = 'http://union.ly.com/web/index'

    # try automatic login for 5 times
    isSuccess = False
    numTries = 6
    while(isSuccess!=True and numTries > 0):
        get_captcha()
        transform_captcha()
        captcha = recognize_captcha()
        print(captcha)
        if (len(captcha) == 4):
            isSuccess = login(captcha)
        numTries -= 1
    if(isSuccess):
        print('Successful login to the website!')
