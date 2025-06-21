import os
import re
import pandas as pd


def create_output_folder():
    """
    尝试创建输出文件夹，优先在C盘，其次是D盘，最后使用桌面
    """
    # 首先尝试在C盘创建文件夹
    c_drive_path = r"C:\coupang_商品评论"
    d_drive_path = r"D:\coupang_商品评论"

    try:
        # 检查C盘文件夹是否已存在，如果不存在则创建
        if not os.path.exists(c_drive_path):
            os.makedirs(c_drive_path)
            print(f"已在C盘创建文件夹: {c_drive_path}")
        else:
            print(f"C盘文件夹已存在: {c_drive_path}")
        return c_drive_path
    except Exception as e:
        print(f"在C盘创建文件夹失败: {e}")

        # 尝试在D盘创建文件夹
        try:
            if not os.path.exists(d_drive_path):
                os.makedirs(d_drive_path)
                print(f"已在D盘创建文件夹: {d_drive_path}")
            else:
                print(f"D盘文件夹已存在: {d_drive_path}")
            return d_drive_path
        except Exception as e2:
            print(f"在D盘创建文件夹也失败: {e2}")

            # 如果C盘和D盘都失败，使用临时目录
            temp_path = os.path.join(os.path.expanduser("~"), "Desktop")
            print(f"无法在C盘或D盘创建文件夹，将使用桌面: {temp_path}")
            return temp_path


def get_unique_filename(base_name, path):
    """
    检查文件名是否存在，如果存在则添加序号 (1), (2), 等
    """
    # 清理文件名，移除不允许的字符
    base_name = re.sub(r'[\\/*?:"<>|]', "", base_name)  # 移除Windows不允许的文件名字符
    base_name = base_name.strip()  # 移除首尾空格

    # 如果文件名为空或过长，使用默认名
    if not base_name or len(base_name) > 100:
        base_name = "coupang_reviews"

    filename = f"{base_name}.xlsx"
    full_path = os.path.join(path, filename)

    counter = 1
    while os.path.exists(full_path):
        filename = f"{base_name}({counter}).xlsx"
        full_path = os.path.join(path, filename)
        counter += 1

    return full_path


def extract_product_id(url):
    """
    从URL提取商品ID
    """
    match = re.search(r'/products/(\d+)', url)
    if not match:
        return None
    return match.group(1)


def save_reviews_to_excel(reviews, product_name, output_folder):
    """
    将评论数据保存到Excel文件
    """
    if not reviews:
        print("没有评论数据可保存")
        return None

    try:
        # 获取唯一的文件名
        output_path = get_unique_filename(product_name, output_folder)
        print(f"数据将保存到: {output_path}")

        # 将字典列表转换为 pandas DataFrame
        df = pd.DataFrame(reviews)
        # 定义列顺序
        fieldnames = ['页面网址', '商品价格', '评论总数', '评论总星级', '评论用户', '评论日期', '评分', '购买规格',
                      '评论内容', '评论图片', '有用数']
        df = df[fieldnames]  # 调整列顺序
        # 写入 Excel 文件，不包含索引列
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"成功保存 {len(reviews)} 条评论到 {output_path}")
        return output_path
    except Exception as e:
        print(f"保存到 Excel 文件时出错: {e}")
        return None
