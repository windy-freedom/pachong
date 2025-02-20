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
            
            # 等待工具卡片加载
            self.browser.wait_for_element(By.CSS_SELECTOR, ".tool-card")
            
            # 滚动页面加载更多内容
            self._load_all_tools()
            
            # 解析工具信息
            self._parse_tools()
            
            # 保存数据
            self.parser.save_to_csv()
            
            print("爬取完成！")
            
        except Exception as e:
            print(f"爬取过程出错: {str(e)}")
        
        finally:
            self.browser.close()
    
    def _load_all_tools(self):
        """加载所有工具"""
        print("正在加载所有工具...")
        retry_count = 0
        
        while retry_count < SCRAPER_CONFIG["max_retries"]:
            try:
                # 滚动页面
                self.browser.scroll_page()
                
                # 检查是否到达底部
                if self._check_end_of_page():
                    break
                    
                retry_count = 0  # 重置重试计数
                
            except Exception as e:
                print(f"加载更多内容时出错: {str(e)}")
                retry_count += 1
                time.sleep(SCRAPER_CONFIG["retry_delay"])
    
    def _check_end_of_page(self):
        """检查是否到达页面底部"""
        try:
            # 检查是否存在"加载更多"按钮或相关提示
            end_indicators = self.browser.find_elements(
                By.CSS_SELECTOR, 
                ".end-of-content, .no-more-content"
            )
            return len(end_indicators) > 0
        except:
            return False
    
    def _parse_tools(self):
        """解析所有工具信息"""
        print("正在解析工具信息...")
        
        # 获取所有工具卡片
        tool_cards = self.browser.find_elements(By.CSS_SELECTOR, ".tool-card")
        
        for card in tool_cards:
            # 解析工具信息
            tool_info = self.parser.parse_tool_card(card)
            
            # 添加到数据集
            if tool_info:
                self.parser.add_tool(tool_info)
            
            # 添加短暂延迟避免解析过快
            time.sleep(0.1)
        
        print(f"共找到 {len(tool_cards)} 个工具")

def main():
    """主函数"""
    scraper = ToolifyScraper()
    scraper.run()

if __name__ == "__main__":
    main()