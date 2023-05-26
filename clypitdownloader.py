from selenium import webdriver
import time
import wget
import re
 
browser = webdriver.Chrome()
browser.get("https://clyp.it/user/ej4pgwed")
time.sleep(3) # 3초 대기

SCROLL_PAUSE_SEC = 1

# 스크롤 높이 가져옴
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # 끝까지 스크롤 다운
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #Load More 찾기
    try:
        some_tag = browser.find_element_by_xpath('//*[@id="profilePageWrapper"]/div/div/div/div/div/a')
    except:
        break
    
    # Load More클릭
    some_tag.click() 
    
    time.sleep(SCROLL_PAUSE_SEC)
    # 스크롤 다운 후 스크롤 높이 다시 가져옴
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

tracklink = 1

#새탭에서 열기
while True:
    print('//*[@id="profilePageWrapper"]/div/div/div/div/div/div/div['+str(tracklink)+']/div[1]/a')

    try:
        track_xpath = browser.find_element_by_xpath('//*[@id="profilePageWrapper"]/div/div/div/div/div/div/div['+str(tracklink)+']/div[1]/a')
    
    except:
        break
    #trackhref = 개별 트랙 링크
    trackhref = track_xpath.get_attribute('href')
    print(track_xpath.get_attribute('href'))
    #새탭에서 개별 트랙 열기
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[1])
    browser.get(trackhref)
    #로딩 대기
    time.sleep(1)
    #아티스트 이름 얻기
    artist_xpath = browser.find_element_by_xpath('//*[@id="player-page"]/div[1]/section[4]/div[1]/div/div/ul/li/div/div[1]/a/span')
    artist_name = artist_xpath.text
     #트랙 이름 얻기
    track_xpath = browser.find_element_by_xpath('/html/head/meta[5]')
    track_name = track_xpath.get_attribute('content')
    track_name = track_name[:len(track_name)-7]
    #트랙 다운로드 링크 얻기
    music_xpath = browser.find_element_by_xpath('//*[@id="nativeAudioPlayer"]')
    music_link = music_xpath.get_attribute('src')
    #파일명을 위한 트랙명 처리
    raw_filename = wget.detect_filename(music_link)
    #파일명 지정하여 다운로드
    path = re.sub(r'[<>:"/\\|?*]', '', (artist_name +' - '+ track_name +' - '+ raw_filename))
    wget.download(music_link, out=path)
    #탭 종료
    browser.close()
    #다음 트랙 지정
    tracklink=tracklink+2
    browser.switch_to.window(browser.window_handles[0])

browser.quit() # 브라우저 종료