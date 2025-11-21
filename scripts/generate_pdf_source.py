import os
import re
import yaml
import datetime

# --- 配置区域 ---
# 确保这些文件夹名字和你仓库里的一模一样（区分大小写）
FOLDERS = ['_history', '_entertainment', '_metaphysics']
OUTPUT_FILE = 'full_project.md'
CONFIG_FILE = '_config.yml'
# ----------------

def parse_front_matter(content):
    """
    更强壮的解析器：
    1. 允许 --- 前后有空格
    2. 处理 Tab 缩进导致 YAML 解析失败的问题
    """
    # 匹配以 --- 开始，以 --- 结束的头部，re.S 让 . 匹配换行符
    pattern = r'^\s*---\s*\n(.*?)\n---\s*'
    match = re.match(pattern, content, re.S)
    
    if match:
        fm_text = match.group(1)
        try:
            # 替换 Tab 为 2个空格，防止 YAML 报错
            fm_data = yaml.safe_load(fm_text.replace('\t', '  '))
            # 获取 --- 之后的所有内容作为正文
            body = content[match.end():]
            return fm_data, body
        except yaml.YAMLError as e:
            print(f"⚠️ YAML 解析错误: {e}")
            return None, content
    return None, content

def main():
    print("🚀 开始执行 Python 整理脚本...")
    articles = []
    
    # 1. 遍历目录
    for folder in FOLDERS:
        if not os.path.exists(folder):
            print(f"❌ 警告: 找不到文件夹 '{folder}'，跳过。")
            continue
            
        print(f"📂 正在扫描目录: {folder} ...")
        files = [f for f in os.listdir(folder) if f.endswith('.md')]
        
        for filename in files:
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            fm, body = parse_front_matter(content)
            
            if fm and 'title' in fm:
                # 处理日期，如果为空则给一个默认老旧日期
                date_event = str(fm.get('date_event', fm.get('date', '1900-01-01')))
                
                print(f"  ✅ 抓取文章: [{date_event}] {fm['title']}")
                
                articles.append({
                    'title': fm['title'],
                    'date': date_event,
                    'category': folder,
                    'author': fm.get('author', '洪清档案整理组'),
                    'body': body,
                    'filepath': filepath
                })
            else:
                print(f"  ⚠️ 跳过文件 (无 Front Matter 或 Title): {filename}")

    # 2. 检查是否有文章
    if not articles:
        print("❌ 错误: 没有找到任何有效文章！请检查 Markdown 头部格式。")
        exit(1) # 退出并报错，让 Action 变红

    # 3. 排序
    articles.sort(key=lambda x: x['date'])
    print(f"📊 共收集到 {len(articles)} 篇文章，已按时间排序。")

    # 4. 生成合并文件
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    
    # 尝试读取 _config.yml 获取标题
    site_title = "洪清档案"
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            try:
                c = yaml.safe_load(f)
                if c and 'title' in c: site_title = c['title']
            except: pass

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        # 写入 PDF 元数据（Pandoc 使用）
        out.write(f"""---
title: "{site_title}"
subtitle: "全站文章汇编 / Full Archive"
author: "洪清档案整理组"
date: "{current_date}"
geometry: "left=2.5cm,right=2.5cm,top=2cm,bottom=2cm"
mainfont: "Noto Sans CJK SC"
sansfont: "Noto Sans CJK SC"
monofont: "Noto Sans CJK SC"
header-includes:
  - \\usepackage{{xeCJK}}
  - \\hypersetup{{colorlinks=true, linkcolor=blue}}
---\n\n""")
        
        out.write(f"# 简介\n\n生成日期：{current_date}\n\n\\newpage\n\n")
        
        for article in articles:
            out.write(f"# {article['title']}\n\n")
            out.write(f"**时间**: {article['date']} | **分类**: {article['category'].replace('_', '')}\n\n")
            out.write(article['body'])
            out.write("\n\n\\newpage\n\n")

    print(f"✅ 成功生成合并文件: {OUTPUT_FILE} (大小: {os.path.getsize(OUTPUT_FILE)} bytes)")

if __name__ == "__main__":
    main()
