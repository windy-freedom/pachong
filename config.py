"""
配置文件
"""
import os
from datetime import datetime

# 基础配置
BASE_URL = "https://www.toolify.ai/"
OUTPUT_DIR = "data"

# 创建输出目录
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 输出文件名（带时间戳）
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    f"toolify_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
)

# 浏览器配置
BROWSER_CONFIG = {
    "headless": True,  # 无头模式
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# 爬虫配置
SCRAPER_CONFIG = {
    "page_load_timeout": 30,  # 页面加载超时时间（秒）
    "scroll_pause_time": 2,   # 滚动暂停时间（秒）
    "max_retries": 3,         # 最大重试次数
    "retry_delay": 5,         # 重试延迟（秒）
}

# CSV文件表头
CSV_HEADERS = ["name", "url", "category", "description", "created_at"]