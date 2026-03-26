# Bookmark Manager

A browser bookmark management tool for OpenClaw/Codex. Parse, search, organize, and export bookmarks from Chrome, Firefox, Safari, and Edge.

## Features

- **Multi-browser support**: Chrome, Firefox, Safari, Edge
- **Smart search**: Search by title, URL, or folder
- **Duplicate detection**: Find duplicate bookmarks by URL
- **AI-powered organization**: Auto-categorize bookmarks by domain and content
- **Export formats**: HTML (Netscape format), Markdown, JSON
- **Statistics**: Analyze bookmark usage patterns

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

### Export bookmarks

```bash
# Export to JSON
python3 scripts/bookmark_parser.py list --format json > bookmarks.json

# Convert to HTML
python3 scripts/bookmark_export.py bookmarks.json output.html --format html

# Convert to Markdown
python3 scripts/bookmark_export.py bookmarks.json output.md --format markdown
```

### AI-powered organization

```bash
# Organize and categorize bookmarks
python3 scripts/bookmark_organizer.py bookmarks.json --html organized.html --summary report.md
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

## AI Organization Categories

The organizer automatically categorizes bookmarks into:

- **Development Resources**: GitHub, Stack Overflow
- **Technical Articles**: Medium, Dev.to, iT邦幫忙
- **Apple Development**: Swift, iOS, Official Docs
- **React Ecosystem**: React, Next.js, React Native
- **JavaScript/TypeScript**: Node.js, NPM
- **Chinese Tech**: CSDN, 博客園, 掘金
- **Learning Resources**: YouTube, Udemy, Coursera
- **Cloud Services**: AWS, GCP, Azure, Vercel
- **Backend**: Firebase, Supabase, MongoDB
- **DevOps**: Docker, Kubernetes, CI/CD
- **Design**: Figma, Dribbble

## Examples

### Find all GitHub bookmarks

```bash
python3 scripts/bookmark_parser.py search github --field url
```

### List bookmarks in a specific folder

```bash
python3 scripts/bookmark_parser.py list --folder "Work" --format text
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

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
