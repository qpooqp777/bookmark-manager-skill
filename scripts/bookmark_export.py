#!/usr/bin/env python3
"""
Bookmark Exporter
Exports bookmarks to various formats.
"""

import json
import argparse
from datetime import datetime
from pathlib import Path


def export_to_html(bookmarks: list, output_path: str):
    """Export bookmarks to Netscape Bookmark HTML format."""
    lines = [
        '<!DOCTYPE NETSCAPE-Bookmark-file-1>',
        '<!-- This is an automatically generated file. -->',
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        '<TITLE>Bookmarks</TITLE>',
        '<H1>Bookmarks</H1>',
        '<DL><p>'
    ]
    
    current_folder = None
    indent = 1
    
    for bm in sorted(bookmarks, key=lambda x: x.get('folder', '')):
        folder = bm.get('folder', '')
        
        if folder != current_folder:
            # Close previous folder
            if current_folder:
                lines.append('  ' * indent + '</DL><p>')
                indent -= 1
            
            # Open new folder
            if folder:
                lines.append('  ' * indent + f'<DT><H3>{folder}</H3>')
                lines.append('  ' * indent + '<DL><p>')
                indent += 1
            current_folder = folder
        
        title = bm.get('title', 'Untitled')
        url = bm.get('url', '')
        lines.append('  ' * indent + f'<DT><A HREF="{url}">{title}</A>')
    
    # Close remaining folders
    while indent > 1:
        lines.append('  ' * indent + '</DL><p>')
        indent -= 1
    
    lines.append('</DL><p>')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def export_to_markdown(bookmarks: list, output_path: str):
    """Export bookmarks to Markdown format."""
    lines = ['# Bookmarks\n']
    
    current_folder = None
    
    for bm in sorted(bookmarks, key=lambda x: x.get('folder', '')):
        folder = bm.get('folder', '')
        
        if folder != current_folder:
            if folder:
                lines.append(f'\n## {folder}\n')
            else:
                lines.append('\n## Root\n')
            current_folder = folder
        
        title = bm.get('title', 'Untitled')
        url = bm.get('url', '')
        lines.append(f'- [{title}]({url})')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def export_to_json(bookmarks: list, output_path: str):
    """Export bookmarks to JSON format."""
    data = {
        'exported_at': datetime.now().isoformat(),
        'count': len(bookmarks),
        'bookmarks': bookmarks
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Bookmark Exporter')
    parser.add_argument('input', help='Input JSON file (from bookmark_parser.py)')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('--format', choices=['html', 'markdown', 'json'], 
                        default='html', help='Output format')
    
    args = parser.parse_args()
    
    # Load bookmarks
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    bookmarks = data.get('bookmarks', [])
    
    if args.format == 'html':
        export_to_html(bookmarks, args.output)
    elif args.format == 'markdown':
        export_to_markdown(bookmarks, args.output)
    elif args.format == 'json':
        export_to_json(bookmarks, args.output)
    
    print(f'Exported {len(bookmarks)} bookmarks to {args.output}')


if __name__ == '__main__':
    main()
