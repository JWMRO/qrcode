import base64
import io
from urllib.parse import urlparse

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from flask import Flask, render_template, request

app = Flask(__name__)
MAX_URL_LENGTH = 2000


def normalize_url(raw: str) -> str:
    """整理使用者輸入的網址；不合法時丟出 ValueError。"""
    url = raw.strip()
    if not url:
        raise ValueError("請輸入網址")
    if len(url) > MAX_URL_LENGTH:
        raise ValueError(f"網址太長（上限 {MAX_URL_LENGTH} 字元）")
    if "://" not in url:
        url = "https://" + url
    parsed = urlparse(url)
    # 只允許 http / https，避免 javascript: 等危險協定
    if parsed.scheme not in ("http", "https") or "." not in parsed.netloc:
        raise ValueError("請輸入有效的網址，例如 https://example.com")
    return url


def make_qr_data_uri(url: str, box_size: int = 10) -> str:
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=box_size, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#14213d", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


@app.route("/", methods=["GET", "POST"])
def index():
    url = qr_image = error = None
    if request.method == "POST":
        try:
            url = normalize_url(request.form.get("url", ""))
            qr_image = make_qr_data_uri(url)
        except ValueError as e:
            error = str(e)
    return render_template("index.html", url=url, qr_image=qr_image, error=error)


if __name__ == "__main__":
    app.run(debug=True)
