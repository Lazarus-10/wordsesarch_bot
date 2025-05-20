from selenium import webdriver
from grid_utils import wait_for_grid, wait_for_word_list, extract_grid, extract_words
from trie import Trie
from solver import solve
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://wordsearch.samsonn.com/')

try:
    round_count = 0
    while round_count < 3:
        wait_for_grid(driver)
        wait_for_word_list(driver)

        grid = extract_grid(driver)
        words = extract_words(driver)

        solve(grid, words, driver, Trie)

        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except TimeoutException:
            break
        round_count += 1
finally:
    driver.quit()
