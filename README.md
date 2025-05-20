# 🔍 Automated Word Search Solver Bot

This project is a fully automated bot that solves online word search puzzles in real time. It scrapes the DOM from the game page, detects words using a **Trie data structure**, and simulates human-like drag gestures using **Selenium WebDriver** to input the correct answers.

---

## 🚀 Features

- 🔎 Extracts puzzle grid and word list from the DOM using web scraping  
- 🧠 Uses Trie and 8-directional DFS to efficiently find valid words  
- 🖱️ Simulates human-like drag interactions with `ActionChains`  
- 🔁 Automatically plays multiple rounds with alert handling  

---

## 🛠️ Tech Stack

- **Python 3**  
- **Selenium WebDriver**  
- **Chrome & ChromeDriver**  
- **Trie Data Structure**  
- **Web Scraping**  

---

## 📸 Screenshots

| Initial Grid           | Solving In Action      |
|-----------------------|-----------------------|
| ![Initial Grid](assets/initialGrid.png) | ![Solving In Action](assets/solving_in_action.png) |

---

## 🎬 Bot in Action

![Bot in Action](assets/bot_in_action.gif)
---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/Lazarus-10/wordsesarch_bot.git
cd wordsearch-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the bot
python wordsearch_bot.py 
```