# Examples

## Full Analysis (Online)
```bash
export GEMINI_API_KEY="your_key"
python3 src/stock_analyzer.py -c "新华人寿, 601336.SH"
```

## Offline Fallback
If external API calls fail, the system will generate an offline summary and still produce the HTML report.
