import qrcode
import io
import base64
from urllib.parse import urlparse
from qrcode.constants import ERROR_CORRECT_H
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
Max_URL_Length = 2048  # 設定最大 URL 長度

def normalize_url(raw: str) -> str:
    """整理網址，不和規顯示error"""
    url = raw.strip()
    if not url:
        raise ValueError("請輸入網址")
    if len(url) > Max_URL_Length:
        raise ValueError(f"網址過長，請限制在 {Max_URL_Length} 個字符以內")
    if "://" not in url:
        url = "https://" + url  # 預設加上 https://
    try:
        parsed = urlparse(url)
    except Exception as e:
        raise ValueError("網址格式不正確")
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("網址格式不正確")
    return url


def make_qr_data_url(url: str, box_size: int = 10) -> str:
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=box_size, border=4)   
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded_image}"


@app.route("/", methods=["GET", "POST"])

def index():
    url = None 
    qr_img = None
    error = None  # 預設 QR Code 圖片

    
    
    if request.method == "POST":
        try:
            url = normalize_url(request.form.get("url", ""))
            qr_img = make_qr_data_url(url)
            
        except ValueError as e:
            error = str(e)
    return render_template("index.html", url=url, qr_img=qr_img, error=error)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)