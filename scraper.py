import os, sys, csv, json
from time import sleep
from urllib.request import urlopen, urlretrieve
from itertools import zip_longest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

ard_url = "https://www.ardmediathek.de/"
ard_api = "https://api.ardmediathek.de/page-gateway/pages/ard/editorial/mainstreamer-webpwa-nichtaendern"
teaser_image_size = "1000" # size in px

output_dir = sys.argv[1]
images_dir = f"{output_dir}/images"
chromedriver_exec = "./chromedriver"
csv_file_name = "ard-mediathek.csv"

def check_output_dir():
    print(f"\nChecking if '{images_dir}' exists...")

    try:
        os.makedirs(f"{images_dir}")
        print(f"Created '{images_dir}'")
    except FileExistsError:
        print(f"'{images_dir}' already exists")

def delete_prev_images():
    print("\nEmptying image directory...")

    for file in os.scandir(images_dir):
        os.remove(file.path)

def take_screenshot():
    print("\nSetting up the browser...")

    options = Options()
    options.headless = True

    serivce = Service(chromedriver_exec)

    browser = webdriver.Chrome(options=options, service=serivce)
    browser.get(ard_url)
    print(f"Opened '{ard_url}'")

    scroll_width = browser.execute_script("return document.body.parentNode.scrollWidth")
    scroll_height = browser.execute_script("return document.body.parentNode.scrollHeight")
    browser.set_window_size(scroll_width, scroll_height)
    print("Adjusted window size")

    print("\nWaiting 10 seconds for the page to load...")
    
    sleep(10)

    print("\nTaking screenshot...")
    
    page_content = browser.find_element(By.CSS_SELECTOR, "body > div > div")
    page_content.screenshot(f"{images_dir}/page.png")
    print("Saved as 'page.png'")

    browser.quit()

def fetch_ard_api():
    print("\nFetching ARD api...")

    with urlopen(ard_api) as url:
        global api_res
        api_res = json.loads(url.read())

def download_stage_teasers():
    print("\nDownloading stage teasers...")

    teasers = api_res["widgets"][0]["teasers"]

    for teaser in teasers:
        teaser_src = teaser["images"]["aspect16x9"]["src"]
        img_url = teaser_src.replace("{width}", teaser_image_size)

        teaser_title = teaser["longTitle"].lower().strip().replace(" ", "_")
        file_name = f"{teaser_title}.png"

        urlretrieve(img_url, f"{images_dir}/{file_name}")
        print(f"Saved as '{file_name}'")

def get_titles():
    print("\nFetching rubric and video titles...")

    global rubric_titles
    rubric_titles = []
    rubric_filter = ["Menü", "Rubriken", "Unsere Region"]

    global video_titles
    video_titles = []

    for rubric in api_res["widgets"]:
        rubric_title = rubric["links"]["self"]["title"]
        rubric_video_titles = []

        if rubric_title in rubric_filter:
            continue

        rubric_titles.append(rubric_title)

        for video in rubric["teasers"]:
            rubric_video_titles.append(video["longTitle"])
        
        video_titles.append(rubric_video_titles)

def write_csv_file():
    print("\nWriting data to CSV file...")

    video_title_columns = zip_longest(*video_titles, fillvalue="")

    with open(f"{output_dir}/{csv_file_name}", "w+", newline="") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(rubric_titles)
        writer.writerows(video_title_columns)

    print(f"Saved as '{csv_file_name}'")

if __name__ == "__main__":
    check_output_dir()
    delete_prev_images()
    take_screenshot()
    fetch_ard_api()
    download_stage_teasers()
    get_titles()
    write_csv_file()