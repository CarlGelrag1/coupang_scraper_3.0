import subprocess

# 定义要执行的命令
command = [
    "pyinstaller",
    "--onefile",
    "--add-data", "chromedriver.exe;.",
    "--hidden-import", "pandas",
    "--hidden-import", "openpyxl",
    "--hidden-import", "pandas._libs.tslibs.base",
    "--hidden-import", "pandas._libs.tslibs.timedeltas",
    "--hidden-import", "openpyxl.cell",
    "--hidden-import", "openpyxl.workbook",
    "--icon", "coupang.ico",
    "main.py"
]

# 执行命令
try:
    subprocess.run(command, check=True)
    print("打包完成！")
except subprocess.CalledProcessError as e:
    print(f"打包失败：{e}")
