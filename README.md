# QR Code 產生器

這個專案使用 PyScript 在瀏覽器中執行 Python，輸入網址後即可產生並下載 QR Code SVG。

## 本機執行

在專案根目錄開啟終端機，執行：

```powershell
py -m http.server 8000
```

接著用瀏覽器開啟 <http://localhost:8000>。第一次載入時需要連線下載 PyScript 和 `qrcode` 套件。

## 專案檔案

- `index.html`：頁面與表單。
- `main.py`：網址驗證及 QR Code 產生邏輯。
- `pyscript.json`：PyScript 使用的 Python 套件設定。 