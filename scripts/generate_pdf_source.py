import os
import re
import yaml
import datetime

# 配置
FOLDERS = ['_history', '_entertainment', '_metaphysics']
OUTPUT_FILE = 'full_project.md'
CONFIG_FILE = '_config.yml'

# 映射文件夹名为中文章节名
CATEGORY_MAP = {
    '_history': '真实史料',
    '_entertainment': '文学娱乐',
    '_metaphysics': '玄学推背'
}

def parse_front_matter(content):
    """解析 Jekyll 的 Front Matter"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        try:
            # 替换 tabs，防止 yaml 解析错误
            fm_data = yaml.safe_load(fm_text.replace('\t', '  '))
            body = content[match.end():]
            return fm_data, body
        except yaml.YAMLError as e:
            print(f"YAML Error: {e}")
    return {}, content

def get_site_config():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except:
        return {"title": "洪清档案", "url": ""}

def main():
    articles = []
    
    # 1. 遍历文件夹抓取文章
    for folder in FOLDERS:
        if not os.path.exists(folder):
            continue
        
        for filename in os.listdir(folder):
            if filename.endswith('.md'):
                filepath = os.path.join(folder, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    fm, body = parse_front_matter(content)
                    
                    # 必须有 title 和 date_event 才处理
                    if 'title' in fm:
                        # 确保 date_event 是字符串以便排序 (YYYY-MM-DD)
                        date_event = str(fm.get('date_event', '9999-12-31'))
                        
                        articles.append({
                            'title': fm['title'],
                            'date': date_event,
                            'category': folder,
                            'author': fm.get('author', '洪清档案整理组'),
                            'body': body,
                            'filepath': filepath
                        })

    # 2. 按 date_event 时间排序
    articles.sort(key=lambda x: x['date'])

    # 3. 获取网站配置
    config = get_site_config()

    # 4. 写入合并后的 Markdown 文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        # --- 封面部分 ---
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        out.write(f"""---
title: "{config.get('title', 'The Dream of Hong')}"
subtitle: "全站文章汇编 / Full Archive"
author: "洪清档案整理组"
date: "{current_date}"
header-includes:
  - \\usepackage{{xeCJK}}
  - \\setCJKmainfont{{Noto Sans CJK SC}}
  - \\hypersetup{{colorlinks=true, linkcolor=blue, urlcolor=blue}}
---\n\n""")
        
        out.write("# 简介\n\n")
        out.write(f"本文档由 GitHub Actions 自动生成于 {current_date}。\n")
        out.write(f"包含真实史料、文学娱乐及玄学推背所有文章，按历史时间轴排序。\n\n")
        out.write(f"在线访问: {config.get('url', '')}{config.get('baseurl', '')}\n\n")
        out.write("\\newpage\n\n") # LaTeX 分页符

        # --- 目录由 Pandoc 自动生成 (通过 --toc 参数)，这里不需要手写 ---

        # --- 正文内容 ---
        for article in articles:
            # 插入新的一页
            out.write("\\newpage\n\n")
            
            # 标题和元数据
            cat_name = CATEGORY_MAP.get(article['category'], '其他')
            out.write(f"# {article['title']}\n\n")
            out.write(f"> **时间**: {article['date']} | **分类**: {cat_name} | **作者**: {article['author']}\n\n")
            
            # 修正图片链接（防止某些相对路径漏网，虽然你说都是绝对路径，加个保险）
            # 如果你确定全是 http 开头，这段可以忽略，但在 Pandoc 中通常不需要特殊处理绝对路径
            
            out.write(article['body'])
            out.write("\n\n")

    print(f"Successfully merged {len(articles)} articles into {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
