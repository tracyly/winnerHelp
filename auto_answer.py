import os

import sys

import subprocess

import pytesseract

from PIL import Image

from selenium import webdriver

from time import sleep

import time

screenshot_way = 2

brower = webdriver.Chrome()


def pull_screenshot():
    # 截图
    start = time.clock()
    global screenshot_way
    if screenshot_way == 2 or screenshot_way == 1:
        process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
        screenshot = process.stdout.read()
        if screenshot_way == 2:
            binary_screenshot = screenshot.replace(b'\r\n', b'\n')
        else:
            binary_screenshot = screenshot.replace(b'\r\r\n', b'\n')
        f = open("screenshot.png", 'wb')
        f.write(binary_screenshot)
        f.close()
    elif screenshot_way == 0:
        os.system('adb shell screencap -p /sdcard/screenshot.png')
        os.system('adb pull /sdcard/screenshot.png .')
    end = time.clock()
    print(' screenshot Running time: %s Seconds' % (end - start))


def check_screenshot():
    # 检查截图方法
    global screenshot_way
    if os.path.isfile("screenshot.png"):
        os.remove("screenshot.png")
    if (screenshot_way < 0):
        print("暂不支持该设备")
        sys.exit(0)
    pull_screenshot()
    try:
        Image.open("screenshot.png").load()
        print("采用方式{}截图".format(screenshot_way))
    except Exception:
        screenshot_way -= 1
        check_screenshot()


def is_start(prompt, true_value='y', false_value='f', default=True):
    prompt = '%s %s/%s: ' % (prompt, true_value, false_value)
    i = input(prompt)
    if not i:
        return default
    while True:
        if i == true_value:
            return True
        elif i == false_value:
            return False
        prompt = "请输入 %s 或者 %s:" % (true_value, false_value)
        i = input(prompt)


# 芝士超人去除index=text.index("."),text=text[index+1:]
def image_to_text():
    start = time.clock()
    im = Image.open("screenshot.png")
    print(im.size)
    box = (0, im.size[1] / 8, im.size[0], im.size[1] / 3)
    image = im.crop(box)
    # image.show()
    # image.save('d:/dave.jpg')
    text = pytesseract.image_to_string(image, lang="chi_sim")
    index = text.index(".")
    # lastIndex = text.index("?")
    text = text[index + 1:]
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    # text = ''.join(text.split(' '))
    print(text)
    end = time.clock()
    print(' image to text Running time: %s Seconds' % (end - start))
    return text


def search_by_browser(text):
    brower.get("http:www.baidu.com")
    brower.find_element_by_id("kw").send_keys(text)
    brower.find_element_by_id("su").click()
    sleep(20)


def main():
    # 函数入口y
    start = time.clock()
    op = is_start("是否开始分析答题?")
    if not op:
        print("那就算了吧")
        return
    pull_screenshot()
    text = image_to_text()
    search_by_browser(text)
    end = time.clock()
    print("time spent %s seconds" % (end - start))


if __name__ == '__main__':
    main()
