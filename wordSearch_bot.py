from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

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
            else:
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
            start = driver.find_element(by=By.XPATH, value=f'//div[@class="Grid_gridCell__1L1O2" and @row={start_i} and @col={start_j}]')
            end = driver.find_element(by=By.XPATH, value=f'//div[@class="Grid_gridCell__1L1O2" and @row={i} and @col={j}]')
            action = ActionChains(driver)
            action.drag_and_drop(start, end)
            action.perform()
        i += i_diff
        j += j_diff


def solve(grid, words):
    moves = []
    trie = Trie(words)
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            if grid[i][j] in trie.children:
                for i_diff, j_diff in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    check(grid, trie, i, j, i_diff, j_diff, moves)
    return moves


driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://wordsearch.samsonn.com/')
while True:
    time.sleep(1)
    n, m = 15, 15
    grid = [['']*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            cell = driver.find_element(by=By.XPATH, value=f'//div[@class="Grid_gridCell__1L1O2" and @row={i} and @col={j}]')
            grid[i][j] = cell.text
    word_list = driver.find_element(by=By.XPATH, value='//div[@class="WordList_wordList__3da04"]')
    words = set([word.text for word in word_list.find_elements(by=By.XPATH, value='//a')])
    solve(grid, words)
    time.sleep(2)
    driver.switch_to.alert.accept()