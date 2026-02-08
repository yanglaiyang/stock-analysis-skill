# Stock Analysis Skill Reference

## Environment
- `GEMINI_API_KEY` or `GOOGLE_API_KEY` must be set for full online analysis.
- Tushare MCP is optional but recommended for richer data.
- Never store API keys in files or commit them to Git.

## Primary Command
```bash
python3 src/stock_analyzer.py -c "<公司名, 代码>"
```

## Output
- HTML report generated in repo root:
  - `<公司名>_分析报告_YYYYMMDD.html`

## Mermaid Rendering
- Mermaid blocks must be in the final HTML as:
  ```html
  <div class="mermaid">graph TD ...</div>
  ```
- The report template loads Mermaid:
  - Preferred: embedded script in HTML
  - Fallback: CDN (requires internet)

## Common Issues
- **Charts missing**: placeholders not replaced or images not embedded.
- **Mermaid not rendering**: no Mermaid script or blocks were escaped.
