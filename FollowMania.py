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
xpath_posts = "//div//article//a"
count = 0

def login(driver):
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password) 
    driver.find_element_by_name("password").send_keys(u'\ue007')

def click_button_with_css(driver, css_selector):
    element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    element.click()
def click_button_with_xpath(driver, xpath):
    element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()

def naviagate_to_followers(driver):
    dropdown_css = '[alt*="' + username + '"]'
    profile_css = "[href*=\"" + username + "\"]"
    click_button_with_css(driver, dropdown_css)
    click_button_with_css(driver, profile_css)


def __main__():
    global xpath_posts
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    login(driver)
    search_css = "[placeholder=\"Search\"]"
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, search_css)))
    
    driver.find_element_by_css_selector(search_css).send_keys('#starwars')
    starwars_hashtag = "[href=\"/explore/tags/starwars/\"]"
    click_button_with_css(driver, starwars_hashtag)
    starting_element = 0
    for j in range(20):

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, xpath_posts)))
        scroll_down(driver)
        posts = driver.find_elements_by_xpath(xpath_posts)
        num = 0
        for i in range(len(posts)):
            try:
                posts[i + starting_element].click()
                follow_button_xpath = "//div/div/div/button"
                WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, follow_button_xpath)))
                element = driver.find_elements_by_xpath(follow_button_xpath)[0]
                print (element.text)
                if ("Following" not in element.text):
                    element.click()
                    num+=1
                close_button = driver.find_elements_by_css_selector("[type=\"button\"]")[::-1][0]
                close_button.click()
            except:
                print("caught exception, continuing")
        starting_element = len(posts)
    print ("You followed" + str(num) + " accounts")

def check_difference_in_count(driver):
    global count
    if count < 3:
        count += 1
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
        driver.execute_script("window.scroll(0," + scroll_top_num +")")
        time.sleep(1)
        try:
            WebDriverWait(driver, 1).until(check_difference_in_count)
        except:
            count = 0
            break




__main__()
#elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
#driver.close()
