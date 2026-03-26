---
name: bookmark-manager
description: |
  Browser bookmark management tool. Parse, search, organize, and export bookmarks from Chrome, Firefox, Safari, and Edge. Use when users want to: (1) read/view browser bookmarks, (2) search bookmarks by keyword, (3) find duplicate bookmarks, (4) export bookmarks to HTML/Markdown/JSON, (5) analyze bookmark statistics, (6) organize bookmarks. Keywords: 書籤, bookmark, 瀏覽器, browser, Chrome, Firefox, Safari, Edge.
---

# Bookmark Manager

Manage browser bookmarks across Chrome, Firefox, Safari, and Edge.

## Quick Start

### List all bookmarks

```bash
python3 scripts/bookmark_parser.py list
```

### Search bookmarks

```bash
python3 scripts/bookmark_parser.py search "關鍵字"
python3 scripts/bookmark_parser.py search "github" --field url
```

### Find duplicates

```bash
python3 scripts/bookmark_parser.py duplicates
```

### Show statistics

```bash
python3 scripts/bookmark_parser.py stats
```

### Export bookmarks

```bash
# First export to JSON
python3 scripts/bookmark_parser.py list --format json > bookmarks.json

# Then convert to other formats
python3 scripts/bookmark_export.py bookmarks.json bookmarks.html --format html
python3 scripts/bookmark_export.py bookmarks.json bookmarks.md --format markdown
```

## AI Smart Classification

Automatically categorize bookmarks using AI pattern matching:

```bash
# Classify and generate organized HTML
python3 scripts/bookmark_classifier.py bookmarks.json --output-html bookmarks_organized.html --report

# With JSON output for further processing
python3 scripts/bookmark_classifier.py bookmarks.json --output-html out.html --output-json out.json
```

### AI Categories

- **Frontend/**: React, Vue, Angular, General
- **Backend/**: Node.js, Python, Java, Go, Database, API
- **Mobile/**: iOS-Swift, Android, React Native, Flutter
- **DevOps/**: Docker, CI-CD, Cloud, Git
- **AI-ML/**: General, Models
- **Library/**: Systems (for library management systems)
- **Community/**: Forums, Chinese-Tech, Medium, StackOverflow
- **Tools/**: IDE, Design, Google, Utilities
- **Learning/**: Tutorials, Documentation
- **Architecture/**: Patterns (MVVM, MVC, etc.)
- **Testing/**: Unit tests, E2E, automation
- **Security/**: Auth, encryption, vulnerabilities
- **Development/**: GitHub, Localhost
- **Network/**: Internal-IP
- **Browser/**: Extensions

## Supported Browsers

| Browser | macOS Path |
|---------|-----------|
| Chrome | `~/Library/Application Support/Google/Chrome/Default/Bookmarks` |
| Safari | `~/Library/Safari/Bookmarks.plist` |
| Edge | `~/Library/Application Support/Microsoft Edge/Default/Bookmarks` |
| Firefox | `~/Library/Application Support/Firefox/Profiles/*.default/places.sqlite` |

## Commands Reference

### list

List all bookmarks.

```bash
python3 scripts/bookmark_parser.py list [options]

Options:
  --browser {chrome,firefox,safari,edge}  Specify browser
  --format {json,text}                    Output format (default: json)
  --folder FOLDER                         Filter by folder name
```

### search

Search bookmarks by keyword.

```bash
python3 scripts/bookmark_parser.py search QUERY [options]

Options:
  --browser {chrome,firefox,safari,edge}  Specify browser
  --field {all,title,url,folder}          Search field (default: all)
```

### duplicates

Find duplicate bookmarks (same URL).

```bash
python3 scripts/bookmark_parser.py duplicates [options]

Options:
  --browser {chrome,firefox,safari,edge}  Specify browser
```

### stats

Show bookmark statistics (total count, top folders, top domains).

```bash
python3 scripts/bookmark_parser.py stats [options]

Options:
  --browser {chrome,firefox,safari,edge}  Specify browser
```

## Output Format

Each bookmark object contains:

```json
{
  "title": "Bookmark Title",
  "url": "https://example.com",
  "folder": "Folder/Subfolder",
  "date_added": 1234567890,
  "source": "chrome"
}
```

## Common Use Cases

### Find all GitHub bookmarks

```bash
python3 scripts/bookmark_parser.py search github --field url
```

### List bookmarks in a specific folder

```bash
python3 scripts/bookmark_parser.py list --folder "工作" --format text
```

### Check for duplicate URLs

```bash
python3 scripts/bookmark_parser.py duplicates
```

### Export to shareable Markdown

```bash
python3 scripts/bookmark_parser.py list --format json > /tmp/bm.json
python3 scripts/bookmark_export.py /tmp/bm.json bookmarks.md --format markdown
```

## Notes

- Safari requires Full Disk Access permission on macOS
- Firefox uses SQLite database, may be locked when browser is running
- Auto-detection prefers Chrome > Safari > Edge > Firefox
