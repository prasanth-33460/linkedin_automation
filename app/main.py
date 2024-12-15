from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
import time 


class LinkedInAutomation:
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
    
    def login(self,email, password):
        try:
            login_url = "https://www.linkedin.com/"
            self.driver.get(login_url)
            time.sleep(2)

            button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//main[@id='main-content']//a[contains(@class, 'sign-in-form__sign-in-cta')]")))
            button.click()
            print("Button clicked successfully!")
            time.sleep(2)

            email_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
            email_input.send_keys(email)
            print("Email entered Successfully!")
            time.sleep(2)

            password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
            password_input.send_keys(password)
            print("Password entered Successfully!")
            time.sleep(2)

            sign_in_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn__primary--large from__button--floating']")))
            sign_in_button.click()
            print("Sign in Button clicked!")
            time.sleep(2)

            try:
                otp_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='input__phone_verification_pin']")))
                print("Please enter the OTP in the browser...")
                self.wait.until(lambda driver: len(otp_input.get_attribute('value')) == 6)
                print(f"OTP detected: {otp_input.get_attribute('value')}")
                time.sleep(2)

                submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='two-step-submit-button']")))
                submit_button.click()
                print("Submit button clicked successfully!")
                time.sleep(2)

            except Exception as otp_exception:
                print("OTP step skipped or not required.")
        
        except Exception as e:
            print(f"Error during login: {e}")
    
    
    def send_messages(self, message_url, message):
        try:
            self.driver.get(message_url)
            time.sleep(2)
            
            while True:
                all_message_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Message') and contains(@class, 'artdeco-button')]")
                message_button = [btn for btn in all_message_buttons if btn.text == "Message"]

                for i in range(7, len(message_button)):
                    try:
                        self.driver.execute_script("arguments[0].click();", message_button[i])
                        time.sleep(2)

                        main_div = self.driver.find_element(By.XPATH, "//div[starts-with(@class, 'msg-form__msg-content-container')]")
                        self.driver.execute_script("arguments[0].click();", main_div)

                        paragraph = self.driver.find_elements(By.TAG_NAME, "p")
                        paragraph[-5].send_keys(message)
                        print(f"Message entered: {message}")
                        time.sleep(2)

                        send_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'msg-form__send-button')]")))
                        send_button.click()
                        print("Message sent successfully!")
                        time.sleep(2)

                        # minimize_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//header[contains(@class, 'msg-overlay-conversation-bubble-header')]/div/button[@id='ember168']")))
                        # minimize_button.click()
                        # print("Chat minimized successfully.")
                        # time.sleep(2)

                        close_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='ember168']")))
                        self.driver.execute_script("arguments[0].click();", close_button)  
                        print("Chat closed successfully.")
                        time.sleep(2)
                        
                    except Exception as message_exception:
                        print(f"Error during message sending for recipient {i}: {message_exception}")
                        
                try:
                    next_button = self.driver.find_element(By.XPATH, "//button[@id='ember140']")
                    if next_button.is_enabled():
                        next_button.click()
                        print("Navigated to next page.")
                        time.sleep(3)
                    else:
                        print("No more pages to navigate.")
                        break
                except Exception as pagination_exception:
                    print(f"Error during pagination or no next button: {pagination_exception}")
                    break
        except Exception as e:
            print(f"Error accessing message URL or sending messages: {e}")
            
    def close(self):
        try:
            self.driver.quit()
            print("Driver closed successfully.")
        except Exception as e:
            print(f"Error during driver close: {e}")
            
if __name__ == "__main__":
    email = "prasanth33460@gmail.com"
    password = "prasanthXbezos@1234509876"
    message_url = "https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=FACETED_SEARCH&sid=*L2"
    message = "Sorry, didn't mean to bother you! I am just building a LinkedIn automation tool!"

    bot = LinkedInAutomation()
    bot.login(email, password)
    bot.send_messages(message_url, message)
    bot.close()