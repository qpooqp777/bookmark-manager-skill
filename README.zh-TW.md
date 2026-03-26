# 瀏覽器書籤管理器

適用於 OpenClaw/Codex 的瀏覽器書籤管理工具。支援解析、搜尋、整理和匯出 Chrome、Firefox、Safari 和 Edge 的書籤。

## 功能特色

- **多瀏覽器支援**：Chrome、Firefox、Safari、Edge
- **智慧搜尋**：依標題、URL 或資料夾搜尋
- **重複偵測**：找出重複的書籤
- **AI 智能分類**：依網域和內容自動分類
- **匯出格式**：HTML（Netscape 格式）、Markdown、JSON
- **統計分析**：分析書籤使用模式

## 安裝方式

### 方法一：透過 OpenClaw 安裝

```bash
openclaw skills install bookmark-manager
```

### 方法二：手動安裝

1. 從 Releases 下載 `bookmark-manager.skill`
2. 放置到 OpenClaw skills 目錄：
   - macOS: `~/.qclaw/skills/`
   - Linux: `~/.openclaw/skills/`

## 快速開始

### 列出所有書籤

```bash
python3 scripts/bookmark_parser.py list
```

### 搜尋書籤

```bash
python3 scripts/bookmark_parser.py search "關鍵字"
python3 scripts/bookmark_parser.py search "github.com" --field url
```

### 找出重複書籤

```bash
python3 scripts/bookmark_parser.py duplicates
```

### 顯示統計資訊

```bash
python3 scripts/bookmark_parser.py stats
```

### 匯出書籤

```bash
# 匯出為 JSON
python3 scripts/bookmark_parser.py list --format json > bookmarks.json

# 轉換為 HTML
python3 scripts/bookmark_export.py bookmarks.json output.html --format html

# 轉換為 Markdown
python3 scripts/bookmark_export.py bookmarks.json output.md --format markdown
```

### AI 智能整理

```bash
# 整理並分類書籤
python3 scripts/bookmark_organizer.py bookmarks.json --html organized.html --summary report.md
```

## 支援的瀏覽器

| 瀏覽器 | macOS 路徑 |
|--------|-----------|
| Chrome | `~/Library/Application Support/Google/Chrome/Default/Bookmarks` |
| Safari | `~/Library/Safari/Bookmarks.plist` |
| Edge | `~/Library/Application Support/Microsoft Edge/Default/Bookmarks` |
| Firefox | `~/Library/Application Support/Firefox/Profiles/*.default/places.sqlite` |

## 指令參考

### `list` - 列出書籤

```bash
python3 scripts/bookmark_parser.py list [選項]

選項:
  --browser {chrome,firefox,safari,edge}  指定瀏覽器
  --format {json,text}                    輸出格式（預設: json）
  --folder 資料夾名稱                      依資料夾篩選
```

### `search` - 搜尋書籤

```bash
python3 scripts/bookmark_parser.py search 關鍵字 [選項]

選項:
  --browser {chrome,firefox,safari,edge}  指定瀏覽器
  --field {all,title,url,folder}          搜尋欄位（預設: all）
```

### `duplicates` - 找出重複

```bash
python3 scripts/bookmark_parser.py duplicates [選項]
```

### `stats` - 統計資訊

```bash
python3 scripts/bookmark_parser.py stats [選項]
```

## 輸出格式

每個書籤物件包含：

```json
{
  "title": "書籤標題",
  "url": "https://example.com",
  "folder": "資料夾/子資料夾",
  "date_added": 1234567890,
  "source": "chrome"
}
```

## AI 分類類別

整理器會自動將書籤分類為：

- **開發資源**：GitHub、Stack Overflow
- **技術文章**：Medium、Dev.to、iT邦幫忙
- **Apple 開發**：Swift、iOS、官方文件
- **React 生態**：React、Next.js、React Native
- **JavaScript/TypeScript**：Node.js、NPM
- **中文技術**：CSDN、博客園、掘金
- **學習資源**：YouTube、Udemy、Coursera
- **雲服務**：AWS、GCP、Azure、Vercel
- **後端**：Firebase、Supabase、MongoDB
- **DevOps**：Docker、Kubernetes、CI/CD
- **設計**：Figma、Dribbble

## 使用範例

### 找出所有 GitHub 書籤

```bash
python3 scripts/bookmark_parser.py search github --field url
```

### 列出特定資料夾的書籤

```bash
python3 scripts/bookmark_parser.py list --folder "工作" --format text
```

### 檢查重複 URL

```bash
python3 scripts/bookmark_parser.py duplicates
```

### 匯出為可分享的 Markdown

```bash
python3 scripts/bookmark_parser.py list --format json > /tmp/bm.json
python3 scripts/bookmark_export.py /tmp/bm.json bookmarks.md --format markdown
```

## 注意事項

- Safari 在 macOS 上需要完整磁碟存取權限
- Firefox 使用 SQLite 資料庫，瀏覽器執行時可能會被鎖定
- 自動偵測順序：Chrome > Safari > Edge > Firefox

## 授權

MIT License

## 貢獻

歡迎提交 Pull Request。對於重大變更，請先開啟 Issue 討論您想要變更的內容。
