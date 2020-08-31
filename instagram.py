from instagramUserInfo import username, password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Instagram:
    def __init__(self,username,password):
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password
    
    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)

        self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input").send_keys(self.username)
        self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(self.password)

        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
        time.sleep(2)
        self.browser.implicitly_wait(20)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()

        self.browser.implicitly_wait(20)
        self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        

    def getFollowers(self, username, max):
        self.browser.get("https://www.instagram.com/" + username)
        
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        time.sleep(2)
        

        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followerCount = len(dialog.find_elements_by_css_selector("li"))
        print(f"First count: {followerCount}")

        action = webdriver.ActionChains(self.browser)

        while followerCount < max:
            dialog.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)
            followers = dialog.find_elements_by_css_selector("li")
            newCount = len(dialog.find_elements_by_css_selector("li"))

            if followerCount != newCount:
                followerCount = newCount
                print(f"Güncel takipçi sayısı: {newCount}")
                time.sleep(1)
            else:
                followers = dialog.find_elements_by_css_selector("li")
                break

        followerList = []
        i = 0
        for user in followers:
            try:
                link = user.find_element_by_css_selector("a").get_attribute("href")
                followerList.append(link)
                
                i += 1
                if i == max:
                    break
            except:
                break
        
        with open("followers.txt", "w", encoding="UTF-8") as file:
            for item in followerList:
                file.write(item + "\n")

    def followUser(self, username):
        self.browser.get("https://www.instagram.com/" + username)
        time.sleep(2)
        
        try: 
            followButton = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button')
            followButton.click()
        except:
            print("Zaten takip ediyorsunuz")

    def unFollow(self, username):
        self.browser.get("https://www.instagram.com/"+ username)
        time.sleep(1)

        try:
           self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button').click()
           self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()
        except:
            print("Zaten takip etmiyorsunuz")

        
        
       

instagram = Instagram(username,password)
instagram.signIn()
instagram.getFollowers("zuleyha_ooz", 50)
# instagram.followUser("bakircay_bilmuh")
# instagram.unFollow("bakircay_bilmuh")