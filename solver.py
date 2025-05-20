from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from constants import DIRECTIONS, GRID_CELL_CLASS

def check(grid, trie, i, j, i_diff, j_diff, moves, driver):
    n, m = len(grid), len(grid[0])
    node = trie.root
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
                    EC.presence_of_element_located((By.XPATH, f'//div[@class="{GRID_CELL_CLASS}" and @row={start_i} and @col={start_j}]')))
                end = driver.find_element(By.XPATH, f'//div[@class="{GRID_CELL_CLASS}" and @row={i} and @col={j}]')
                ActionChains(driver).click_and_hold(start).move_to_element(end).release().perform()
            except (TimeoutException, NoSuchElementException):
                pass
        i += i_diff
        j += j_diff

def solve(grid, words, driver, trie_class):
    moves = []
    trie = trie_class(words)
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            if grid[i][j] in trie.root.children:
                for i_diff, j_diff in DIRECTIONS:
                    check(grid, trie, i, j, i_diff, j_diff, moves, driver)
    return moves
