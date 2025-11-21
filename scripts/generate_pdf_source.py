import os
import re
import yaml
import datetime
import json

# --- 配置区域 ---
FOLDERS = ['_history', '_entertainment', '_metaphysics']
OUTPUT_FILE = 'full_project.md'
CONFIG_FILE = '_config.yml'

CATEGORY_MAP = {
    '_history': '真实史料',
    '_entertainment': '文学娱乐',
    '_metaphysics': '玄学推背'
}

def parse_front_matter(content):
    """解析 Front Matter，忽略所有可能导致报错的复杂字符"""
    pattern = r'^\s*---\s*\n(.*?)\n---\s*'
    match = re.match(pattern, content, re.S)
    if match:
        fm_text = match.group(1)
        try:
            # 简单清理 tab
            fm_data = yaml.safe_load(fm_text.replace('\t', '  '))
            body = content[match.end():]
            return fm_data, body
        except:
            pass
    return None, content

def main():
    print("🚀 启动：手动构建模式 (Bypassing YAML Library)...")
    articles = []
    
    for folder in FOLDERS:
        if not os.path.exists(folder): continue
        files = [f for f in os.listdir(folder) if f.endswith('.md')]
        
        for filename in files:
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fm, body = parse_front_matter(content)
            
            if fm and 'title' in fm:
                d_event = str(fm.get('date_event') or fm.get('date') or '1900-01-01')
                articles.append({
                    'title': fm['title'],
                    'date': d_event,
                    'folder': folder,
                    'author': fm.get('author', '洪清档案整理组'),
                    'body': body
                })

    # 排序
    articles.sort(key=lambda x: x['date'])
    print(f"📊 抓取到 {len(articles)} 篇文章。")

    if not articles:
        print("❌ 错误: 未找到有效文章。")
        exit(1)

    # 获取标题
    site_title = "洪清档案"
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                c = yaml.safe_load(f)
                if c and 'title' in c: site_title = c['title']
        except: pass

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    # --- 写入合并文件 ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        # 1. 极简 YAML 头部 (绝对安全)
        out.write("---\n")
        # 使用 json.dumps 确保标题里的特殊符号被正确转义（比如双引号）
        out.write(f"title: {json.dumps(site_title, ensure_ascii=False)}\n")
        out.write(f"subtitle: \"全站文章汇编 / Full Archive\"\n")
        out.write(f"author: \"洪清档案整理组\"\n")
        out.write(f"date: \"{current_date}\"\n")
        out.write(f"geometry: \"margin=1in\"\n")
        out.write("---\n\n")
        
        # 2. 将复杂的 LaTeX 配置移出 YAML，放入 Raw Block
        # 这招能避开所有 YAML 解析错误
        out.write("```{=latex}\n")
        out.write("\\usepackage{xeCJK}\n")
        out.write("\\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}\n")
        # 如果之前的 action 指定了字体，这里可以不加，也可以加上双保险
        out.write("```\n\n")

        out.write(f"# 简介\n\n导出日期：{current_date}\n\n\\newpage\n\n")
        
        for article in articles:
            cat_name = CATEGORY_MAP.get(article['folder'], article['folder'])
            out.write(f"# {article['title']}\n\n")
            out.write(f"> **时间**: {article['date']} | **分类**: {cat_name}\n\n")
            
            # 简单的正文清理
            body = article['body']
            # 去掉 Jekyll 的 include 标签
            body = re.sub(r'\{%.*?%\}', '', body)
            # 确保正文里没有多余的 metadata block 干扰
            body = re.sub(r'^---.*?---', '', body, flags=re.DOTALL | re.MULTILINE)
            
            out.write(body)
            out.write("\n\n\\newpage\n\n")

    print(f"✅ 成功生成: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
