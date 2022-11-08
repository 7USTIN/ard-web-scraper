from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

url = "https://www.ardmediathek.de/"
chromedriver_path="/Users/justin/Downloads/chromedriver"

def set_up():
    options = Options()
    options.headless = True

    global browser
    browser = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    browser.get(url)

    scroll_width = browser.execute_script("return document.body.parentNode.scrollWidth")
    scroll_height = browser.execute_script("return document.body.parentNode.scrollHeight")
    
    browser.set_window_size(scroll_width, scroll_height)
    ActionChains(browser).scroll_by_amount(0, scroll_height).perform()

    browser.implicitly_wait(3)

def take_screenshots():
    page_content = browser.find_element(By.CSS_SELECTOR, "body > div > div")
    page_content.screenshot("./screenshots/full-page.png")

    stage_content = browser.find_elements(By.CSS_SELECTOR, "div > div > a > div > img")
    next_button = browser.find_element(By.CSS_SELECTOR, ".swiper-button-next")

    for index, stage_img in enumerate(stage_content):
        stage_img.screenshot("./screenshots/{}-stage.png".format(index))
        next_button.click()

def get_video_titles():
    output = { "Stage": [] }
    rubric_titles = browser.find_elements(By.CSS_SELECTOR, "section h2")
    rubrics = browser.find_elements(By.CSS_SELECTOR, ".swiper-wrapper")

    for rubric_title in rubric_titles:
        output[rubric_title.text] = []

    for rubric_index, rubric in enumerate(rubrics):
        try:
            videos = rubric.find_elements(By.CSS_SELECTOR, ".swiper-slide")
            
            for video_index, video in enumerate(videos):
                img = video.find_element(By.CSS_SELECTOR, "img")
                img_alt = img.get_attribute("alt")

                print(rubric_index, video_index, img_alt)
        except:
            pass

    print(output, len(output), len(rubrics))

if __name__ == "__main__":
    set_up()
    #take_screenshots()
    get_video_titles()

    browser.quit()