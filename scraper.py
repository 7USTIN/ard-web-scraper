from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

url = "https://www.ardmediathek.de/"

def set_up():
    options = Options()
    options.headless = True

    global browser
    
    browser = webdriver.Chrome(
        options=options,
        executable_path="/Users/justin/Downloads/chromedriver"
    )

    browser.get(url)
    browser.set_page_load_timeout(5)

    scroll_width = browser.execute_script('return document.body.parentNode.scrollWidth')
    scroll_height = browser.execute_script('return document.body.parentNode.scrollHeight')
    
    browser.set_window_size(scroll_width, scroll_height)
    ActionChains(browser).scroll_by_amount(0, scroll_height).perform()

def take_screenshots():
    websiteContent = browser.find_element(By.CSS_SELECTOR, "body > div > div")
    websiteContent.screenshot("./screenshots/full-page.png")

    stageContent = browser.find_elements(By.CSS_SELECTOR, "div > div > a > div > img")
    
    for index, img in enumerate(stageContent):
        img.screenshot("./screenshots/{}-stage.png".format(index))

def get_video_titles():
    rubrics = browser.find_elements(By.CSS_SELECTOR, "section > span > h2")
    titles = browser.find_elements(By.CLASS_NAME, "swiper-wrapper")

    for rubric in rubrics:
        print(rubric.text)

    #for title in titles:
    #    print(title.text)

if __name__ == "__main__":
    set_up()
    take_screenshots()
    get_video_titles()

    browser.quit()