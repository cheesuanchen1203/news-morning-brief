"""
新闻抓取工具
使用联网搜索获取指定新闻网站的头条内容
"""

from langchain.tools import tool
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from datetime import datetime
import json

# 新闻网站配置
NEWS_SITES = [
    # 国内科技
    {
        "name": "36氪",
        "url": "36kr.com",
        "category": "科技"
    },
    {
        "name": "IT之家",
        "url": "ithome.com",
        "category": "科技"
    },
    # 国际科技
    {
        "name": "TechCrunch",
        "url": "techcrunch.com",
        "category": "科技"
    },
    {
        "name": "The Verge",
        "url": "theverge.com",
        "category": "科技"
    },
    # 国内经济
    {
        "name": "华尔街见闻",
        "url": "wallstreetcn.com",
        "category": "经济"
    },
    {
        "name": "财联社",
        "url": "cls.cn",
        "category": "经济"
    },
    # 国际经济
    {
        "name": "彭博社",
        "url": "bloomberg.com",
        "category": "经济"
    },
    {
        "name": "路透社",
        "url": "reuters.com",
        "category": "经济"
    },
    {
        "name": "华尔街日报",
        "url": "wsj.com",
        "category": "经济"
    },
    {
        "name": "金融时报",
        "url": "ft.com",
        "category": "经济"
    },
    # 国内政治/社会
    {
        "name": "澎湃新闻",
        "url": "thepaper.cn",
        "category": "政治/社会"
    },
    # 国际政治/社会
    {
        "name": "BBC新闻",
        "url": "bbc.com",
        "category": "政治/社会"
    },
    {
        "name": "CNN",
        "url": "cnn.com",
        "category": "政治/社会"
    },
    {
        "name": "纽约时报",
        "url": "nytimes.com",
        "category": "政治/社会"
    }
]


@tool
def fetch_news() -> str:
    """
    从全球多个权威新闻网站抓取最新新闻（最近3天）
    
    抓取范围（覆盖国内外）：
    - 科技：36氪、IT之家、TechCrunch、The Verge
    - 经济：华尔街见闻、财联社、彭博社、路透社、华尔街日报、金融时报
    - 政治/社会：澎湃新闻、BBC新闻、CNN、纽约时报
    
    注意：由于部分国际媒体在中文搜索服务中的索引有限，实际获取到的新闻来源可能有所差异
    
    返回格式：
    JSON格式的新闻列表，每个新闻包含标题、链接、来源和类别
    """
    all_news = []
    errors = []
    
    # 获取今天的日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 为每个媒体搜索最新新闻
    for site in NEWS_SITES:
        try:
            ctx = new_context(method="search.web")
            client = SearchClient(ctx=ctx)
            
            # 使用媒体名称作为搜索关键词
            query = f"{site['name']} 最新消息"
            response = client.search(
                query=query,
                search_type="web",
                count=8,
                time_range="3d",  # 搜索最近3天的内容
                need_summary=False
            )
            
            if response.web_items:
                for item in response.web_items:
                    # 严格过滤：只接受来自目标媒体官方域名的新闻
                    item_url = item.url if item.url else ""
                    
                    # 检查URL是否包含目标媒体的域名
                    if site['url'] in item_url:
                        news_item = {
                            'title': item.title,
                            'url': item_url,
                            'source': site['name'],
                            'category': site['category'],
                            'snippet': item.snippet if item.snippet else ""
                        }
                        all_news.append(news_item)
            else:
                errors.append(f"{site['name']}: 未找到今日新闻")
                
        except Exception as e:
            errors.append(f"{site['name']}: {str(e)}")
            print(f"Error fetching news from {site['name']}: {str(e)}")
    
    result = {
        "news": all_news,
        "errors": errors if errors else None,
        "total_count": len(all_news),
        "date": today
    }
    
    return json.dumps(result, ensure_ascii=False, indent=2)
