import base64
from urllib.parse import urlparse

import qrcode
from pyscript import when, web
from qrcode.constants import ERROR_CORRECT_H
from qrcode.exceptions import DataOverflowError
from qrcode.image.svg import SvgPathFillImage

MAX_URL_LENGTH = 2048


def normalize_url(raw: str) -> str:
    url = raw.strip()
    if not url:
        raise ValueError("請輸入網址")
    if len(url) > MAX_URL_LENGTH:
        raise ValueError(f"網址過長，請限制在 {MAX_URL_LENGTH} 個字符以內")
    if "://" not in url:
        url = "https://" + url

    try:
        parsed = urlparse(url)
    except ValueError as exc:
        raise ValueError("網址格式不正確") from exc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("網址格式不正確")
    return url


def make_qr_data_url(url: str, box_size: int = 10) -> str:
    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_H,
        box_size=box_size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(image_factory=SvgPathFillImage)
    svg = image.to_string(encoding="unicode")
    encoded_image = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded_image}"


@when("submit", "#qr-form")
def generate_qr(event):
    event.preventDefault()

    url_input = web.page["url"]
    error_message = web.page["error"]
    result = web.page["result"]

    error_message.textContent = ""
    error_message.style["display"] = "none"
    result.style["display"] = "none"

    try:
        url = normalize_url(url_input.value)
    except ValueError as exc:
        error_message.textContent = str(exc)
        error_message.style["display"] = "block"
        return

    try:
        qr_data_url = make_qr_data_url(url)
    except (DataOverflowError, ValueError):
        error_message.textContent = "網址太長，無法產生 QR Code"
        error_message.style["display"] = "block"
        return

    web.page["qr-image"].src = qr_data_url
    web.page["download-link"].href = qr_data_url
    web.page["url-result"].textContent = url
    result.style["display"] = "block"
