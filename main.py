from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import random, sys, time

words = open('words.txt', 'r').readlines()

used_words = []

def get_word(matching):
    wordz = []
    for word in words:
        if matching in word and word not in used_words:
            wordz.append(word)
    rand = random.choice(wordz)
    used_words.append(rand)
    return rand

def startBot(url):
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/form/div[2]/input"))).clear()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/form/div[2]/input"))).send_keys(nick)
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/form/div[2]/button"))).click()

    sys.stdout.write(f'[+] Launched game as {nick} \n')
    sys.stdout.flush()
    
    frame = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[4]/div[1]/iframe")))

    driver.switch_to.frame(frame)

    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div[1]/div[1]/button"))).click()

    sys.stdout.write(f'[+] Joined game as {nick} \n')
    sys.stdout.flush()
    time.sleep(0.5)
    text = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div/header"))).text
    while 'Round' not in text:
        time.sleep(1)
    
    time.sleep(15)
    sys.stdout.write(f'[INFO] Round has started. \n')
    sys.stdout.flush()
    wait4 = WebDriverWait(driver, 0.4)
    while True:
        try:
            time.sleep(0.4)
            try:
                turn = wait4.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[1]/span[1]"))).text
            except TimeoutException:
                syllable = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/div"))).text
                word = get_word(syllable.upper())
                for char in word:
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[2]/form/input"))).send_keys(char)
                sys.stdout.write(f'[+] Used the word "{word[:-1]}". \n')
                sys.stdout.flush()
        except Exception as e:
            pass

nick = input('Nick: ')
link = input('Link: ')
startBot(link)
