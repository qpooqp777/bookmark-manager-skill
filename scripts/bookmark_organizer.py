#!/usr/bin/env python3
"""
AI Bookmark Organizer
Reads bookmarks, uses AI to categorize, and generates organized HTML.
"""

import json
import argparse
from urllib.parse import urlparse
from collections import defaultdict

# Domain to category mapping
DOMAIN_CATEGORIES = {
    # Development
    'github.com': '開發資源/GitHub',
    'stackoverflow.com': '開發資源/問答',
    'medium.com': '技術文章/Medium',
    'dev.to': '技術文章/Dev.to',
    'hashnode.com': '技術文章/Hashnode',
    
    # Apple / iOS
    'developer.apple.com': 'Apple開發/官方文件',
    'swift.org': 'Apple開發/Swift',
    'cocoapods.org': 'Apple開發/套件',
    
    # React
    'react.dev': 'React/官方',
    'reactjs.org': 'React/官方',
    'nextjs.org': 'React/Next.js',
    'redux.js.org': 'React/Redux',
    
    # JavaScript
    'javascript.info': 'JavaScript/教學',
    'nodejs.org': 'JavaScript/Node.js',
    'npmjs.com': 'JavaScript/NPM',
    
    # Learning
    'ithelp.ithome.com.tw': '學習資源/iT邦幫忙',
    'www.udemy.com': '學習資源/Udemy',
    'www.coursera.org': '學習資源/Coursera',
    'www.youtube.com': '影音學習/YouTube',
    
    # Chinese Tech
    'blog.csdn.net': '中文技術/CSDN',
    'www.cnblogs.com': '中文技術/博客園',
    'juejin.cn': '中文技術/掘金',
    'segmentfault.com': '中文技術/SegmentFault',
    'www.jianshu.com': '中文技術/簡書',
    
    # Tools
    'chat.openai.com': 'AI工具/ChatGPT',
    'claude.ai': 'AI工具/Claude',
    'codepen.io': '開發工具/CodePen',
    'jsfiddle.net': '開發工具/JSFiddle',
    
    # Cloud
    'aws.amazon.com': '雲服務/AWS',
    'cloud.google.com': '雲服務/GCP',
    'azure.microsoft.com': '雲服務/Azure',
    'vercel.com': '雲服務/Vercel',
    
    # Database
    'firebase.google.com': '後端/Firebase',
    'supabase.com': '後端/Supabase',
    'mongodb.com': '後端/MongoDB',
    
    # Design
    'dribbble.com': '設計/Dribbble',
    'figma.com': '設計/Figma',
    'uiverse.io': '設計/UI元件',
}

# Title keywords to category
KEYWORD_CATEGORIES = {
    'swift': 'Apple開發/Swift',
    'swiftui': 'Apple開發/SwiftUI',
    'ios': 'Apple開發/iOS',
    'react native': 'React/React Native',
    'react': 'React',
    'nextjs': 'React/Next.js',
    'next.js': 'React/Next.js',
    'javascript': 'JavaScript',
    'typescript': 'TypeScript',
    'node.js': 'JavaScript/Node.js',
    'nodejs': 'JavaScript/Node.js',
    'kotlin': 'Kotlin',
    'android': 'Android開發',
    'docker': 'DevOps/Docker',
    'kubernetes': 'DevOps/Kubernetes',
    'git': '開發工具/Git',
    'webpack': '開發工具/Webpack',
    'vite': '開發工具/Vite',
    'tailwind': 'CSS/Tailwind',
    'css': 'CSS',
    'html': 'HTML',
    'api': '後端/API',
    'sql': '資料庫/SQL',
    'mysql': '資料庫/MySQL',
    'postgresql': '資料庫/PostgreSQL',
    'mongodb': '資料庫/MongoDB',
    'firebase': '後端/Firebase',
    'aws': '雲服務/AWS',
    'docker': 'DevOps/Docker',
    'ci/cd': 'DevOps/CI-CD',
    'test': '測試',
    'jest': '測試/Jest',
    'security': '資安',
    'mb3': 'MB3資安',
    'shms': 'SHMS系統',
    '弘光': '弘光科大',
}


def get_category(bookmark):
    """Determine category for a bookmark using domain and title analysis."""
    url = bookmark.get('url', '')
    title = bookmark.get('title', '').lower()
    original_folder = bookmark.get('folder', '')
    
    # Parse domain
    try:
        domain = urlparse(url).netloc.lower()
        # Remove www. prefix
        if domain.startswith('www.'):
            domain = domain[4:]
    except:
        domain = ''
    
    # Check domain mapping first
    if domain in DOMAIN_CATEGORIES:
        return DOMAIN_CATEGORIES[domain]
    
    # Check for partial domain matches
    for key_domain, category in DOMAIN_CATEGORIES.items():
        if key_domain in domain or domain in key_domain:
            return category
    
    # Check title keywords
    for keyword, category in KEYWORD_CATEGORIES.items():
        if keyword in title:
            return category
    
    # Check URL keywords
    url_lower = url.lower()
    for keyword, category in KEYWORD_CATEGORIES.items():
        if keyword in url_lower:
            return category
    
    # Preserve original folder structure if it has meaningful categories
    if original_folder and original_folder != '書籤列':
        # Clean up folder name
        folder = original_folder.replace('書籤列/', '')
        if folder and folder != '':
            return folder
    
    # Default category
    return '未分類'


def organize_bookmarks(bookmarks):
    """Organize bookmarks into categories."""
    categorized = defaultdict(list)
    
    for bm in bookmarks:
        category = get_category(bm)
        categorized[category].append(bm)
    
    # Sort categories and bookmarks within each category
    organized = {}
    for category in sorted(categorized.keys()):
        organized[category] = sorted(
            categorized[category], 
            key=lambda x: x.get('title', '').lower()
        )
    
    return organized


def generate_html(organized_bookmarks, output_path):
    """Generate organized HTML bookmark file."""
    lines = [
        '<!DOCTYPE NETSCAPE-Bookmark-file-1>',
        '<!-- This is an automatically generated file. -->',
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        '<TITLE>Bookmarks - AI Organized</TITLE>',
        '<H1>Bookmarks</H1>',
        '<DL><p>',
        ''
    ]
    
    total = 0
    for category, bookmarks in organized_bookmarks.items():
        lines.append(f'    <DT><H3>{category}</H3>')
        lines.append('    <DL><p>')
        
        for bm in bookmarks:
            title = bm.get('title', 'Untitled').replace('<', '&lt;').replace('>', '&gt;')
            url = bm.get('url', '').replace('"', '&quot;')
            lines.append(f'        <DT><A HREF="{url}">{title}</A>')
            total += 1
        
        lines.append('    </DL><p>')
        lines.append('')
    
    lines.append('</DL><p>')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return total


def generate_summary(organized_bookmarks, output_path):
    """Generate a summary report."""
    lines = ['# 書籤整理報告\n']
    lines.append(f'**總書籤數:** {sum(len(bms) for bms in organized_bookmarks.values())}\n')
    lines.append(f'**分類數:** {len(organized_bookmarks)}\n')
    lines.append('## 分類統計\n')
    
    for category, bookmarks in sorted(organized_bookmarks.items(), key=lambda x: -len(x[1])):
        lines.append(f'- **{category}**: {len(bookmarks)} 個書籤')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description='AI Bookmark Organizer')
    parser.add_argument('input', help='Input JSON file from bookmark_parser.py')
    parser.add_argument('--html', default='bookmarks_organized.html', help='Output HTML file')
    parser.add_argument('--summary', default='bookmarks_summary.md', help='Output summary file')
    
    args = parser.parse_args()
    
    # Load bookmarks
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    bookmarks = data.get('bookmarks', [])
    print(f'載入 {len(bookmarks)} 個書籤...')
    
    # Organize
    print('正在 AI 分類...')
    organized = organize_bookmarks(bookmarks)
    
    # Generate HTML
    total = generate_html(organized, args.html)
    print(f'✅ 已產生 HTML: {args.html} ({total} 個書籤)')
    
    # Generate summary
    generate_summary(organized, args.summary)
    print(f'✅ 已產生報告: {args.summary}')
    
    # Print category summary
    print('\n📊 分類統計:')
    for category, bms in sorted(organized.items(), key=lambda x: -len(x[1]))[:15]:
        print(f'  {category}: {len(bms)}')


if __name__ == '__main__':
    main()
