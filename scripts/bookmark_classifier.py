#!/usr/bin/env python3
"""
AI Bookmark Classifier
Uses pattern matching and ML-like heuristics to intelligently categorize bookmarks
based on actual user bookmark patterns.
"""

import json
import re
from urllib.parse import urlparse
from collections import defaultdict
from typing import Dict, List, Tuple


class BookmarkClassifier:
    """Intelligent bookmark classifier based on user patterns."""
    
    def __init__(self):
        # User's actual technology stack (from bookmark analysis)
        self.tech_stack = {
            'frontend': ['react', 'nextjs', 'next.js', 'vue', 'angular', 'svelte', 'html', 'css', 'tailwind'],
            'mobile': ['swift', 'ios', 'android', 'kotlin', 'react native', 'rn', 'flutter', 'xamarin'],
            'backend': ['nodejs', 'node.js', 'python', 'java', 'c#', 'go', 'rust', 'api', 'rest', 'graphql'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'firebase', 'supabase', 'redis', 'elasticsearch'],
            'devops': ['docker', 'kubernetes', 'ci/cd', 'jenkins', 'github actions', 'gitlab', 'aws', 'gcp', 'azure'],
            'security': ['security', '資安', 'mb3', 'encryption', 'auth', 'oauth', 'jwt', 'ssl', 'tls'],
            'testing': ['test', 'jest', 'pytest', 'mocha', 'cypress', 'selenium', 'unit test', 'e2e'],
            'tools': ['git', 'webpack', 'vite', 'npm', 'yarn', 'pnpm', 'eslint', 'prettier', 'typescript'],
        }
        
        # Domain to category mapping (comprehensive)
        self.domain_categories = {
            # Development Platforms
            'github.com': '開發資源/GitHub',
            'gitlab.com': '開發資源/GitLab',
            'bitbucket.org': '開發資源/Bitbucket',
            
            # Q&A & Documentation
            'stackoverflow.com': '開發資源/Stack Overflow',
            'developer.mozilla.org': '開發資源/MDN',
            'docs.microsoft.com': '開發資源/Microsoft Docs',
            'developer.apple.com': 'Apple開發/官方文件',
            
            # Technical Articles & Blogs
            'medium.com': '技術文章/Medium',
            'dev.to': '技術文章/Dev.to',
            'hashnode.com': '技術文章/Hashnode',
            'blog.csdn.net': '中文技術/CSDN',
            'www.cnblogs.com': '中文技術/博客園',
            'juejin.cn': '中文技術/掘金',
            'segmentfault.com': '中文技術/SegmentFault',
            'www.jianshu.com': '中文技術/簡書',
            'ithelp.ithome.com.tw': '學習資源/iT邦幫忙',
            
            # Official Documentation
            'react.dev': 'React/官方文件',
            'reactjs.org': 'React/官方文件',
            'nextjs.org': 'React/Next.js',
            'vuejs.org': 'Vue/官方文件',
            'angular.io': 'Angular/官方文件',
            'swift.org': 'Apple開發/Swift',
            'kotlinlang.org': 'Kotlin/官方文件',
            'nodejs.org': 'JavaScript/Node.js',
            'python.org': 'Python/官方文件',
            'golang.org': 'Go/官方文件',
            'rust-lang.org': 'Rust/官方文件',
            
            # Package Managers & Libraries
            'npmjs.com': 'JavaScript/NPM',
            'pypi.org': 'Python/PyPI',
            'crates.io': 'Rust/Crates',
            'maven.apache.org': 'Java/Maven',
            'cocoapods.org': 'Apple開發/CocoaPods',
            
            # Learning Platforms
            'www.udemy.com': '學習資源/Udemy',
            'www.coursera.org': '學習資源/Coursera',
            'www.youtube.com': '影音學習/YouTube',
            'www.bilibili.com': '影音學習/Bilibili',
            'www.skillshare.com': '學習資源/Skillshare',
            
            # Cloud Platforms
            'aws.amazon.com': '雲服務/AWS',
            'cloud.google.com': '雲服務/GCP',
            'azure.microsoft.com': '雲服務/Azure',
            'vercel.com': '雲服務/Vercel',
            'netlify.com': '雲服務/Netlify',
            'heroku.com': '雲服務/Heroku',
            'digitalocean.com': '雲服務/DigitalOcean',
            
            # Backend Services
            'firebase.google.com': '後端/Firebase',
            'supabase.com': '後端/Supabase',
            'mongodb.com': '資料庫/MongoDB',
            'www.postgresql.org': '資料庫/PostgreSQL',
            'www.mysql.com': '資料庫/MySQL',
            'redis.io': '資料庫/Redis',
            
            # Design & UI
            'figma.com': '設計/Figma',
            'dribbble.com': '設計/Dribbble',
            'www.sketch.com': '設計/Sketch',
            'www.adobe.com': '設計/Adobe',
            'uiverse.io': '設計/UI元件',
            
            # AI & ML
            'chat.openai.com': 'AI工具/ChatGPT',
            'claude.ai': 'AI工具/Claude',
            'gemini.google.com': 'AI工具/Gemini',
            'huggingface.co': 'AI工具/Hugging Face',
            
            # Development Tools
            'codepen.io': '開發工具/CodePen',
            'jsfiddle.net': '開發工具/JSFiddle',
            'replit.com': '開發工具/Replit',
            'glitch.com': '開發工具/Glitch',
        }
        
        # Keyword patterns for categorization
        self.keyword_patterns = {
            'React': ['react', 'jsx', 'hooks', 'redux', 'nextjs', 'next.js', 'gatsby'],
            'Vue': ['vue', 'vuex', 'nuxt'],
            'Angular': ['angular', 'typescript'],
            'Swift': ['swift', 'swiftui', 'ios', 'macos', 'watchos'],
            'Kotlin': ['kotlin', 'android'],
            'JavaScript': ['javascript', 'js', 'es6', 'es2015', 'node.js', 'nodejs'],
            'TypeScript': ['typescript', 'ts'],
            'Python': ['python', 'django', 'flask', 'fastapi'],
            'Java': ['java', 'spring', 'maven'],
            'C#': ['c#', 'csharp', '.net', 'dotnet', 'mvc', 'asp.net'],
            'Go': ['golang', 'go'],
            'Rust': ['rust'],
            'API': ['api', 'rest', 'graphql', 'grpc', 'websocket'],
            'Database': ['database', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis'],
            'DevOps': ['docker', 'kubernetes', 'ci/cd', 'jenkins', 'github actions', 'gitlab ci'],
            'Security': ['security', '資安', 'encryption', 'auth', 'oauth', 'jwt', 'ssl', 'tls', 'mb3'],
            'Testing': ['test', 'jest', 'pytest', 'mocha', 'cypress', 'selenium'],
            'Tools': ['git', 'webpack', 'vite', 'npm', 'yarn', 'eslint', 'prettier'],
        }
    
    def classify(self, bookmark: Dict) -> str:
        """Classify a single bookmark."""
        url = bookmark.get('url', '').lower()
        title = bookmark.get('title', '').lower()
        folder = bookmark.get('folder', '').lower()
        
        # 1. Check domain mapping first (highest priority)
        category = self._classify_by_domain(url)
        if category:
            return category
        
        # 2. Check title keywords
        category = self._classify_by_keywords(title)
        if category:
            return f'{category}/資源'
        
        # 3. Check URL keywords
        category = self._classify_by_keywords(url)
        if category:
            return f'{category}/資源'
        
        # 4. Preserve meaningful folder structure
        category = self._classify_by_folder(folder)
        if category:
            return category
        
        # 5. Default category
        return '未分類'
    
    def _classify_by_domain(self, url: str) -> str:
        """Classify by domain."""
        try:
            domain = urlparse(url).netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Exact match
            if domain in self.domain_categories:
                return self.domain_categories[domain]
            
            # Partial match
            for key_domain, category in self.domain_categories.items():
                if key_domain in domain or domain in key_domain:
                    return category
        except:
            pass
        
        return None
    
    def _classify_by_keywords(self, text: str) -> str:
        """Classify by keyword patterns."""
        for category, keywords in self.keyword_patterns.items():
            for keyword in keywords:
                if keyword in text:
                    return category
        return None
    
    def _classify_by_folder(self, folder: str) -> str:
        """Classify by folder structure."""
        if not folder or folder == '書籤列':
            return None
        
        # Clean folder name
        folder = folder.replace('書籤列/', '').strip()
        
        # Skip imported folders
        if folder.startswith('已匯入'):
            return None
        
        # Map known folders
        folder_map = {
            'react': 'React',
            'nextjs': 'React/Next.js',
            'next.js': 'React/Next.js',
            'vue': 'Vue',
            'angular': 'Angular',
            'swift': 'Apple開發/Swift',
            'ios': 'Apple開發/iOS',
            'android': 'Android開發',
            'kotlin': 'Kotlin',
            'rn': 'React/React Native',
            'react native': 'React/React Native',
            'js': 'JavaScript',
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'python': 'Python',
            'java': 'Java',
            'c#': 'C#',
            'go': 'Go',
            'rust': 'Rust',
            'api': '後端/API',
            'api core': '後端/API',
            'database': '資料庫',
            'sql': '資料庫/SQL',
            'mongodb': '資料庫/MongoDB',
            'docker': 'DevOps/Docker',
            'kubernetes': 'DevOps/Kubernetes',
            'git': '開發工具/Git',
            'webpack': '開發工具/Webpack',
            'vite': '開發工具/Vite',
            'security': '資安',
            '資安': '資安',
            'mb3': '資安/MB3',
            'mb3 資安': '資安/MB3',
            'shms': 'SHMS系統',
            'shms7_api': 'SHMS系統/API',
            'test': '測試',
            'testing': '測試',
        }
        
        folder_lower = folder.lower()
        for key, category in folder_map.items():
            if key in folder_lower:
                return category
        
        # Return original folder if meaningful
        if len(folder) > 2 and not folder.startswith('已匯入'):
            return folder
        
        return None
    
    def classify_batch(self, bookmarks: List[Dict]) -> Dict[str, List[Dict]]:
        """Classify multiple bookmarks."""
        categorized = defaultdict(list)
        
        for bm in bookmarks:
            category = self.classify(bm)
            categorized[category].append(bm)
        
        # Sort categories and bookmarks
        organized = {}
        for category in sorted(categorized.keys()):
            organized[category] = sorted(
                categorized[category],
                key=lambda x: x.get('title', '').lower()
            )
        
        return organized
    
    def get_category_stats(self, organized: Dict) -> List[Tuple[str, int]]:
        """Get category statistics."""
        stats = [(cat, len(bms)) for cat, bms in organized.items()]
        return sorted(stats, key=lambda x: -x[1])


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Bookmark Classifier')
    parser.add_argument('input', help='Input JSON file from bookmark_parser.py')
    parser.add_argument('--output', default='classified.json', help='Output JSON file')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    # Load bookmarks
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    bookmarks = data.get('bookmarks', [])
    print(f'載入 {len(bookmarks)} 個書籤...')
    
    # Classify
    classifier = BookmarkClassifier()
    organized = classifier.classify_batch(bookmarks)
    
    # Save
    output_data = {
        'total': len(bookmarks),
        'categories': len(organized),
        'bookmarks': organized
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f'✅ 已分類並保存到: {args.output}')
    
    if args.stats:
        print('\n📊 分類統計:')
        stats = classifier.get_category_stats(organized)
        for category, count in stats[:20]:
            print(f'  {category}: {count}')


if __name__ == '__main__':
    main()
