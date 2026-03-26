# Bookmark Manager

An intelligent browser bookmark management skill for OpenClaw. Parse, search, organize, and export bookmarks from Chrome, Firefox, Safari, and Edge with AI-powered categorization.

## Features

- **Multi-browser support**: Chrome, Firefox, Safari, Edge
- **Smart search**: Search by title, URL, or folder
- **Duplicate detection**: Find duplicate bookmarks by URL
- **AI-powered categorization**: Intelligently categorize bookmarks based on:
  - Domain analysis (GitHub, Stack Overflow, Medium, etc.)
  - Content keywords (React, Swift, Python, etc.)
  - User bookmark patterns and folder structure
- **Export formats**: HTML (Netscape format), Markdown, JSON
- **Statistics**: Analyze bookmark usage patterns and top domains

## Installation

### Method 1: Install via OpenClaw

```bash
openclaw skills install bookmark-manager
```

### Method 2: Manual Installation

1. Download `bookmark-manager.skill` from releases
2. Place in your OpenClaw skills directory:
   - macOS: `~/.qclaw/skills/`
   - Linux: `~/.openclaw/skills/`

## Quick Start

### List all bookmarks

```bash
python3 scripts/bookmark_parser.py list
```

### Search bookmarks

```bash
python3 scripts/bookmark_parser.py search "keyword"
python3 scripts/bookmark_parser.py search "github.com" --field url
```

### Find duplicates

```bash
python3 scripts/bookmark_parser.py duplicates
```

### Show statistics

```bash
python3 scripts/bookmark_parser.py stats
```

### AI-powered organization

```bash
# Classify bookmarks using AI
python3 scripts/bookmark_classifier.py bookmarks.json --stats

# Export organized bookmarks
python3 scripts/bookmark_export.py classified.json output.html --format html
```

### Export bookmarks

```bash
# Export to JSON
python3 scripts/bookmark_parser.py list --format json > bookmarks.json

# Convert to HTML
python3 scripts/bookmark_export.py bookmarks.json output.html --format html

# Convert to Markdown
python3 scripts/bookmark_export.py bookmarks.json output.md --format markdown
```

## Supported Browsers

| Browser | macOS Path |
|---------|-----------|
| Chrome | `~/Library/Application Support/Google/Chrome/Default/Bookmarks` |
| Safari | `~/Library/Safari/Bookmarks.plist` |
| Edge | `~/Library/Application Support/Microsoft Edge/Default/Bookmarks` |
| Firefox | `~/Library/Application Support/Firefox/Profiles/*.default/places.sqlite` |

## Commands Reference

### `list`

List all bookmarks with optional filtering.

```bash
python3 scripts/bookmark_parser.py list [options]

Options:
  --browser {chrome,firefox,safari,edge}  Specify browser
  --format {json,text}                    Output format (default: json)
  --folder FOLDER                         Filter by folder name
```

### `search`

Search bookmarks by keyword.

```bash
python3 scripts/bookmark_parser.py search QUERY [options]

Options:
  --browser {chrome,firefox,safari,edge}  Specify browser
  --field {all,title,url,folder}          Search field (default: all)
```

### `duplicates`

Find duplicate bookmarks (same URL).

```bash
python3 scripts/bookmark_parser.py duplicates [options]
```

### `stats`

Show bookmark statistics.

```bash
python3 scripts/bookmark_parser.py stats [options]
```

### `classify` (AI-powered)

Intelligently categorize bookmarks using AI pattern matching.

```bash
python3 scripts/bookmark_classifier.py INPUT.json [options]

Options:
  --output FILE    Output JSON file (default: classified.json)
  --stats          Show category statistics
```

## AI Categorization System

The classifier uses multi-level pattern matching to intelligently organize bookmarks:

### Level 1: Domain Analysis
Recognizes popular platforms and maps to categories:
- **Development**: GitHub, GitLab, Stack Overflow, MDN
- **Learning**: Medium, Dev.to, iT邦幫忙, YouTube
- **Official Docs**: React, Vue, Swift, Node.js, Python
- **Cloud**: AWS, GCP, Azure, Vercel
- **Databases**: MongoDB, PostgreSQL, Firebase

### Level 2: Content Keywords
Detects technology keywords in title and URL:
- **Frontend**: React, Vue, Angular, Next.js, Svelte
- **Mobile**: Swift, iOS, Kotlin, Android, React Native
- **Backend**: Node.js, Python, Java, C#, Go, Rust
- **Database**: SQL, MongoDB, PostgreSQL, Redis
- **DevOps**: Docker, Kubernetes, CI/CD, GitHub Actions
- **Security**: Encryption, OAuth, JWT, SSL/TLS

### Level 3: Folder Structure
Preserves meaningful user-created folder names:
- React, Vue, Angular, Swift, Kotlin
- JavaScript, TypeScript, Python, Java, C#
- API, Database, DevOps, Security, Testing

### Level 4: Fallback
Unclassified bookmarks go to "未分類" for manual review.

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

## Real-World Category Examples

Based on analysis of 612 bookmarks:

| Category | Count | Examples |
|----------|-------|----------|
| 開發資源/GitHub | 52 | GitHub repositories, projects |
| React | 33 | React tutorials, libraries |
| Swift | 30 | Swift documentation, tutorials |
| 技術文章/Medium | 28 | Technical articles on Medium |
| 學習資源/iT邦幫忙 | 23 | iT邦幫忙 tutorials |
| 中文技術/CSDN | 22 | CSDN technical articles |
| 開發資源/Stack Overflow | 22 | Stack Overflow Q&A |
| JavaScript | 16 | JavaScript resources |
| 影音學習/YouTube | 16 | YouTube tutorials |
| Apple開發/官方文件 | 10 | Apple official documentation |

## Common Use Cases

### Find all GitHub bookmarks

```bash
python3 scripts/bookmark_parser.py search github --field url
```

### List bookmarks in a specific folder

```bash
python3 scripts/bookmark_parser.py list --folder "React" --format text
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

### Organize and categorize all bookmarks

```bash
python3 scripts/bookmark_parser.py list --format json > bookmarks.json
python3 scripts/bookmark_classifier.py bookmarks.json --stats
python3 scripts/bookmark_export.py classified.json organized.html --format html
```

## Advanced: Customizing Categories

Edit `scripts/bookmark_classifier.py` to customize categorization:

1. **Domain mappings**: Add new domain → category mappings
2. **Keyword patterns**: Add technology keywords and categories
3. **Folder mappings**: Map user folder names to categories

Example:

```python
self.domain_categories = {
    'mycompany.com': 'Company Resources/Internal',
    'custom-docs.io': 'Custom Documentation',
}

self.keyword_patterns = {
    'MyFramework': ['myframework', 'mf-'],
}
```

## Notes

- Safari requires Full Disk Access permission on macOS
- Firefox uses SQLite database, may be locked when browser is running
- Auto-detection prefers Chrome > Safari > Edge > Firefox
- AI classification is based on pattern matching, not ML models
- Unclassified bookmarks can be manually reviewed and recategorized

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
