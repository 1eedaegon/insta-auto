import os


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from opt.settings import config

# Init config
ID = config["ROFL"]["ID"]
PW = config["ROFL"]["PW"]
SITE = config["CRAWL"]["SITE"]
WIDTH = config["CRAWL"]["WIDTH"]
HEIGHT = config["CRAWL"]["HEIGHT"]
ID_XPATH = config["CRAWL"]["ID_XPATH"]
PW_XPATH = config["CRAWL"]["PW_XPATH"]
FORM_CLS_PATH = config["CRAWL"]["FORM_CLS_PATH"]
NOTI_INFO_XPATH = config["CRAWL"]["NOTI_INFO_XPATH"]
LOGIN_INFO_XPATH = config["CRAWL"]["LOGIN_INFO_XPATH"]
POST_TAG_PATH = config["CRAWL"]["POST_TAG_PATH"]
LINK_TAG_PATH = config["CRAWL"]["LINK_TAG_PATH"]
TOTAL_POSTS_XPATH = config["CRAWL"]["TOTAL_POSTS_XPATH"]
POST_DESC_XPATH = config["CRAWL"]["POST_DESC_XPATH"]
LIKE_LIST_XPATH = config["CRAWL"]["LIKE_LIST_XPATH"]

# Wait time set
LOAD_TIME = 10
RENDER_TIME = 1


# Implicit wait function
def wait_presence(wait_target, explicit_time, call_by, element_path):
    """
    =Usage=
    wait_target: implicit wait target scope
    implicit_time: wait time
    call_by: find element by element type (ex: By.CLASS_NAME, By.XPATH)
    element_path: target elememnt path(ex: 'a', ''//*[@id="loginForm"]/div/div[1]/div/label/input')

    =Return=
    found web element
    """
    element = WebDriverWait(wait_target, explicit_time).until(
        EC.element_to_be_clickable((call_by, element_path))
    )
    return element


# Initialize browser
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()
browser.set_window_size(WIDTH, HEIGHT)
browser.get(SITE)

# find login form
login_form = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, FORM_CLS_PATH))
)
id_form = login_form.find_element_by_xpath(ID_XPATH)
pw_form = login_form.find_element_by_xpath(PW_XPATH)

# send login info
id_form.send_keys(ID)
pw_form.send_keys(PW)
pw_form.send_keys(Keys.ENTER)

# wait and click login info btn
check_btn = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, LOGIN_INFO_XPATH))
)
check_btn.send_keys(Keys.ENTER)

# wait and click noti btn
check2_btn = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, NOTI_INFO_XPATH))
)
check2_btn.send_keys(Keys.ENTER)


def get_like_btn(url):
    browser.get(url)
    LIKE_BTN_CONTAINER_PATH = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button'
    like_btn_container = wait_presence(browser, 10, By.XPATH, LIKE_BTN_CONTAINER_PATH)
    return like_btn_container


def is_like_post(url):
    like_btn_container = get_like_btn(url)
    like_status = like_btn_container.find_element(By.TAG_NAME, "svg").get_attribute(
        "aria-label"
    )
    if like_status == "Like":
        return False
    return True


def click_like_target_post(url, wait_time=2):
    like_btn_container = get_like_btn(url)
    isLike = like_btn_container.find_element(By.TAG_NAME, "svg").get_attribute(
        "aria-label"
    )
    if isLike == "Like":
        like_btn_container.send_keys(Keys.ENTER)
    return


def get_top_three_posts(user):
    posts = {}
    browser.get(user)
    # GET user info
    num_posts = wait_presence(browser, 2, By.XPATH, POSTS_XPATH).text
    num_follower = wait_presence(browser, 2, By.XPATH, FOLLOWER_XPATH).text
    num_following = wait_presence(browser, 2, By.XPATH, FOLLOWING_XPATH).text
    user_reactions[user] = {
        "posts": num_posts,
        "follower": num_follower,
        "following": num_following,
        "top_three_posts": {},
    }
    # GET top three posts info
    posts_container = browser.find_element(By.TAG_NAME, POST_TAG_PATH)
    top_three_posts = posts_container.find_elements(By.TAG_NAME, LINK_TAG_PATH)
    links = [post.get_attribute("href") for post in top_three_posts]
    for link in links:
        # click_like_target_post(link)
        if is_like_post(link):
            user_reactions[user]["top_three_posts"][link] = True
        else:
            user_reactions[user]["top_three_posts"][link] = False
    return


POSTS_XPATH = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span'
FOLLOWER_XPATH = (
    '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/span/span'
)
FOLLOWING_XPATH = (
    '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/span/span'
)

# Get top three posts in like
sample_user = "https://www.instagram.com/dev.gon.io/"

user_reactions = {}
# click_like_target_post(sample_user)
get_top_three_posts(sample_user)
print(user_reactions)
# browser.quit()


# Target post consume
time.sleep(3)
browser.get(SITE + ID)

# GET FOLLOWER LIST

###################
FOLLOW_BTN_XPATH = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
follower_btn = browser.find_element(By.XPATH, FOLLOW_BTN_XPATH)
follower_btn.send_keys(Keys.ENTER)
time.sleep(2)


ll_inner_xpath = "/html/body/div[last()]/div/div/div[2]/ul/div"
ll_inner = browser.find_element_by_xpath(ll_inner_xpath)

# Likes 창의 맨 밑이 끝날 때 까지 inner 창 스크롤
end_of_ll = []
ll = ll_inner.find_elements(By.XPATH, "/html/body/div[last()]/div/div/div[2]/ul/div/li")
# /html/body/div[5]/div/div/div[2]/ul/div/li[1]/div/div[3]/button
# /html/body/div[5]/div/div/div[2]/ul/div/li[1]/div/div[2]/div[1]/div/div/span/a
# /html/body/div[5]/div/div/div[2]/ul/div/li/div/div[1]/div[2]/div[1]/span/a
# 브라우저 스크롤링 이전에 가져온 ll(like list)안에서 테스트
while end_of_ll != ll[-1]:
    # Get like info

    for l in ll:
        luser = WebDriverWait(l, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "a"))
        )
        # luser = l.find_element(By.TAG_NAME, "a")
        lbtn = WebDriverWait(l, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "button"))
        )
        # lbtn = l.find_element(By.TAG_NAME, "button")
        print(luser.get_attribute("href"), lbtn.text)

    # Page scrolling
    end_of_ll = ll[-1]
    browser.execute_script("arguments[0].scrollIntoView()", end_of_ll)
    time.sleep(1)
    ll = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/html/body/div[last()]/div/div/div[2]/ul/div/li")
        )
    )
    # ll = browser.find_elements(
    #     By.XPATH, "/html/body/div[last()]/div/div/div[2]/ul/div/li"
    # )


##################
total_size = browser.execute_script(""" return document.body.scrollHeight """)
post_container = browser.find_element_by_tag_name(POST_TAG_PATH)
linkes = post_container.find_elements_by_tag_name(LINK_TAG_PATH)
total_posts = browser.find_element_by_xpath(TOTAL_POSTS_XPATH)

curr_pos = 0
post_reactions = {}
# scroll
time.sleep(2)
while curr_pos + int(HEIGHT) < total_size:
    browser.execute_script(f"window.scrollTo(0, {total_size})")
    curr_pos = browser.execute_script(""" return window.pageYOffset """)
    time.sleep(1.5)
    linkes = WebDriverWait(post_container, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, LINK_TAG_PATH))
    )
    # linkes = post_container.find_elements_by_tag_name(LINK_TAG_PATH)
    total_size = browser.execute_script(""" return document.body.scrollHeight """)
    for l in linkes:
        addr = l.get_attribute("href")
        if addr not in post_reactions:
            # May be not orderble but <3.6 support ordable dictionary
            post_reactions[addr] = {
                # {
                #     "user_name": "",
                #     "react_type": 0,
                #     "comments": [],
                #     "follower": 0,
                #     "following": 0,
                #     "posts": 0,
                #     "top_three_posts": [{"name": "", "liked": False}],
                # }
            }

# Detail each post sample number 2
curr_link = list(post_reactions.keys())[2]
browser.get(curr_link)
time.sleep(2)
post_desc = browser.find_element_by_xpath(POST_DESC_XPATH)
print(post_desc.text)

# Comments
comm_list_xpath = (
    '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul'
)
# try:
comm_list = browser.find_elements(By.XPATH, comm_list_xpath)
# Number 0 comments sample

for idx, cm in enumerate(comm_list):
    time.sleep(0.5)
    comm_user = browser.find_element(
        By.XPATH,
        f'//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul[{idx+1}]/div/li/div/div[1]/div[2]/h3',
    ).text
    comm_text = browser.find_element(
        By.XPATH,
        f'//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul[{idx+1}]/div/li/div/div[1]/div[2]/span',
    ).text
    print(f"[{comm_user}]: {comm_text}")
    comm_more_btn = browser.find_element(
        By.XPATH,
        f'//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul[{idx+1}]/li/ul/li/div/button',
    )
    comm_more_btn.send_keys(Keys.ENTER)
    sub_comm_list = browser.find_elements(
        By.XPATH,
        f'//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul[{idx+1}]/li/ul/div',
    )
    # //*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul[1]/li/ul/div[1]
    # //*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul[1]/li/ul/div[2]
    # //*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul[1]/li/ul/div[1]/li/div/div[1]/div[2]/h3
    # //*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul[1]/li/ul/div[1]/li/div/div[1]/div[2]/span
    for sub_idx, scm in enumerate(sub_comm_list):
        sub_comm_user = browser.find_element(
            By.XPATH,
            f'//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul[{idx+1}]/li/ul/div[{sub_idx+1}]/li/div/div[1]/div[2]/h3',
        ).text
        sub_comm_text = browser.find_element(
            By.XPATH,
            f'//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/ul[{idx+1}]/li/ul/div[{sub_idx+1}]/li/div/div[1]/div[2]/span',
        ).text
        print(f"[{sub_comm_user}]: {sub_comm_text}")

# except Exception as ex:
#     print(f"[NOT FOUND COMMENTS]: {ex}")


# Like list
like_list_btn = browser.find_element_by_xpath(LIKE_LIST_XPATH)
like_list_btn.send_keys(Keys.ENTER)
time.sleep(2)

ll_container_xpath = "/html/body/div[last()]/div/div/div[2]/div"
ll_inner_xpath = "/html/body/div[last()]/div/div/div[2]/div/div"

# ll_container = browser.find_element_by_xpath(ll_container_xpath)
ll_inner = browser.find_element_by_xpath(ll_inner_xpath)

# Likes 창의 맨 밑이 끝날 때 까지 inner 창 스크롤
end_of_ll = []
ll = ll_inner.find_elements(By.CSS_SELECTOR, "div")
lbtns = ll_inner.find_elements(By.TAG_NAME, "button")
lusers = ll_inner.find_elements(By.CSS_SELECTOR, "span>a")
# for i in lbtns:
#     print(i.text)
# for u in lusers:
#     print(u.get_attribute("href"))

# 브라우저 스크롤링 이전에 가져온 ll(like list)안에서 테스트
while end_of_ll != ll[-1]:
    # Get like info
    user_link_list = ll_inner.find_elements(By.CSS_SELECTOR, "span>a")
    for user_link in user_link_list:
        user = user_link.get_attribute("href")
        post_reactions[curr_link][user] = {"react_type": 1, "comments": []}
    # Page scrolling
    end_of_ll = ll[-1]
    browser.execute_script("arguments[0].scrollIntoView()", end_of_ll)
    time.sleep(1)
    ll = ll_inner.find_elements(By.TAG_NAME, "div")


print(post_reactions)

# browser.quit()