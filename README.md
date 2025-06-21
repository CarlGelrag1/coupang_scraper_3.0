Coupang 商品评论爬取工具

这是一个用于从韩国电商平台 Coupang 爬取商品评论的 Python 工具。该工具使用 Selenium 和 BeautifulSoup 实现网页内容抓取和解析，支持批量爬取多个商品页面的评论信息，并将结果保存为 Excel 文件。

功能特点
使用 undetected_chromedriver 绕过 Coupang 的反爬虫检测机制
支持批量爬取多个商品页面的评论
提取丰富的评论信息：用户名、评分、评论内容、图片链接、有用数等
自动处理分页评论，可自定义爬取页数
智能等待和随机滚动模拟人类操作
自动创建输出文件夹并生成唯一文件名的 Excel 文件
支持打包为单个可执行文件

主要模块

main.py

主程序入口，负责接收用户输入的商品 URL 列表，调用爬虫功能，并控制整体流程。

scraper.py

核心爬虫逻辑，实现评论数据的提取和页面导航：

extract_product_name(): 从页面中提取商品名称

extract_reviews_from_page(): 提取当前页面的所有评论数据

scrape_reviews(): 控制整个评论爬取流程，包括分页处理

browser.py

浏览器操作封装，实现不可检测的 ChromeDriver 初始化和页面交互：

create_browser(): 创建配置好的 Chrome 浏览器实例

init_browser_session(): 初始化浏览器会话

visit_product_page(): 访问指定商品页面

scroll_to_reviews_section(): 滚动到评论部分

navigate_to_page(): 导航到特定评论页面

utils.py

实用工具函数：
create_output_folder(): 创建输出文件夹

get_unique_filename(): 生成唯一的文件名

extract_product_id(): 从 URL 中提取商品 ID

save_reviews_to_excel(): 将评论数据保存到 Excel 文件

build.py

PyInstaller 打包脚本，用于将整个项目打包为单个可执行文件


版权信息
本工具仅供学习和研究使用，请勿用于非法用途。使用本工具爬取的数据请遵守 Coupang 的服务条款和相关法律法规。
