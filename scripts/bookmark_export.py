#!/usr/bin/env python3
"""
Bookmark Exporter
Exports bookmarks to various formats.
"""

import json
import argparse
from datetime import datetime
from pathlib import Path


def export_to_html(bookmarks_data, output_path):
    """Export bookmarks to Netscape Bookmark HTML format."""
    
    # Handle both flat list and categorized dict formats
    if isinstance(bookmarks_data, dict) and 'bookmarks' in bookmarks_data:
        # Categorized format from classifier
        organized = bookmarks_data['bookmarks']
    elif isinstance(bookmarks_data, list):
        # Flat list format
        organized = {}
        for bm in bookmarks_data:
            folder = bm.get('folder', 'Root')
            if folder not in organized:
                organized[folder] = []
            organized[folder].append(bm)
    else:
        organized = bookmarks_data
    
    lines = [
        '<!DOCTYPE NETSCAPE-Bookmark-file-1>',
        '<!-- This is an automatically generated file. -->',
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        '<TITLE>Bookmarks</TITLE>',
        '<H1>Bookmarks</H1>',
        '<DL><p>'
    ]
    
    total = 0
    
    # Handle categorized format
    if isinstance(organized, dict):
        for category in sorted(organized.keys()):
            bookmarks = organized[category]
            
            # Skip if category is a string (shouldn't happen but safety check)
            if isinstance(bookmarks, str):
                continue
            
            lines.append(f'    <DT><H3>{category}</H3>')
            lines.append('    <DL><p>')
            
            # Handle both list and dict of bookmarks
            if isinstance(bookmarks, list):
                for bm in bookmarks:
                    if isinstance(bm, dict):
                        title = bm.get('title', 'Untitled').replace('<', '&lt;').replace('>', '&gt;')
                        url = bm.get('url', '').replace('"', '&quot;')
                        lines.append(f'        <DT><A HREF="{url}">{title}</A>')
                        total += 1
            
            lines.append('    </DL><p>')
    
    lines.append('</DL><p>')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return total


def export_to_markdown(bookmarks_data, output_path):
    """Export bookmarks to Markdown format."""
    
    # Handle both flat list and categorized dict formats
    if isinstance(bookmarks_data, dict) and 'bookmarks' in bookmarks_data:
        organized = bookmarks_data['bookmarks']
    elif isinstance(bookmarks_data, list):
        organized = {}
        for bm in bookmarks_data:
            folder = bm.get('folder', 'Root')
            if folder not in organized:
                organized[folder] = []
            organized[folder].append(bm)
    else:
        organized = bookmarks_data
    
    lines = ['# Bookmarks\n']
    
    total = 0
    
    if isinstance(organized, dict):
        for category in sorted(organized.keys()):
            bookmarks = organized[category]
            
            if isinstance(bookmarks, str):
                continue
            
            lines.append(f'\n## {category}\n')
            
            if isinstance(bookmarks, list):
                for bm in bookmarks:
                    if isinstance(bm, dict):
                        title = bm.get('title', 'Untitled')
                        url = bm.get('url', '')
                        lines.append(f'- [{title}]({url})')
                        total += 1
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return total


def export_to_json(bookmarks_data, output_path):
    """Export bookmarks to JSON format."""
    
    # If already in categorized format, keep it
    if isinstance(bookmarks_data, dict) and 'bookmarks' in bookmarks_data:
        data = bookmarks_data
    else:
        # Convert to flat list
        bookmarks = []
        if isinstance(bookmarks_data, dict):
            for category, items in bookmarks_data.items():
                if isinstance(items, list):
                    bookmarks.extend(items)
        else:
            bookmarks = bookmarks_data
        
        data = {
            'exported_at': datetime.now().isoformat(),
            'count': len(bookmarks),
            'bookmarks': bookmarks
        }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Bookmark Exporter')
    parser.add_argument('input', help='Input JSON file (from bookmark_parser.py or bookmark_classifier.py)')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('--format', choices=['html', 'markdown', 'json'], 
                        default='html', help='Output format')
    
    args = parser.parse_args()
    
    # Load bookmarks
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if args.format == 'html':
        total = export_to_html(data, args.output)
    elif args.format == 'markdown':
        total = export_to_markdown(data, args.output)
    elif args.format == 'json':
        export_to_json(data, args.output)
        total = 'N/A'
    
    print(f'✅ 已匯出到: {args.output}')


if __name__ == '__main__':
    main()
