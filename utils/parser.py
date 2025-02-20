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
            # 尝试不同的选择器来提取工具名称
            name = None
            
            # 首先尝试直接从链接文本获取名称
            try:
                link = element.find_element(By.TAG_NAME, "a")
                name = link.text.strip()
            except:
                pass
                
            # 如果链接没有文本，尝试其他选择器
            if not name:
                selectors = [
                    "h2", "h3", "h4",
                    "a h2", "a h3", "a h4",
                    ".title", "[class*='name']", "[class*='title']",
                    "a .title", "a [class*='name']", "a [class*='title']",
                    "[class*='heading']", "a [class*='heading']"
                ]
                for selector in selectors:
                    try:
                        name_element = element.find_element(By.CSS_SELECTOR, selector)
                        name = name_element.text.strip()
                        if name:
                            break
                    except:
                        continue
            
            # 过滤掉不合法的工具名称
            if name:
                # 移除常见的广告和标签文本
                invalid_names = [
                    "Sponsored by",
                    "Just launched",
                    "Featured",
                    "New",
                    "Today",
                    "Most Used",
                    "Most Saved"
                ]
                
                # 检查是否是无效名称
                if any(invalid.lower() in name.lower() for invalid in invalid_names):
                    name = None
                
                # 确保名称长度合适且不包含特殊字符
                elif len(name) < 2 or name.count('\n') > 0 or name.count('-') > 2:
                    name = None
            
            if not name:
                print("无法提取工具名称")
                return None
                
            # 尝试提取工具链接
            url = None
            try:
                # 首先尝试从父元素获取链接
                url = element.get_attribute("href")
                if not url:
                    # 然后尝试从子元素获取链接
                    link_element = element.find_element(By.CSS_SELECTOR, "a")
                    url = link_element.get_attribute("href")
            except:
                # 如果都失败了，记录错误但继续处理
                print(f"警告: 无法获取工具 '{name}' 的链接")
                url = ""
            
            # 尝试不同的选择器来提取分类
            category = "未分类"
            for selector in [".category", "[class*='category']", "[class*='tag']", ".pill"]:
                try:
                    category_element = element.find_element(By.CSS_SELECTOR, selector)
                    category_text = category_element.text.strip()
                    if category_text:
                        category = category_text
                        break
                except:
                    continue
            
            # 尝试不同的选择器来提取描述
            description = ""
            selectors = [
                ".description",
                "[class*='desc']",
                "[class*='content']",
                "p:not(:empty)",  # 非空段落
                "[class*='text']:not(:empty)",  # 非空文本容器
                "[class*='info'] p",  # info容器中的段落
                "div > p:not(:empty)"  # 直接子段落
            ]
            
            for selector in selectors:
                try:
                    desc_elements = element.find_elements(By.CSS_SELECTOR, selector)
                    for desc_element in desc_elements:
                        desc_text = desc_element.text.strip()
                        # 确保描述不是名称的重复，且长度合适
                        if desc_text and desc_text != name and len(desc_text) > 10:
                            description = desc_text
                            break
                    if description:  # 如果找到了合适的描述就退出循环
                        break
                except:
                    continue
            
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