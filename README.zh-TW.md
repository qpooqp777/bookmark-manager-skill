# 瀏覽器書籤管理器

適用於 OpenClaw 的智能瀏覽器書籤管理工具。支援解析、搜尋、整理和匯出 Chrome、Firefox、Safari 和 Edge 的書籤，並具備 AI 智能分類功能。

## 功能特色

- **多瀏覽器支援**：Chrome、Firefox、Safari、Edge
- **智慧搜尋**：依標題、URL 或資料夾搜尋
- **重複偵測**：找出重複的書籤
- **AI 智能分類**：基於以下因素智能分類書籤：
  - 網域分析（GitHub、Stack Overflow、Medium 等）
  - 內容關鍵字（React、Swift、Python 等）
  - 使用者書籤模式和資料夾結構
- **匯出格式**：HTML（Netscape 格式）、Markdown、JSON
- **統計分析**：分析書籤使用模式和熱門網域

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

### AI 智能整理

```bash
# 使用 AI 分類書籤
python3 scripts/bookmark_classifier.py bookmarks.json --stats

# 匯出已整理的書籤
python3 scripts/bookmark_export.py classified.json output.html --format html
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

### `classify` - AI 智能分類

```bash
python3 scripts/bookmark_classifier.py 輸入檔案.json [選項]

選項:
  --output 檔案名稱    輸出 JSON 檔案（預設: classified.json）
  --stats             顯示分類統計
```

## AI 分類系統

分類器使用多層級模式匹配來智能整理書籤：

### 第一層：網域分析
識別熱門平台並對應到分類：
- **開發資源**：GitHub、GitLab、Stack Overflow、MDN
- **學習資源**：Medium、Dev.to、iT邦幫忙、YouTube
- **官方文件**：React、Vue、Swift、Node.js、Python
- **雲服務**：AWS、GCP、Azure、Vercel
- **資料庫**：MongoDB、PostgreSQL、Firebase

### 第二層：內容關鍵字
偵測標題和 URL 中的技術關鍵字：
- **前端**：React、Vue、Angular、Next.js、Svelte
- **行動開發**：Swift、iOS、Kotlin、Android、React Native
- **後端**：Node.js、Python、Java、C#、Go、Rust
- **資料庫**：SQL、MongoDB、PostgreSQL、Redis
- **DevOps**：Docker、Kubernetes、CI/CD、GitHub Actions
- **資安**：加密、OAuth、JWT、SSL/TLS

### 第三層：資料夾結構
保留有意義的使用者建立的資料夾名稱：
- React、Vue、Angular、Swift、Kotlin
- JavaScript、TypeScript、Python、Java、C#
- API、Database、DevOps、Security、Testing

### 第四層：預設分類
未分類的書籤進入「未分類」供手動檢查

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

## 真實分類範例

基於 612 個書籤的分析：

| 分類 | 數量 | 範例 |
|------|------|------|
| 開發資源/GitHub | 52 | GitHub 倉庫、專案 |
| React | 33 | React 教學、函式庫 |
| Swift | 30 | Swift 文件、教學 |
| 技術文章/Medium | 28 | Medium 技術文章 |
| 學習資源/iT邦幫忙 | 23 | iT邦幫忙 教學 |
| 中文技術/CSDN | 22 | CSDN 技術文章 |
| 開發資源/Stack Overflow | 22 | Stack Overflow 問答 |
| JavaScript | 16 | JavaScript 資源 |
| 影音學習/YouTube | 16 | YouTube 教學 |
| Apple開發/官方文件 | 10 | Apple 官方文件 |

## 使用範例

### 找出所有 GitHub 書籤

```bash
python3 scripts/bookmark_parser.py search github --field url
```

### 列出特定資料夾的書籤

```bash
python3 scripts/bookmark_parser.py list --folder "React" --format text
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

### 整理並分類所有書籤

```bash
python3 scripts/bookmark_parser.py list --format json > bookmarks.json
python3 scripts/bookmark_classifier.py bookmarks.json --stats
python3 scripts/bookmark_export.py classified.json organized.html --format html
```

## 進階：自訂分類

編輯 `scripts/bookmark_classifier.py` 以自訂分類：

1. **網域對應**：新增網域 → 分類對應
2. **關鍵字模式**：新增技術關鍵字和分類
3. **資料夾對應**：將使用者資料夾名稱對應到分類

範例：

```python
self.domain_categories = {
    'mycompany.com': '公司資源/內部',
    'custom-docs.io': '自訂文件',
}

self.keyword_patterns = {
    'MyFramework': ['myframework', 'mf-'],
}
```

## 注意事項

- Safari 在 macOS 上需要完整磁碟存取權限
- Firefox 使用 SQLite 資料庫，瀏覽器執行時可能會被鎖定
- 自動偵測順序：Chrome > Safari > Edge > Firefox
- AI 分類基於模式匹配，不使用機器學習模型
- 未分類的書籤可以手動檢查並重新分類

## 授權

MIT License

## 貢獻

歡迎提交 Pull Request。對於重大變更，請先開啟 Issue 討論您想要變更的內容。
