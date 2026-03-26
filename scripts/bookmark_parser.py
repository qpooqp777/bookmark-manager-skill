#!/usr/bin/env python3
"""
Browser Bookmark Parser
Parses bookmark files from Chrome, Firefox, Safari, and Edge.
"""

import json
import sqlite3
import plistlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional
import os


def parse_chrome_bookmarks(path: str) -> dict:
    """Parse Chrome/Edge bookmarks JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    bookmarks = []
    
    def extract_items(node, folder_path=""):
        if node.get('type') == 'url':
            bookmarks.append({
                'title': node.get('name', ''),
                'url': node.get('url', ''),
                'folder': folder_path,
                'date_added': node.get('date_added'),
                'source': 'chrome'
            })
        elif node.get('type') == 'folder':
            current_path = f"{folder_path}/{node.get('name', '')}" if folder_path else node.get('name', '')
            for child in node.get('children', []):
                extract_items(child, current_path)
    
    # Parse bookmark bar and other bookmarks
    roots = data.get('roots', {})
    for root_name in ['bookmark_bar', 'other', 'synced']:
        if root_name in roots:
            extract_items(roots[root_name])
    
    return {'bookmarks': bookmarks, 'count': len(bookmarks)}


def parse_safari_bookmarks(path: str) -> dict:
    """Parse Safari bookmarks plist file."""
    with open(path, 'rb') as f:
        data = plistlib.load(f)
    
    bookmarks = []
    
    def extract_items(items, folder_path=""):
        for item in items:
            if item.get('WebBookmarkType') == 'WebBookmarkTypeLeaf':
                bookmarks.append({
                    'title': item.get('URIDictionary', {}).get('title', item.get('Title', '')),
                    'url': item.get('URLString', ''),
                    'folder': folder_path,
                    'source': 'safari'
                })
            elif item.get('WebBookmarkType') == 'WebBookmarkTypeList':
                current_path = f"{folder_path}/{item.get('Title', '')}" if folder_path else item.get('Title', '')
                if 'Children' in item:
                    extract_items(item['Children'], current_path)
    
    if 'Children' in data:
        extract_items(data['Children'])
    
    return {'bookmarks': bookmarks, 'count': len(bookmarks)}


def parse_firefox_bookmarks(path: str) -> dict:
    """Parse Firefox places.sqlite database."""
    bookmarks = []
    
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    # Query bookmarks with folder structure
    query = """
    SELECT 
        b.title,
        p.url,
        b.dateAdded,
        GROUP_CONCAT(f.title, '/') as folder_path
    FROM moz_bookmarks b
    JOIN moz_places p ON b.fk = p.id
    JOIN moz_bookmarks f ON b.parent = f.id
    WHERE b.type = 1
    GROUP BY b.id
    """
    
    cursor.execute(query)
    for row in cursor.fetchall():
        bookmarks.append({
            'title': row[0] or '',
            'url': row[1] or '',
            'folder': row[3] or '',
            'date_added': row[2],
            'source': 'firefox'
        })
    
    conn.close()
    return {'bookmarks': bookmarks, 'count': len(bookmarks)}


def detect_browser_and_path(browser: Optional[str] = None) -> tuple:
    """Detect browser and return bookmark file path."""
    home = Path.home()
    
    paths = {
        'chrome': home / 'Library/Application Support/Google/Chrome/Default/Bookmarks',
        'edge': home / 'Library/Application Support/Microsoft Edge/Default/Bookmarks',
        'safari': home / 'Library/Safari/Bookmarks.plist',
        'firefox': None  # Need to find profile
    }
    
    # Find Firefox profile
    firefox_dir = home / 'Library/Application Support/Firefox/Profiles'
    if firefox_dir.exists():
        for profile in firefox_dir.iterdir():
            if profile.is_dir() and profile.name.endswith('.default'):
                paths['firefox'] = profile / 'places.sqlite'
                break
    
    if browser:
        browser = browser.lower()
        if browser in paths and paths[browser]:
            return browser, str(paths[browser])
        else:
            return None, None
    
    # Auto-detect
    for browser_name, path in paths.items():
        if path and Path(path).exists():
            return browser_name, str(path)
    
    return None, None


def search_bookmarks(bookmarks: list, query: str, field: str = 'all') -> list:
    """Search bookmarks by query."""
    query = query.lower()
    results = []
    
    for bm in bookmarks:
        match = False
        if field in ['all', 'title']:
            if query in bm.get('title', '').lower():
                match = True
        if field in ['all', 'url']:
            if query in bm.get('url', '').lower():
                match = True
        if field in ['all', 'folder']:
            if query in bm.get('folder', '').lower():
                match = True
        
        if match:
            results.append(bm)
    
    return results


def find_duplicates(bookmarks: list) -> list:
    """Find duplicate bookmarks by URL."""
    seen = {}
    duplicates = []
    
    for bm in bookmarks:
        url = bm.get('url', '')
        if url in seen:
            duplicates.append({
                'url': url,
                'bookmarks': [seen[url], bm]
            })
        else:
            seen[url] = bm
    
    return duplicates


def main():
    parser = argparse.ArgumentParser(description='Browser Bookmark Parser')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all bookmarks')
    list_parser.add_argument('--browser', choices=['chrome', 'firefox', 'safari', 'edge'], help='Browser name')
    list_parser.add_argument('--format', choices=['json', 'text'], default='json', help='Output format')
    list_parser.add_argument('--folder', help='Filter by folder')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search bookmarks')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--browser', choices=['chrome', 'firefox', 'safari', 'edge'], help='Browser name')
    search_parser.add_argument('--field', choices=['all', 'title', 'url', 'folder'], default='all', help='Search field')
    
    # Duplicates command
    dup_parser = subparsers.add_parser('duplicates', help='Find duplicate bookmarks')
    dup_parser.add_argument('--browser', choices=['chrome', 'firefox', 'safari', 'edge'], help='Browser name')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show bookmark statistics')
    stats_parser.add_argument('--browser', choices=['chrome', 'firefox', 'safari', 'edge'], help='Browser name')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    browser, path = detect_browser_and_path(getattr(args, 'browser', None))
    
    if not browser:
        print(json.dumps({'error': 'No browser bookmarks found'}))
        return
    
    # Parse bookmarks
    if browser in ['chrome', 'edge']:
        data = parse_chrome_bookmarks(path)
    elif browser == 'safari':
        data = parse_safari_bookmarks(path)
    elif browser == 'firefox':
        data = parse_firefox_bookmarks(path)
    
    if args.command == 'list':
        bookmarks = data['bookmarks']
        if hasattr(args, 'folder') and args.folder:
            bookmarks = [b for b in bookmarks if args.folder.lower() in b.get('folder', '').lower()]
        
        if args.format == 'json':
            print(json.dumps({'bookmarks': bookmarks, 'count': len(bookmarks)}, ensure_ascii=False, indent=2))
        else:
            for bm in bookmarks:
                print(f"[{bm['folder']}] {bm['title']}: {bm['url']}")
    
    elif args.command == 'search':
        results = search_bookmarks(data['bookmarks'], args.query, args.field)
        print(json.dumps({'results': results, 'count': len(results)}, ensure_ascii=False, indent=2))
    
    elif args.command == 'duplicates':
        dups = find_duplicates(data['bookmarks'])
        print(json.dumps({'duplicates': dups, 'count': len(dups)}, ensure_ascii=False, indent=2))
    
    elif args.command == 'stats':
        # Calculate statistics
        folders = {}
        domains = {}
        for bm in data['bookmarks']:
            folder = bm.get('folder', 'Root')
            folders[folder] = folders.get(folder, 0) + 1
            
            try:
                from urllib.parse import urlparse
                domain = urlparse(bm.get('url', '')).netloc
                if domain:
                    domains[domain] = domains.get(domain, 0) + 1
            except:
                pass
        
        stats = {
            'total': data['count'],
            'browser': browser,
            'top_folders': sorted(folders.items(), key=lambda x: -x[1])[:10],
            'top_domains': sorted(domains.items(), key=lambda x: -x[1])[:10]
        }
        print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
