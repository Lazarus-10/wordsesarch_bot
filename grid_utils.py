from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from constants import GRID_CELL_CLASS, WORD_LIST_CLASS, GRID_SIZE, WAIT_TIMEOUT, POLL_FREQUENCY

def wait_for_grid(driver):
    WebDriverWait(driver, WAIT_TIMEOUT, POLL_FREQUENCY).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, GRID_CELL_CLASS))
    )

def wait_for_word_list(driver):
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, WORD_LIST_CLASS))
    )

def extract_grid(driver):
    cells = driver.find_elements(By.CLASS_NAME, GRID_CELL_CLASS)
    grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for cell in cells:
        i = int(cell.get_attribute("row"))
        j = int(cell.get_attribute("col"))
        grid[i][j] = cell.text
    return grid

def extract_words(driver):
    try:
        word_list = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, WORD_LIST_CLASS))
        )
        return set([word.text for word in word_list.find_elements(By.XPATH, './/a')])
    except TimeoutException:
        return set()
