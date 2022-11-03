import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

url = "https://www.ardmediathek.de/"
screenshot_path = os.path.dirname(sys.argv[0])

def set_up():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    global browser
    browser = webdriver.Chrome(options=options)
    browser.get(url)

def take_screenshot():
    websiteContent = browser.find_element_by_tag_name('body')
    websiteContent.screenshot(screenshot_path)

def get_video_titles():
    rubrics = browser.find_elements(By.TAG_NAME, "h2").text
    titles = browser.find_elements(By.CLASSNAME, "swiper-wrapper")

    for title in titles:
        print(title)
    
    print(rubrics)

if __name__ == "__main__":
    set_up()
    take_screenshot()
    #get_video_titles()

    browser.quit()