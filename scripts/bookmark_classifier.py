#!/usr/bin/env python3
"""
AI Bookmark Classifier
Intelligently categorizes bookmarks based on title and URL patterns.
"""

import json
import re
from urllib.parse import urlparse
from collections import defaultdict


# 分類規則定義
CATEGORY_RULES = {
    # 前端框架
    'Frontend/React': [
        r'react', r'reactjs', r'react\.js', r'react-native', r'react native', r'react router', 
        r'redux', r'next\.?js', r'gatsby', r'create-react-app', r'jsx', r'hook',
        r'react hooks', r'useeffect', r'usestate', r'context api'
    ],
    'Frontend/Vue': [
        r'vue', r'vuejs', r'vue\.js', r'vuex', r'vue router', r'vue-cli', r'nuxt',
        r'composition api', r'pinia', r'vee-validate'
    ],
    'Frontend/Angular': [
        r'angular', r'angularjs', r'ng-', r'rxjs angular', r'angular cli'
    ],
    'Frontend/General': [
        r'javascript', r'js', r'frontend', r'front-end', r'html', r'css', 
        r'typescript', r'ts', r'webpack', r'babel', r'vite', r'rollup',
        r'npm', r'yarn', r'pnpm', r'eslint', r'prettier', r'postcss',
        r'tailwind', r'bootstrap', r'sass', r'less', r'styled-components'
    ],
    
    # 後端
    'Backend/Node.js': [
        r'node\.?js', r'express', r'koa', r'nestjs', r'fastify', r'eggjs',
        r'npm package', r'node module'
    ],
    'Backend/Python': [
        r'python', r'django', r'flask', r'fastapi', r'pytorch', r'tensorflow',
        r'pandas', r'numpy', r'scikit', r'jupyter'
    ],
    'Backend/Java': [
        r'java', r'spring', r'springboot', r'spring boot', r'hibernate',
        r'maven', r'gradle', r'kotlin backend', r'ktor'
    ],
    'Backend/Go': [
        r'golang', r'go\s+lang', r'gin', r'echo', r'beego', r'fiber'
    ],
    'Backend/Database': [
        r'mysql', r'postgresql', r'mongodb', r'redis', r'elasticsearch',
        r'database', r'sql', r'nosql', r'orm', r'prisma', r'sequelize'
    ],
    'Backend/API': [
        r'rest api', r'graphql', r'api design', r'openapi', r'swagger',
        r'postman', r'json api', r'webhook'
    ],
    
    # 移動開發
    'Mobile/iOS-Swift': [
        r'swift', r'swiftui', r'ios', r'xcode', r'uikit', r'coredata',
        r'combine', r'rxswift', r'alamofire', r'cocoapods', r'swift package',
        r'app store', r'testflight', r'apple developer'
    ],
    'Mobile/Android': [
        r'android', r'kotlin', r'java android', r'jetpack compose', r'gradle android',
        r'android studio', r'firebase android'
    ],
    'Mobile/React Native': [
        r'react native', r'expo', r'rn ', r'react-native'
    ],
    'Mobile/Flutter': [
        r'flutter', r'dart'
    ],
    
    # DevOps & 工具
    'DevOps/Docker': [
        r'docker', r'container', r'kubernetes', r'k8s', r'helm', r'dockerfile',
        r'docker compose', r'containerization'
    ],
    'DevOps/CI-CD': [
        r'github action', r'ci/cd', r'gitlab ci', r'jenkins', r'travis',
        r'circleci', r'deployment', r'automation'
    ],
    'DevOps/Cloud': [
        r'aws', r'amazon web', r'azure', r'gcp', r'google cloud', r'cloudflare',
        r'vercel', r'netlify', r'heroku', r'linode', r'digitalocean'
    ],
    'DevOps/Git': [
        r'git', r'github', r'gitlab', r'version control', r'git flow',
        r'git commit', r'pull request', r'merge conflict'
    ],
    
    # AI & ML
    'AI-ML/General': [
        r'machine learning', r'artificial intelligence', r'deep learning',
        r'neural network', r'llm', r'large language model', r'openai',
        r'chatgpt', r'gpt', r'claude', r'ai ', r' ml ', r'machinelearning'
    ],
    'AI-ML/Models': [
        r'transformer', r'bert', r'gpt-3', r'gpt-4', r'llama', r'stable diffusion',
        r'huggingface', r'hugging face', r'pytorch', r'tensorflow'
    ],
    
    # 開發工具
    'Tools/IDE': [
        r'vscode', r'visual studio code', r'jetbrains', r'webstorm', r'pycharm',
        r'intellij', r'sublime', r'atom', r'vim', r'neovim'
    ],
    'Tools/Design': [
        r'figma', r'sketch', r'adobe xd', r'ui design', r'ux design',
        r'prototyping', r'wireframe', r'mockup'
    ],
    
    # 學習資源
    'Learning/Tutorials': [
        r'tutorial', r'教學', r'入門', r'guide', r'getting started',
        r'learn ', r'course', r'lesson', r'crash course'
    ],
    'Learning/Documentation': [
        r'documentation', r'docs', r'reference', r'api doc', r'official doc'
    ],
    
    # 社群 & 論壇
    'Community/Forums': [
        r'stackoverflow', r'stack overflow', r'reddit', r'dev\.to',
        r'medium', r'csdn', r'博客園', r'簡書', r'掘金', r'ithome',
        r'it邦幫忙', r'v2ex', r'github issue', r'discussion'
    ],
    
    # 資安
    'Security': [
        r'security', r'資安', r'cybersecurity', r'encryption', r'oauth',
        r'jwt', r'authentication', r'authorization', r'vulnerability',
        r'penetration test', r'駭客', r'加密', r'防火牆'
    ],
    
    # 其他
    'Other/Video': [
        r'youtube', r'vimeo', r'bilibili', r'video', r'watch'
    ],
    'Other/Social': [
        r'twitter', r'x\.com', r'linkedin', r'facebook', r'instagram'
    ],
    
    # 圖書館 & 學術
    'Library/Systems': [
        r'圖書', r'library', r'opac', r'mitopac', r'webopac', r'編目',
        r'bookhouse', r'weblink', r'採訪', r'推薦', r'借閱', r'catalog'
    ],
    
    # 中文技術社群
    'Community/Chinese-Tech': [
        r'簡書', r'jianshu', r'掘金', r'juejin', r'csdn', r'博客園',
        r'ithome', r'it邦幫忙', r'it幫幫忙', r'鐵人賽', r'彼得潘',
        r'程式人', r'軟體', r'開發', r'技術'
    ],
    
    # 設計模式 & 架構
    'Architecture/Patterns': [
        r'mvvm', r'mvc', r'mvp', r'設計模式', r'design pattern',
        r'architecture', r'架構', r'重構', r'refactor', r'clean code',
        r'solid', r'依賴注入', r'dependency injection'
    ],
    
    # 測試
    'Testing': [
        r'unit test', r'integration test', r'e2e', r'jest', r'vitest',
        r'cypress', r'playwright', r'selenium', r'tdd', r'測試',
        r'自動化測試', r'qa', r'quality assurance'
    ],
    
    # 實用工具
    'Tools/Utilities': [
        r'json', r'converter', r'formatter', r'beautifier', r'minifier',
        r'generator', r'online tool', r'倒數', r'timer', r'計時器',
        r'calculator', r'轉換', r'工具'
    ],
}


def classify_bookmark(title: str, url: str) -> str:
    """根據標題和 URL 分類書籤。"""
    text = f"{title} {url}".lower()
    
    scores = defaultdict(int)
    
    for category, patterns in CATEGORY_RULES.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                scores[category] += 1
    
    if scores:
        # 返回得分最高的分類
        return max(scores.items(), key=lambda x: x[1])[0]
    
    # 預設分類：根據域名
    domain = urlparse(url).netloc.lower()
    
    if 'github.com' in domain:
        return 'Development/GitHub'
    elif 'stackoverflow.com' in domain:
        return 'Community/StackOverflow'
    elif 'medium.com' in domain:
        return 'Community/Medium'
    elif 'youtube.com' in domain:
        return 'Other/Video'
    elif any(x in domain for x in ['apple.com', 'developer.apple.com']):
        return 'Mobile/iOS-Swift'
    elif 'google.com' in domain:
        return 'Tools/Google'
    elif 'jianshu.com' in domain:
        return 'Community/Chinese-Tech'
    elif 'juejin.cn' in domain:
        return 'Community/Chinese-Tech'
    elif 'csdn.net' in domain:
        return 'Community/Chinese-Tech'
    elif 'ithome.com.tw' in domain:
        return 'Community/Chinese-Tech'
    elif 'ithelp.ithome.com.tw' in domain:
        return 'Community/Chinese-Tech'
    elif 'tpisoftware.com' in domain:
        return 'Community/Chinese-Tech'
    elif 'localhost' in domain:
        return 'Development/Localhost'
    elif 'chrome-extension' in url or 'chrome://' in url:
        return 'Browser/Extensions'
    elif re.search(r'\d+\.\d+\.\d+\.\d+', domain):
        return 'Network/Internal-IP'
    
    return 'Uncategorized'


def organize_bookmarks(bookmarks: list) -> dict:
    """重新組織書籤。"""
    organized = defaultdict(list)
    
    for bm in bookmarks:
        category = classify_bookmark(
            bm.get('title', ''),
            bm.get('url', '')
        )
        
        # 保留原始資訊，更新分類
        new_bm = bm.copy()
        new_bm['new_folder'] = category
        new_bm['original_folder'] = bm.get('folder', '')
        organized[category].append(new_bm)
    
    return dict(organized)


def generate_html(organized: dict, output_path: str):
    """生成重新分類後的 HTML 書籤檔案。"""
    lines = [
        '<!DOCTYPE NETSCAPE-Bookmark-file-1>',
        '<!-- This is an automatically generated file. -->',
        f'<!-- Generated: {__import__("datetime").datetime.now().isoformat()} -->',
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        '<TITLE>Bookmarks - AI Organized</TITLE>',
        '<H1>Bookmarks</H1>',
        '<DL><p>',
        ''
    ]
    
    # 按分類排序
    for category in sorted(organized.keys()):
        bookmarks = organized[category]
        
        lines.append(f'    <DT><H3>{category}</H3>')
        lines.append('    <DL><p>')
        
        # 按標題排序書籤
        for bm in sorted(bookmarks, key=lambda x: x.get('title', '').lower()):
            title = bm.get('title', 'Untitled')
            url = bm.get('url', '')
            # HTML escape
            title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            url = url.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            lines.append(f'        <DT><A HREF="{url}">{title}</A>')
        
        lines.append('    </DL><p>')
        lines.append('')
    
    lines.append('</DL><p>')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def generate_report(organized: dict) -> str:
    """生成分類報告。"""
    report = []
    report.append("=" * 60)
    report.append("書籤 AI 分類報告")
    report.append("=" * 60)
    report.append("")
    
    total = sum(len(bms) for bms in organized.values())
    report.append(f"總書籤數: {total}")
    report.append(f"分類數: {len(organized)}")
    report.append("")
    
    # 按書籤數量排序
    sorted_categories = sorted(
        organized.items(),
        key=lambda x: -len(x[1])
    )
    
    for category, bookmarks in sorted_categories:
        report.append(f"📁 {category}: {len(bookmarks)} 個書籤")
    
    report.append("")
    report.append("=" * 60)
    
    return '\n'.join(report)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Bookmark Classifier')
    parser.add_argument('input', help='Input JSON file')
    parser.add_argument('--output-html', default='bookmarks_organized.html', help='Output HTML file')
    parser.add_argument('--output-json', help='Output JSON file')
    parser.add_argument('--report', action='store_true', help='Show classification report')
    
    args = parser.parse_args()
    
    # 載入書籤
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    bookmarks = data.get('bookmarks', [])
    
    # 分類
    organized = organize_bookmarks(bookmarks)
    
    # 生成報告
    if args.report:
        print(generate_report(organized))
    
    # 輸出 HTML
    generate_html(organized, args.output_html)
    print(f"\n✅ HTML 已匯出: {args.output_html}")
    
    # 輸出 JSON（可選）
    if args.output_json:
        with open(args.output_json, 'w', encoding='utf-8') as f:
            json.dump({
                'organized': organized,
                'stats': {
                    'total': len(bookmarks),
                    'categories': len(organized)
                }
            }, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 已匯出: {args.output_json}")


if __name__ == '__main__':
    main()
