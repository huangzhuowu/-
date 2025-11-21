import os
import re
import yaml
import datetime

# --- 配置 ---
FOLDERS = ['_history', '_entertainment', '_metaphysics']
CONTENT_FILE = 'content.md'
METADATA_FILE = 'metadata.yaml'
CONFIG_FILE = '_config.yml'

CATEGORY_MAP = {
    '_history': '真实史料',
    '_entertainment': '文学娱乐',
    '_metaphysics': '玄学推背'
}

def parse_front_matter(content):
    """
    强力去除 Front Matter
    """
    # 1. 尝试标准正则
    pattern = r'^\s*---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.S)
    if match:
        try:
            fm = yaml.safe_load(match.group(1))
            body = content[match.end():]
            return fm, body
        except:
            pass
            
    # 2. 如果正则失败，尝试暴力查找第二个 ---
    if content.strip().startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # parts[0] 是空的, parts[1] 是头部, parts[2] 是正文
            try:
                fm = yaml.safe_load(parts[1])
                return fm, parts[2]
            except:
                pass
                
    # 3. 失败，返回空头部，但保留内容（需小心，这可能导致残留）
    return None, content

def main():
    print("🚀 启动：分离生成模式...")
    articles = []
    
    # --- 1. 扫描文章 ---
    for folder in FOLDERS:
        if not os.path.exists(folder): continue
        
        for filename in os.listdir(folder):
            if filename.endswith('.md'):
                filepath = os.path.join(folder, filename)
                # 使用 utf-8-sig 自动处理 BOM
                with open(filepath, 'r', encoding='utf-8-sig') as f:
                    content = f.read()
                
                fm, body = parse_front_matter(content)
                
                if fm and 'title' in fm:
                    d_event = str(fm.get('date_event') or fm.get('date') or '1999-01-01')
                    articles.append({
                        'title': fm['title'],
                        'date': d_event,
                        'folder': folder,
                        'author': fm.get('author', '洪清档案整理组'),
                        'body': body.strip() # 去除首尾空格
                    })

    articles.sort(key=lambda x: x['date'])
    print(f"📊 抓取到 {len(articles)} 篇文章。")

    if not articles:
        print("❌ 错误: 未找到有效文章。")
        exit(1)

    # --- 2. 生成 metadata.yaml (封面配置) ---
    site_title = "洪清档案"
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                c = yaml.safe_load(f)
                if c and 'title' in c: site_title = c['title']
        except: pass

    metadata = {
        'title': site_title,
        'subtitle': '全站文章汇编 / Full Archive',
        'author': '洪清档案整理组',
        'date': datetime.date.today().strftime('%Y-%m-%d'),
        'geometry': 'margin=1in',
        'mainfont': 'Noto Sans CJK SC',
        'sansfont': 'Noto Sans CJK SC', # 避免找不到字体
        'header-includes': [
            '\\usepackage{xeCJK}',
            '\\hypersetup{colorlinks=true, linkcolor=blue}'
        ]
    }

    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, allow_unicode=True, default_flow_style=False)
    print(f"✅ 生成封面配置: {METADATA_FILE}")

    # --- 3. 生成 content.md (纯净正文) ---
    with open(CONTENT_FILE, 'w', encoding='utf-8') as out:
        # 不写 YAML 头部！直接开始写内容
        out.write(f"# 简介\n\n导出时间：{metadata['date']}\n\n\\newpage\n\n")
        
        for article in articles:
            cat_name = CATEGORY_MAP.get(article['folder'], article['folder'])
            out.write(f"# {article['title']}\n\n")
            out.write(f"> **时间**: {article['date']} | **分类**: {cat_name}\n\n")
            
            # 清理 Jekyll 标签
            body = re.sub(r'\{%.*?%\}', '', article['body'])
            # 再次确保没有残留的 YAML ---
            if body.strip().startswith('---'):
                 # 如果正文开头还有 ---，说明没切干净，强制去掉前几行
                 body = re.sub(r'^---.*?---\s*', '', body, flags=re.DOTALL)
            
            out.write(body)
            out.write("\n\n\\newpage\n\n")
            
    print(f"✅ 生成正文内容: {CONTENT_FILE}")

if __name__ == "__main__":
    main()
