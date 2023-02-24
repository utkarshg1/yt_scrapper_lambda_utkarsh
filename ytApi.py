from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json


# This is main function to execute
def main(event, context):
    
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-extensions')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('/opt/chromedriver',chrome_options=options)
    
    data = json.loads(event['body'])['url']
    
    driver.get(data)
    time.sleep(2)
    title = driver.title
    
    driver.execute_script("window.scrollTo(0, 200)")
    
    # First Get Titles and URL    
    url_elems = driver.find_elements(By.XPATH,"//a[@id='video-title-link']")
    url_elems5 = url_elems[0:5] 
    top5titles = []
    top5urls = []
    for i in url_elems5:
        top5titles.append(i.get_attribute('title'))
        top5urls.append(i.get_attribute('href'))
    
    print('Top5 Urls :',top5urls)    
    print('Top5 Titles :',top5titles)
    
    # Get Thumbnail URL's
    images = driver.find_elements(By.TAG_NAME,'img')
    img_links = []    
    for i in images:    
        link = i.get_attribute('src')
        if str(link).find('i.ytimg.com')>0:
            img_links.append(link)
    top5thumbnails = img_links[0:5]
    print('Top5thumbnails',top5thumbnails)

    # Get Views and Relative time
    views_elements = driver.find_elements(By.XPATH,"//span[@class='inline-metadata-item style-scope ytd-video-meta-block']")
    view_count = []
    rel_time = []
    for i in views_elements:  
        meta_string = i.text      
        if meta_string.find('views')>0:      
            view_count.append(meta_string)
        elif meta_string.find('ago')>0:
            rel_time.append(meta_string)
    
    top5views = view_count[0:5]
    top5_reltime = rel_time[0:5]
    print('Top5Views',top5views)
    print('top5reltime',top5_reltime)

    # Creating a final response to compile all data and provide as json
    
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            'url_provided':data,
            'channel_title':title,
            'output':{
                'title':top5titles,
                'reltime':top5_reltime,
                'views':top5views,
                'videoURL':top5urls,
                'thumbnailURL':top5thumbnails
            }
            
        })
    }
    
    return response
    
