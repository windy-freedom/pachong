"""
数据解析模块
"""
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By
from config import CSV_HEADERS, OUTPUT_FILE

class DataParser:
    def __init__(self):
        """初始化数据解析器"""
        self.data = []

    def parse_tool_card(self, element):
        """解析工具卡片元素
        
        Args:
            element: 工具卡片元素
            
        Returns:
            dict: 工具信息
        """
        try:
            # 提取工具名称
            name = element.find_element(By.CSS_SELECTOR, "h2").text.strip()
            
            # 提取工具链接
            url = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            
            # 提取分类（如果有）
            try:
                category = element.find_element(By.CSS_SELECTOR, ".category").text.strip()
            except:
                category = "未分类"
            
            # 提取描述（如果有）
            try:
                description = element.find_element(By.CSS_SELECTOR, ".description").text.strip()
            except:
                description = ""
            
            # 创建工具信息字典
            tool_info = {
                "name": name,
                "url": url,
                "category": category,
                "description": description,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return tool_info
            
        except Exception as e:
            print(f"解析工具卡片出错: {str(e)}")
            return None

    def add_tool(self, tool_info):
        """添加工具信息到数据列表
        
        Args:
            tool_info (dict): 工具信息
        """
        if tool_info:
            self.data.append(tool_info)

    def save_to_csv(self):
        """保存数据到CSV文件"""
        try:
            # 转换为DataFrame
            df = pd.DataFrame(self.data)
            
            # 重排列顺序
            df = df.reindex(columns=CSV_HEADERS)
            
            # 保存到CSV
            df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
            print(f"数据已保存到: {OUTPUT_FILE}")
            print(f"共收集了 {len(self.data)} 个工具信息")
            
        except Exception as e:
            print(f"保存CSV文件出错: {str(e)}")

    def get_data_count(self):
        """获取已收集的数据数量"""
        return len(self.data)