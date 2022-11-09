import os, csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

url = "https://www.ardmediathek.de/"
chromedriver_path="/Users/justin/Downloads/chromedriver"
screenshots_path="./screenshots"
csv_file_path="./ard.csv"

def set_up():
    print("\nSetting up the browser...")

    options = Options()
    options.headless = True

    serivce = Service(chromedriver_path)

    global browser
    browser = webdriver.Chrome(options=options, service=serivce)
    browser.get(url)
    print("Opened '{}'".format(url))

    scroll_width = browser.execute_script("return document.body.parentNode.scrollWidth")
    scroll_height = browser.execute_script("return document.body.parentNode.scrollHeight")
    browser.set_window_size(scroll_width, scroll_height)
    print("Adjusted window size")

def take_screenshots():
    print("\nDeleting previous screenshots...")

    for file in os.scandir(screenshots_path):
        os.remove(file.path)

    print("\nTaking screenshots...")

    sleep(5)
    
    page_content = browser.find_element(By.CSS_SELECTOR, "body > div > div")
    page_content.screenshot("{}/full-page.png".format(screenshots_path))
    print("Saved screenshot 'full-page.png'")

    stage_content = browser.find_elements(By.CSS_SELECTOR, "div > div > a > div > img")
    next_button = browser.find_element(By.CSS_SELECTOR, ".swiper-button-next")

    for index, stage_img in enumerate(stage_content):
        stage_img.screenshot("{}/{}-stage.png".format(screenshots_path, index + 1))
        print("Saved screenshot '{}-stage.png'".format(index + 1))

        next_button.click()
        sleep(1)

def get_video_titles():
    print("\nFetching video titles...")

    global rubric_titles
    rubric_titles = []

    global video_titles
    video_titles = []

    rubric_title_elements = browser.find_elements(By.CSS_SELECTOR, "section h2")
    rubric_elements = browser.find_elements(By.CSS_SELECTOR, ".swiper-wrapper")

    for rubric_title in rubric_title_elements:
        rubric_titles.append(rubric_title.text)

    for rubric in rubric_elements:
        results = []

        try:
            videos = rubric.find_elements(By.CSS_SELECTOR, ".swiper-slide")

            for video in videos:
                video_title = video.find_element(By.CSS_SELECTOR, "img").get_attribute("alt")

                results.append(video_title)
        except:
            pass
        
        video_titles.append(results)

def write_to_csv_file():
    print("\nWriting to CSV file...")

    with open(csv_file_path, "w+", newline="") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(rubric_titles)
        writer.writerows(video_titles)

    print(rubric_titles, "\n", video_titles)

if __name__ == "__main__":
    set_up()
    take_screenshots()
    get_video_titles()
    write_to_csv_file()

    browser.quit()