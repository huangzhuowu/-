import os
import re
import yaml
import datetime

# --- 配置区域 ---
FOLDERS = ['_history', '_entertainment', '_metaphysics']
OUTPUT_FILE = 'full_project.md'
CONFIG_FILE = '_config.yml'

# 映射文件夹名为中文分类名
CATEGORY_MAP = {
    '_history': '真实史料',
    '_entertainment': '文学娱乐',
    '_metaphysics': '玄学推背'
}

def parse_front_matter(content):
    """解析 Front Matter，容错性更强"""
    pattern = r'^\s*---\s*\n(.*?)\n---\s*'
    match = re.match(pattern, content, re.S)
    
    if match:
        fm_text = match.group(1)
        try:
            fm_data = yaml.safe_load(fm_text.replace('\t', '  '))
            body = content[match.end():]
            return fm_data, body
        except Exception:
            return None, content
    return None, content

def main():
    print("🚀 开始执行 Python 整理脚本 (YAML修复版)...")
    articles = []
    
    # 1. 抓取文章
    for folder in FOLDERS:
        if not os.path.exists(folder): continue
            
        for filename in os.listdir(folder):
            if filename.endswith('.md'):
                filepath = os.path.join(folder, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                fm, body = parse_front_matter(content)
                
                if fm and 'title' in fm:
                    # 这里的 get 需要处理可能的 None
                    d_event = fm.get('date_event') or fm.get('date') or '1900-01-01'
                    date_event = str(d_event)
                    
                    articles.append({
                        'title': fm['title'],
                        'date': date_event,
                        'folder': folder,
                        'author': fm.get('author', '洪清档案整理组'),
                        'body': body
                    })

    # 2. 排序
    articles.sort(key=lambda x: x['date'])
    print(f"📊 共收集到 {len(articles)} 篇文章。")

    if not articles:
        print("❌ 错误: 没有找到文章，终止。")
        exit(1)

    # 3. 获取网站标题
    site_title = "洪清档案"
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            try:
                c = yaml.safe_load(f)
                if c and 'title' in c: site_title = c['title']
            except: pass

    # 4. 构建标准的 YAML 头部字典 (避免手写出错)
    header_data = {
        'title': site_title,
        'subtitle': '全站文章汇编 / Full Archive',
        'author': '洪清档案整理组',
        'date': datetime.date.today().strftime('%Y-%m-%d'),
        'geometry': 'margin=1in',
        'mainfont': 'Noto Sans CJK SC',
        'sansfont': 'Noto Sans CJK SC',
        'monofont': 'Noto Sans CJK SC',
        # 使用 list 格式，yaml.dump 会自动处理缩进和转义
        'header-includes': [
            '\\usepackage{xeCJK}',
            '\\hypersetup{colorlinks=true, linkcolor=blue}'
        ]
    }

    # 5. 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        out.write("---\n")
        # allow_unicode=True 保证中文不被转义为 \uXXXX
        yaml.dump(header_data, out, allow_unicode=True, default_flow_style=False)
        out.write("---\n\n")
        
        out.write("# 简介\n\n本文档由 GitHub Actions 自动生成。\n\n\\newpage\n\n")
        
        for article in articles:
            cat_name = CATEGORY_MAP.get(article['folder'], article['folder'])
            
            out.write(f"# {article['title']}\n\n")
            out.write(f"> **时间**: {article['date']} | **分类**: {cat_name} | **作者**: {article['author']}\n\n")
            
            # 简单的清理：移除 Jekyll 的 include 标签，防止 pandoc 报错
            clean_body = re.sub(r'\{%.*?%\}', '', article['body'])
            out.write(clean_body)
            out.write("\n\n\\newpage\n\n")

    print(f"✅ 成功生成: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
