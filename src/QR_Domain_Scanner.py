# QR코드와 도메인을 스캔하여 검사하는 알고리즘
import cv2
import numpy as np
import re
import requests
from pyzbar.pyzbar import decode

# 설정
SUSPICIOUS_DOMAINS = ["discord-gift.com", "free-nitro.com", "discord-airdrop.com"]  # 의심 도메인 리스트

# URL에서 도메인 추출 함수
def extract_domain(url):
    domain_pattern = re.compile(r"https?://([^/]+)/?")
    match = domain_pattern.search(url)
    return match.group(1) if match else None

# 의심 도메인인지 확인
def is_suspicious_domain(domain):
    return domain in SUSPICIOUS_DOMAINS

# 이미지에서 QR 코드 탐지
def scan_qr_code(image_path):
    img = cv2.imread(image_path)
    detected_qrs = decode(img)
    results = []

    for qr in detected_qrs:
        qr_data = qr.data.decode("utf-8")
        domain = extract_domain(qr_data)
        is_suspicious = is_suspicious_domain(domain) if domain else False
        results.append({
            "data": qr_data,
            "domain": domain,
            "suspicious": is_suspicious
        })
    return results

# 이미지에서 텍스트 기반 URL 탐지
def scan_text_for_urls(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 이미지 전처리 (노이즈 제거)
    gray = cv2.medianBlur(gray, 3)

    # pytesseract 불러오기 (OCR)
    try:
        import pytesseract
    except ImportError:
        print("[!] pytesseract 모듈이 필요합니다. 설치: pip install pytesseract")
        return []

    text = pytesseract.image_to_string(gray)
    urls = re.findall(r"https?://[\w./-]+", text)

    results = []
    for url in urls:
        domain = extract_domain(url)
        is_suspicious = is_suspicious_domain(domain) if domain else False
        results.append({
            "url": url,
            "domain": domain,
            "suspicious": is_suspicious
        })
    return results
