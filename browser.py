import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException


def create_browser():
    """
    初始化不可检测的ChromeDriver
    """
    print("正在初始化不可检测的ChromeDriver...")
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=ko-KR")  # 设置韩语
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    # 禁用自动化控制特征
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # 创建无痕模式浏览器实例
    chrome_options.add_argument("--incognito")
    # 禁用图片加载和其他资源
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_settings.cookies": 2,
        "profile.managed_default_content_settings.javascript": 1,  # 1=允许JS，因为我们需要它来加载评论
        "profile.managed_default_content_settings.plugins": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.notifications": 2,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # 创建无痕模式浏览器实例
    #chrome_options.add_argument("--incognito")

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.136 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.20 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.52 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.10 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    ]
    # 设置用户代理和窗口大小（模拟正常用户行为）
    chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
    chrome_options.add_argument("--window-size=1920,1080")
    # 启动浏览器
    driver = uc.Chrome(options=chrome_options)
    driver.set_page_load_timeout(20)
    return driver


def init_browser_session(driver):
    """
    初始化浏览器会话，访问主页并进行随机滚动
    """
    print("正在访问Coupang主页...")
    driver.get("https://www.coupang.com/")
    time.sleep(random.uniform(18, 30))

    # 随机滚动主页
    driver.execute_script("window.scrollBy(0, window.innerHeight);")
    time.sleep(random.uniform(0.5, 2))
    driver.execute_script("window.scrollBy(0, window.innerHeight);")
    time.sleep(random.uniform(1, 2))
    driver.execute_script("window.scrollBy(0, window.innerHeight);")
    time.sleep(random.uniform(0.4, 1))
    return True


def visit_product_page(driver, url):
    """
    访问商品页面
    """
    print(f"正在访问商品页: {url}")
    driver.get(url)

    print("等待页面加载...")
    time.sleep(random.uniform(4, 7))

    # 检查页面是否成功加载
    if "error" in driver.title.lower() or "ERR_HTTP2_PROTOCOL_ERROR" in driver.page_source:
        print("页面加载失败，可能遇到了反爬机制。")
        return False

    print("页面加载成功！")

    # 随机滚动页面，模拟人类行为
    for _ in range(2):
        scroll_amount = random.uniform(0.5, 1) * driver.execute_script("return document.body.scrollHeight;")
        driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
        time.sleep(random.uniform(0.5, 1.2))

    return True


def scroll_to_reviews_section(driver):
    """
    滚动到评论部分
    """
    print("尝试找到评论部分...")
    try:
        review_text_elements = driver.find_elements(By.XPATH,
                                                    "//*[contains(text(), '상품평') or contains(text(), '리뷰') or contains(text(), 'Review') or contains(text(), 'REVIEW')]")
        if review_text_elements:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                  review_text_elements[0])
            time.sleep(random.uniform(1, 1.5))
            print("找到评论部分！")
            return True
    except Exception as e:
        print(f"找不到评论部分: {e}")
        return False


def navigate_to_page(driver, page_number, timeout=1):
    """
    导航到特定的评论页面
    """
    print(f"尝试导航到第 {page_number} 页...")
    wait = WebDriverWait(driver, timeout)
    navigated_by_page_button = False

    # 1. 尝试定位并点击精确的页码按钮
    try:
        page_button_selector = f'button[data-page="{page_number}"]'
        # 等待按钮出现并可见
        page_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, page_button_selector)))
        print(f"找到可见的页码按钮 {page_number}，尝试点击...")
        # 滚动到视图并等待可点击
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", page_button)
        time.sleep(random.uniform(0.5, 0.8))  # 短暂暂停让滚动生效
        # 再次等待确保按钮可点击
        clickable_page_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, page_button_selector)))
        clickable_page_button.click()
        print(f"已点击页码按钮: {page_number}")
        time.sleep(random.uniform(0.8, 1))  # 等待页面加载
        navigated_by_page_button = True
        return True  # 成功通过页码按钮导航
    except TimeoutException:
        print(f"页码按钮 {page_number} 在 {timeout} 秒内未找到或不可见，尝试回退到第 {page_number - 9} 页并点击下一页。")
    except ElementClickInterceptedException:
        print(f"页码按钮 {page_number} 被遮挡，尝试回退到第 {page_number - 9} 页并点击下一页。")
    except Exception as e:
        print(f"查找或点击页码 {page_number} 时出错: {e}，尝试回退到第 {page_number - 9} 页并点击下一页。")

    # 2. 如果无法直接导航到目标页，尝试回退到第 (page_number - 10) 页
    if not navigated_by_page_button:
        fallback_page = page_number - 10
        if fallback_page >= 1:  # 确保回退页码有效
            print(f"尝试导航到回退页码: 第 {fallback_page} 页...")
            try:
                fallback_button_selector = f'button[data-page="{fallback_page}"]'
                # 等待回退页码按钮出现并可见
                fallback_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, fallback_button_selector)))
                print(f"找到可见的回退页码按钮 {fallback_page}，尝试点击...")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", fallback_button)
                time.sleep(random.uniform(0.4, 0.7))
                clickable_fallback_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, fallback_button_selector)))
                clickable_fallback_button.click()
                print(f"已点击回退页码按钮: {fallback_page}")
                time.sleep(random.uniform(0.5, 1))  # 等待页面加载

                # 3. 点击“下一页”按钮
                try:
                    next_button_selector = "button.sdp-review__article__page__next.sdp-review__article__page__next--active"
                    next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector)))
                    print("找到可点击的“下一页”按钮，尝试点击...")
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
                    time.sleep(random.uniform(0.5, 1.5))
                    next_button_clickable = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector)))
                    next_button_clickable.click()
                    print(f"已点击“下一页”按钮 (目标页码 {page_number})")
                    time.sleep(random.uniform(0.5, 1))  # 等待页面加载
                    return True  # 成功通过回退页码+下一页导航
                except TimeoutException:
                    print(f"“下一页”按钮 在 {timeout} 秒内未找到或不可点击。可能已到达最后一页。")
                    return False
                except NoSuchElementException:
                    print("无法找到“下一页”按钮元素。已到达最后一页。")
                    return False
                except ElementClickInterceptedException:
                    print("“下一页”按钮被遮挡，无法点击。")
                    return False
                except Exception as e:
                    print(f"点击“下一页”按钮时出错: {e}")
                    return False
            except TimeoutException:
                print(f"回退页码按钮 {fallback_page} 在 {timeout} 秒内未找到或不可见。")
                return False
            except ElementClickInterceptedException:
                print(f"回退页码按钮 {fallback_page} 被遮挡。")
                return False
            except Exception as e:
                print(f"查找或点击回退页码 {fallback_page} 时出错: {e}")
                return False
        else:
            print(f"回退页码 {fallback_page} 无效（小于1），无法继续导航。")
            return False

    return False  # 如果所有方法都失败
