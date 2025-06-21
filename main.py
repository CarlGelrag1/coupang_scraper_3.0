import time
import random
from utils import create_output_folder, extract_product_id, save_reviews_to_excel
from scraper import scrape_reviews

def main():
    print("===== Coupang 商品评论批量爬取工具 =====")
    print("请输入要爬取的商品URL列表，每行输入一个URL")
    print("输入完成后请按两次回车键 (即输入一个空行) 表示输入结束\n")

    # 收集用户输入的所有URL
    urls = []
    while True:
        user_input = input("URL (留空结束输入): ").strip()
        if not user_input:
            break
        urls.append(user_input)

    if not urls:
        print("未输入任何URL，程序退出")
        return

    print(f"\n已收集 {len(urls)} 个URL:")
    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")

    # 创建输出文件夹
    output_folder = create_output_folder()
    print(f"数据将保存在: {output_folder}")

    # 依次处理每个URL
    for i, url in enumerate(urls, 1):
        print(f"\n===== 正在处理第 {i}/{len(urls)} 个URL =====")
        print(f"目标URL: {url}")

        # 检查URL格式
        product_id = extract_product_id(url)
        if not product_id:
            print(f"URL格式错误，无法提取商品ID，跳过此URL: {url}")
            continue

        print("将自动爬取所有评论页面")

        # 爬取评论和商品名称
        all_reviews, product_name = scrape_reviews(url)

        # 将评论保存到Excel文件
        if all_reviews:
            save_reviews_to_excel(all_reviews, product_name, output_folder)
            print(f"\n成功爬取 {len(all_reviews)} 条评论！")
        else:
            print(f"\n从 {url} 未能爬取到任何评论")

        # 如果还有下一个URL，等待一段时间再继续
        if i < len(urls):
            wait_time = random.uniform(60, 80)
            print(f"\n等待 {wait_time:.1f} 秒后继续下一个URL...")
            time.sleep(wait_time)

    print("\n===== 所有URL处理完成 =====")

if __name__ == "__main__":
    main()
