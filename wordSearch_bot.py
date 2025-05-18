from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Trie:
    def __init__(self, words=None):
        self.children = {}
        self.is_end = False
        if words:
            for word in words:
                self.insert(word)

    def insert(self, s):
        node = self
        for ch in s:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_end = True

    def search(self, s):
        node = self
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node if node.is_end else None

    def delete(self, s):
        def rec(node, s, i):
            if i == len(s):
                node.is_end = False
                return len(node.children) == 0
				 
            next_deletion = rec(node.children[s[i]], s, i+1)
            if next_deletion:
                del node.children[s[i]]
            return next_deletion and not node.is_end and len(node.children) == 0
        if self.search(s):
            rec(self, s, 0)

    def get_strings(self):
        def rec(node, string, strings):
            if node.is_end:
                strings.append("".join(string))
            for ch in node.children:
                string.append(ch)
                rec(node.children[ch], string, strings)
                string.pop()
        strings = []
        rec(self, [], strings)
        return strings
    
def check(grid, trie, i, j, i_diff, j_diff, moves):
    n, m = len(grid), len(grid[0])
    node = trie
    start_i, start_j = i, j
    substring = ''
    while 0 <= i < n and 0 <= j < m and grid[i][j] in node.children:
        substring += grid[i][j]
        node = node.children[grid[i][j]]
        if node.is_end:
            moves.append(((start_i, start_j), (i, j)))
            trie.delete(substring)
            try:
                start = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f'//div[@class="Grid_gridCell__1L1O2" and @row={start_i} and @col={start_j}]')))
                end = driver.find_element(By.XPATH, f'//div[@class="Grid_gridCell__1L1O2" and @row={i} and @col={j}]')
                action = ActionChains(driver)
                action.click_and_hold(start).move_to_element(end).release().perform()
            except (TimeoutException, NoSuchElementException):
                pass
        i += i_diff
        j += j_diff


def solve(grid, words, driver):
    moves = []
    trie = Trie(words)
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            if grid[i][j] in trie.children:
                for i_diff, j_diff in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    check(grid, trie, i, j, i_diff, j_diff, moves, driver)
    return moves

def wait_for_grid(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Grid_gridCell__1L1O2"))
    )

def wait_for_word_list(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, "WordList_wordList__3da04"))
    )

def extract_grid(driver, n=15, m=15):
    grid = [[''] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            try:
                cell = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'//div[@class="Grid_gridCell__1L1O2" and @row={i} and @col={j}]'))
                )
                grid[i][j] = cell.text
            except TimeoutException:
                grid[i][j] = ''
    return grid

def extract_words(driver):
    try:
        word_list = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "WordList_wordList__3da04"))
        )
        return set([word.text for word in word_list.find_elements(By.XPATH, './/a')])
    except TimeoutException:
        return set()

# Driver setup
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

        solve(grid, words, driver)

        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except TimeoutException:
            break
        round_count += 1
finally:
    driver.quit()