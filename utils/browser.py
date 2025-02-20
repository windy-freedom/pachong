"""
浏览器管理模块
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from config import BROWSER_CONFIG, SCRAPER_CONFIG

class BrowserManager:
    def __init__(self):
        """初始化浏览器管理器"""
        self.driver = None
        self.setup_browser()

    def setup_browser(self):
        """配置并启动浏览器"""
        options = Options()
        if BROWSER_CONFIG["headless"]:
            options.add_argument("--headless")
        options.add_argument(f'user-agent={BROWSER_CONFIG["user_agent"]}')
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(SCRAPER_CONFIG["page_load_timeout"])

    def get_page(self, url):
        """访问页面
        
        Args:
            url (str): 目标URL
            
        Returns:
            bool: 是否成功访问
        """
        try:
            self.driver.get(url)
            return True
        except TimeoutException:
            print(f"页面加载超时: {url}")
            return False
        except WebDriverException as e:
            print(f"访问页面出错: {str(e)}")
            return False

    def scroll_page(self):
        """滚动页面到底部以加载更多内容"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # 滚动到底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # 等待页面加载
            time.sleep(SCRAPER_CONFIG["scroll_pause_time"])
            
            # 计算新的滚动高度并与上一个滚动高度进行比较
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def wait_for_element(self, by, value, timeout=10):
        """等待元素出现
        
        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间（秒）
            
        Returns:
            element: 找到的元素，如果未找到返回None
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"等待元素超时: {value}")
            return None

    def find_elements(self, by, value):
        """查找所有匹配的元素
        
        Args:
            by: 定位方式
            value: 定位值
            
        Returns:
            list: 元素列表
        """
        try:
            return self.driver.find_elements(by, value)
        except WebDriverException as e:
            print(f"查找元素出错: {str(e)}")
            return []

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None