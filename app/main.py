from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
import time 

driver = webdriver.Chrome()
login_url = "https://www.linkedin.com/"
driver.get(login_url)
time.sleep(2)

wait = WebDriverWait(driver, 20)
button = wait.until(EC.element_to_be_clickable((By.XPATH, "//main[@id='main-content']//a[contains(@class, 'sign-in-form__sign-in-cta')]")))
button.click()
print("Button clicked successfully!")
time.sleep(2)

email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
email_input.send_keys("prasanth33460@gmail.com")
print("Email entered Successfully!")
time.sleep(2)

password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
password_input.send_keys("prasanthXbezos@1234509876")
print("Password entered Successfully!")
time.sleep(2)

sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn__primary--large from__button--floating']")))
sign_in_button.click()
print("Sign in Button clicked!")
time.sleep(2)

try:
    otp_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='input__phone_verification_pin']")))
    print("Please enter the OTP in the browser...")
    wait.until(lambda driver: len(otp_input.get_attribute('value')) == 6)
    otp_value = otp_input.get_attribute('value')
    print(f"OTP detected: {otp_input.get_attribute('value')}")
    time.sleep(2)

    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='two-step-submit-button']")))
    submit_button.click()
    print("Submit button clicked successfully!")
    time.sleep(2)

except Exception as e:
    print("Logged in!")    
    
message_url = "https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=FACETED_SEARCH&sid=*L2"
driver.get(message_url)
time.sleep(2)

all_message_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Message') and contains(@class, 'artdeco-button')]")
message_button = [btn for btn in all_message_buttons if btn.text == "Message"]

for i in range(0, len(message_button)):
    driver.execute_script("arguments[0].click();", message_button[i])
    time.sleep(2)

    main_div = driver.find_element(By.XPATH, "//div[starts-with(@class, 'msg-form__msg-content-container')]")
    driver.execute_script("arguments[0].click();", main_div)

    message = "Sorry, didn't mean to bother you! I am just building a LinkedIn automation tool!"
    paragraph = driver.find_elements(By.TAG_NAME, "p")
    paragraph[-5].send_keys(message)
    print(f"Message entered: {message}")
    time.sleep(2)

    send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'msg-form__send-button')]")))
    send_button.click()
    print("Message sent successfully!")
    time.sleep(2)

    # minimize_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//header[contains(@class, 'msg-overlay-conversation-bubble-header')]/div/button[@id='ember168']")))
    # minimize_button.click()
    # print("Chat minimized successfully.")
    # time.sleep(2)

    close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='ember168']")))
    driver.execute_script("arguments[0].click();", close_button)  
    # close_button.click()
    print("Chat closed successfully.")
    time.sleep(2)