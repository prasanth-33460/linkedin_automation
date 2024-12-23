from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
import time 
import random
from fastapi import FastAPI

app = FastAPI()

class LinkedInAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        
    def random_sleep(self):
        delay = random.uniform(1,5)
        time.sleep(delay)
        print(f"Paused for {delay:.2f} seconds.")  
    
    def login(self,email, password):
        try:
            login_url = "https://www.linkedin.com/"
            self.driver.get(login_url)
            self.driver.maximize_window()
            self.random_sleep()

            button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//main[@id='main-content']//a[contains(@class, 'sign-in-form__sign-in-cta')]")))
            button.click()
            print("Button clicked successfully!")
            self.random_sleep()

            email_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
            email_input.send_keys(email)
            print("Email entered Successfully!")
            self.random_sleep()

            password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
            password_input.send_keys(password)
            print("Password entered Successfully!")
            self.random_sleep()

            sign_in_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn__primary--large from__button--floating']")))
            sign_in_button.click()
            print("Sign in Button clicked!")
            self.random_sleep()
            try:
                otp_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='input__phone_verification_pin']")))
                print("Please enter the OTP in the browser...")
                self.wait.until(lambda driver: len(otp_input.get_attribute('value')) == 6)
                print(f"OTP detected: {otp_input.get_attribute('value')}")
                self.random_sleep()

                submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='two-step-submit-button']")))
                submit_button.click()
                print("Submit button clicked successfully!")
                self.random_sleep()
            except Exception as otp_exception:
                print("OTP step skipped or not required.")
        except Exception as e:
            print(f"Error during login: {e}")
    
    def send_messages(self, message_url, message):
        try:
            self.driver.get(message_url)
            self.random_sleep()
            
            while True:
                all_message_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Message') and contains(@class, 'artdeco-button')]")
                message_button = [btn for btn in all_message_buttons if btn.text == "Message"]
                for i in range(0, len(message_button)):
                    try:
                        self.driver.execute_script("arguments[0].click();", message_button[i])
                        self.random_sleep()

                        main_div = self.driver.find_element(By.XPATH, "//div[starts-with(@class, 'msg-form__msg-content-container')]")
                        self.driver.execute_script("arguments[0].click();", main_div)

                        paragraph = self.driver.find_elements(By.TAG_NAME, "p")
                        paragraph[-5].send_keys(message)
                        print(f"Message entered: {message}")
                        self.random_sleep()

                        send_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'msg-form__send-button')]")))
                        send_button.click()
                        print("Message sent successfully!")
                        self.random_sleep()

                        # minimize_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//header[contains(@class, 'msg-overlay-conversation-bubble-header')]/div/button[@id='ember168']")))
                        # minimize_button.click()
                        # print("Chat minimized successfully.")
                        # self.random_sleep()

                        close_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'msg-overlay-bubble-header__controls')]//button[contains(., 'Close')]")))
                        self.driver.execute_script("arguments[0].click();", close_button)  
                        print("Chat closed successfully.")
                        self.random_sleep()
                        
                    except Exception as message_exception:
                        print(f"Error during message sending for recipient {i}: {message_exception}")
                        
                try:
                    next_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Next']")
                    if next_button.is_enabled():
                        self.driver.execute_script("arguments[0].scrollIntoView();", next_button)
                        next_button.click()
                        print("Navigated to next page.")
                        self.random_sleep()
                    else:
                        print("No more pages to navigate.")
                        break
                except Exception as pagination_exception:
                    print(f"Error during pagination or no next button: {pagination_exception}")
                    break
        except Exception as e:
            print(f"Error accessing message URL or sending messages: {e}")
    
    def send_connection(self, second_url):
        try:
            self.driver.get(second_url)
            print("Navigating to the page...")
            self.random_sleep()
            
            while True:
                try:
                    connect_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@aria-label, "Invite")]')
                    follow_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@aria-label, "Follow")]')
                    print("Elements are visible on the page.")
                except Exception as e:
                    print(f"Error waiting for elements: {e}")
                    break

                print(f"Found {len(connect_buttons)} Connect buttons and {len(follow_buttons)} Follow buttons.")
                
                for button in connect_buttons:
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView();", button)                
                        self.driver.execute_script("arguments[0].click();", button)
                        print("Clicked a Connect button.")
                        self.random_sleep()
                        
                        try:
                            send_without_note_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Send without a note")]')))
                            self.driver.execute_script("arguments[0].click();", send_without_note_button)
                            print("Clicked 'Send without a note' button.")
                            self.random_sleep()
                        except Exception:
                            print("No 'Send without a note' button found.")
                            
                        try:
                            send_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Send invitation")]')))
                            self.driver.execute_script("arguments[0].click();", send_button)
                            print("Clicked the Send button.")
                            self.random_sleep()
                        except Exception:
                            print("No 'send' button found.")
                            
                        try:
                            got_it_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Got it")]')))
                            self.driver.execute_script("arguments[0].click();", got_it_button)
                            print("Clicked the Got it button.")
                            self.random_sleep()
                        except Exception:
                            print("No 'Got it' pop-up appeared.")
                    except Exception as inner_e:
                        print(f"Could not click a button: {inner_e}")   
                
                for follow_button in follow_buttons:
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView();", follow_button)
                        self.driver.execute_script("arguments[0].click();", follow_button)
                        print("Clicked a 'Follow' button.")
                        self.random_sleep()
                    except Exception as follow_e:
                        print(f"Could not click a 'Follow' button: {follow_e}")

                try:
                    next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Next")]')))
                    self.driver.execute_script("arguments[0].click();", next_button)
                    print("Clicked the 'Next' button for pagination.")
                    self.random_sleep()
                except Exception:
                    print("No 'Next' button found or reached the last page.")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")            
        
    def close(self):
        try:
            self.driver.quit()
            print("Driver closed successfully.")
        except Exception as e:
            print(f"Error during driver close: {e}")

@app.get('/')            
def main():
    email = "prasanth33460@gmail.com"
    password = "prasanthXbezos@1234509876"
    message_url = "https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=FACETED_SEARCH&sid=*L2"
    message = "Sorry, didn't mean to bother you! I am just building a LinkedIn automation tool!"
    second_url = "https://www.linkedin.com/search/results/people/?network=%5B%22S%22%5D&origin=FACETED_SEARCH&sid=0cY"

    bot = LinkedInAutomation()
    bot.login(email, password)
    bot.send_messages(message_url, message)
    bot.send_connection(second_url)
    bot.close()