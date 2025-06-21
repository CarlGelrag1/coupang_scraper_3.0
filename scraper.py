import time
import random
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser import create_browser, init_browser_session, visit_product_page, scroll_to_reviews_section, \
    navigate_to_page


def extract_product_name(driver):
    """
    从页面提取商品名称
    """
    try:
        # 尝试通过 CSS 选择器获取商品名称
        product_name_elem = driver.find_element(
            By.CSS_SELECTOR,
            "h1.product-title span.twc-font-bold"
        )
        product_name = product_name_elem.text.strip()
        print(f"找到商品名称: {product_name}")
        return product_name
    except Exception as e:
        print(f"提取商品名称时出错: {e}")

    return "coupang_reviews"  # 默认文件名



def extract_reviews_from_page(driver, url):
    """
    从当前页面提取评论数据
    """
    reviews = []
    total_reviews = "-"
    total_star = "-"
    product_price = "-"

    try:
        # 获取页面源码
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # 获取评论总数
        try:
            total_reviews_elem = soup.select_one("div.review-average-header div.review-average-header-total-count")
            if total_reviews_elem:
                total_reviews = total_reviews_elem.text.strip()
                print(f"找到评论总数: {total_reviews}")
            else:
                total_reviews = "-"
        except Exception as e:
            print(f"获取评论总数时出错: {e}")
            total_reviews = "-"

        # 尝试获取价格
        try:
            product_price_elem = soup.select_one("div.price-container div.final-price-amount")
            if product_price_elem:
                product_price = product_price_elem.text.strip()
                print(f"找到商品价格: {product_price}")
            else:
                print("未找到价格元素")
        except Exception as e:
            print(f"获取价格时出错: {e}")
            product_price = "-"

        # 获取评论总星级
        try:
            rating_inner_elem = soup.select_one("span.review-rating-inner")
            if rating_inner_elem and 'style' in rating_inner_elem.attrs:
                style_attr = rating_inner_elem['style']
                # 提取 width: 90%
                width_str = style_attr.split("width:")[1].split(";")[0].strip()
                percent = float(width_str.strip("%")) / 100
                total_star = round(percent * 5, 1)  # 90% -> 4.5
                print(f"找到评论总星级: {total_star}")
            else:
                print("未找到评分元素或缺少 style 属性")
                total_star = "-"
        except Exception as e:
            print(f"获取评论总星级时出错: {e}")
            total_star = "-"

        # 找到所有评论文章
        articles = soup.select("article.sdp-review__article__list")
        print(f"找到 {len(articles)} 条评论")

        # 如果没有找到评论，尝试其他选择器
        if len(articles) == 0:
            print("使用备用选择器查找评论...")
            articles = soup.select(".review-item, .prod-review-item, .review-article")
            print(f"备用选择器找到 {len(articles)} 条评论")

        # 处理每条评论
        for article in articles:
            # 评论用户
            user_name_elem = article.select_one("span.sdp-review__article__list__info__user__name")
            user_name = user_name_elem.text.strip() if user_name_elem else "-"

            # 评论日期
            review_date_elem = article.select_one("div.sdp-review__article__list__info__product-info__reg-date")
            review_date = review_date_elem.text.strip() if review_date_elem else "-"

            # 评分
            rating_elem = article.select_one("div.sdp-review__article__list__info__product-info__star-orange")
            rating = int(rating_elem.attrs["data-rating"]) if rating_elem and "data-rating" in rating_elem.attrs else 0

            # 购买规格
            product_size = article.select_one("div.sdp-review__article__list__info__product-info__name")
            size = product_size.text.strip() if product_size else "-"

            # 评论内容
            review_content_elem = article.select_one("div.sdp-review__article__list__review > div")
            review_content = review_content_elem.text.strip() if review_content_elem else "-"

            # 获取有用数量
            helpful_elem = article.select_one("div.sdp-review__article__list__help__count > strong")
            helpful_count = helpful_elem.text.strip() if helpful_elem else "0"

            # 获取评论图片链接
            image_elems = article.select("div.sdp-review__article__list__attachment__list img")
            if image_elems:
                # 将所有图片链接用分号连接成一个字符串
                image_links = ";".join([img.get("src", "") for img in image_elems if img.get("src")])
            else:
                image_links = "-"

            reviews.append({
                '页面网址': url,
                '评论总数': total_reviews,
                '商品价格': product_price,
                '评论总星级': total_star,
                '评论用户': user_name,
                '评论日期': review_date,
                '评分': rating,
                '购买规格': size,
                '评论内容': review_content,
                '评论图片': image_links,
                '有用数': helpful_count,
            })

        return reviews, total_reviews, total_star, product_price
    except Exception as e:
        print(f"提取评论数据时出错: {e}")
        return [], total_reviews, total_star, product_price


def scrape_reviews(url, page_to_crawl=9999):
    """
    爬取指定URL的所有评论
    """
    reviews = []
    driver = None
    total_reviews = "-"  # 默认评论总数值
    product_name = "coupang_reviews"  # 默认商品名

    try:
        # 初始化浏览器
        driver = create_browser()
        # 访问主页并初始化会话
        init_browser_session(driver)
        # 访问商品页面
        if not visit_product_page(driver, url):
            return reviews, product_name

        # 提取商品名称
        product_name = extract_product_name(driver)

        # 滚动到评论部分
        scroll_to_reviews_section(driver)

        # 爬取第1页
        print(f"\n===== 正在爬取第 1 页评论 =====")
        time.sleep(random.uniform(1, 1.5))
        page_reviews, total_reviews, total_star, product_price = extract_reviews_from_page(driver, url)
        reviews.extend(page_reviews)
        print(f"从第 1 页获取到 {len(page_reviews)} 条评论")

        # 爬取第2页到第page_to_crawl页
        for current_page in range(2, page_to_crawl + 1):
            if not navigate_to_page(driver, current_page):
                print(f"无法导航到第 {current_page} 页，结束爬取")
                break

            # 等待评论加载
            try:
                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "article.sdp-review__article__list"))
                )
                time.sleep(random.uniform(1, 1.5))
            except Exception as e:
                print(f"等待评论加载超时: {e}")
                break

            print(f"\n===== 正在爬取第 {current_page} 页评论 =====")
            page_reviews, page_total_reviews, page_total_star, product_price = extract_reviews_from_page(driver, url)
            # 如果第一页没有获取到评论总数，但这一页获取到了，就更新总数
            if total_reviews == "-" and page_total_reviews != "-":
                total_reviews = page_total_reviews
            reviews.extend(page_reviews)
            print(f"从第 {current_page} 页获取到 {len(page_reviews)} 条评论")

            # 页面之间添加随机等待
            wait_time = random.uniform(1, 2)
            print(f"等待 {wait_time:.1f} 秒后继续...")
            time.sleep(wait_time)

        return reviews, product_name

    except Exception as e:
        print(f"爬取过程中出错: {e}")
        return reviews, product_name
    finally:
        if driver:
            driver.quit()
            print("浏览器已关闭")
