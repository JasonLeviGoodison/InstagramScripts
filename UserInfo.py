from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 



username_css = '@name=\'username\''
passowrd_css = 'name="password"'
username = 'username'
password = 'password'
count = 0


def login(driver):
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password) 
    driver.find_element_by_name("password").send_keys(u'\ue007')

def click_button_with_css(driver, css_selector):
    element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    element.click()

def naviagate_to_followers(driver):
    dropdown_css = '[alt*="' + username + '"]'
    profile_css = "[href*=\"" + username + "\"]"
    click_button_with_css(driver, dropdown_css)
    click_button_with_css(driver, profile_css)


def __main__():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    time.sleep(1)

    login(driver)
    naviagate_to_followers(driver)

    try:
        click_button_with_css(driver, "[href*=\"" + username + "/followers/\"]")
    except:
        print("auto opened this time")
    
    followers = get_list_from_dialog(driver)

    css_select_close = '[aria-label="Close"]'
    click_button_with_css(driver, css_select_close)
    click_button_with_css(driver, "[href*=\"" + username + "/following/\"]")

    following = get_list_from_dialog(driver)
    unfollow_list = no_followback(followers, following)
    print ("You follow the following people who do not follow you back:")
    for i in range(len(unfollow_list)):
        print (unfollow_list[i])
    time.sleep(200)

def no_followback(followers, following):
    followers.sort()
    following.sort()
    no_followback_list = []
    for i in range(len(following)):
        try:
            followers.index(following[i])
        except ValueError:
            no_followback_list += [following[i]]
    return no_followback_list

def get_list_from_dialog(driver):
    list_xpath ="//div[@role='dialog']//li"
    WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, list_xpath)))

    scroll_down(driver)

    list_elems = driver.find_elements_by_xpath(list_xpath)
    users = []

    for i in range(len(list_elems)):
        try:
            row_text = list_elems[i].text
            if ("Follow" in row_text):
                username = row_text[:row_text.index("\n")]
                users += [username]
        except:
            print("continue")
    return users

def check_difference_in_count(driver):
    global count

    new_count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))

    if count != new_count:
        count = new_count
        return True
    else:
        return False

def scroll_down(driver):
    global count
    iter = 1
    while 1:
        scroll_top_num = str(iter * 1000)
        iter += 1
        # scroll down
        driver.execute_script("document.querySelector('div[role=dialog] ul').parentNode.scrollTop=" + scroll_top_num)
        try:
            WebDriverWait(driver, 1).until(check_difference_in_count)
        except:
            count = 0
            break




__main__()
