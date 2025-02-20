"""
Toolify.ai 爬虫主程序
"""
import time
from selenium.webdriver.common.by import By
from utils import BrowserManager, DataParser
from config import BASE_URL, SCRAPER_CONFIG

class ToolifyScraper:
    def __init__(self):
        """初始化爬虫"""
        self.browser = BrowserManager()
        self.parser = DataParser()
        
    def run(self):
        """运行爬虫"""
        try:
            print("开始爬取Toolify.ai...")
            
            # 访问主页
            if not self.browser.get_page(BASE_URL):
                raise Exception("无法访问网站")
            
            # 等待页面加载完成
            self.browser.wait_for_element(By.CSS_SELECTOR, "body")
            
            # 尝试不同的选择器来定位工具卡片
            selectors = [
                ".tool-card",
                "[class*='card']",
                "[class*='tool']",
                "article",
                ".items > div"
            ]
            
            tool_cards = None
            for selector in selectors:
                print(f"尝试使用选择器: {selector}")
                if self.browser.wait_for_element(By.CSS_SELECTOR, selector):
                    tool_cards = selector
                    break
            
            if not tool_cards:
                raise Exception("无法找到工具卡片元素")
                
            print(f"成功找到工具卡片，使用选择器: {tool_cards}")
            
            # 滚动页面加载更多内容
            self._load_all_tools(tool_cards)
            
            # 解析工具信息
            self._parse_tools(tool_cards)
            
            # 保存数据
            self.parser.save_to_csv()
            
            print("爬取完成！")
            
        except Exception as e:
            print(f"爬取过程出错: {str(e)}")
        
        finally:
            self.browser.close()
    
    def _load_all_tools(self, selector):
        """加载所有工具"""
        print("正在加载所有工具...")
        retry_count = 0
        last_count = 0
        
        while retry_count < SCRAPER_CONFIG["max_retries"]:
            try:
                # 滚动页面
                self.browser.scroll_page()
                
                # 获取当前工具数量
                current_tools = self.browser.find_elements(By.CSS_SELECTOR, selector)
                current_count = len(current_tools)
                
                print(f"当前已加载 {current_count} 个工具")
                
                # 如果连续两次数量相同，可能已到达底部
                if current_count == last_count:
                    retry_count += 1
                else:
                    retry_count = 0  # 重置重试计数
                    
                last_count = current_count
                time.sleep(SCRAPER_CONFIG["scroll_pause_time"])
                
            except Exception as e:
                print(f"加载更多内容时出错: {str(e)}")
                retry_count += 1
                time.sleep(SCRAPER_CONFIG["retry_delay"])
    
    def _parse_tools(self, selector):
        """解析所有工具信息"""
        print("正在解析工具信息...")
        
        try:
            # 获取所有工具卡片
            tool_cards = self.browser.find_elements(By.CSS_SELECTOR, selector)
            
            if not tool_cards:
                print("未找到任何工具卡片")
                return
            
            print(f"开始解析 {len(tool_cards)} 个工具")
            
            for index, card in enumerate(tool_cards, 1):
                try:
                    # 解析工具信息
                    tool_info = self.parser.parse_tool_card(card)
                    
                    # 添加到数据集
                    if tool_info:
                        self.parser.add_tool(tool_info)
                        print(f"成功解析第 {index} 个工具: {tool_info['name']}")
                    
                    # 添加短暂延迟避免解析过快
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"解析第 {index} 个工具时出错: {str(e)}")
                    continue
            
            print(f"解析完成，共成功解析 {self.parser.get_data_count()} 个工具")
            
        except Exception as e:
            print(f"解析工具信息时出错: {str(e)}")

def main():
    """主函数"""
    scraper = ToolifyScraper()
    scraper.run()

if __name__ == "__main__":
    main()