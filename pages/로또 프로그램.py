# lotto_weighted_app.py
import streamlit as st
import requests
import pandas as pd
import numpy as np
import datetime
import os
import json
from pathlib import Path
from functools import lru_cache

# ---------------------------
# 설정
# ---------------------------
st.set_page_config(page_title="가중 로또 번호 생성기 (역대 통계 반영)", layout="centered")
st.title("🎯 가중 로또 번호 생성기 — 최근 30년 통계 반영")

CACHE_PATH = Path("lotto_history_cache.json")
API_URL_TEMPLATE = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}"  # 공개된 회차 API 예제

# ---------------------------
# 유틸: 로또 데이터 불러오기 (API 반복 호출, 캐시 사용)
# ---------------------------
def fetch_draw(drw_no: int):
    url = API_URL_TEMPLATE.format(drw_no)
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return None
    try:
        data = r.json()
    except Exception:
        return None
    # API 응답에서 'returnValue' 체크(정상/fail) - 일부 예제 API는 이를 포함
    return data

def load_history_cached_or_api(max_round_guess=2000):
    """
    캐시가 있으면 캐시 사용. 없으면 API로 최신 회차부터 역추적해서 데이터 수집.
    (참고: 동행복권 웹에서 회차별 API 호출 방식이 널리 사용됩니다.) 2
    """
    # 캐시 있으면 사용
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # 캐시 없으면 API로 수집: 1회부터 최신까지 시도 (성능 고려)
    draws = []
    # 먼저 최신 번호 추정(예: 2000회 내외). 실제 최신 회차는 API에서 확인 가능하므로 역추적 시 멈춤 조건 둠.
    for rn in range(1, max_round_guess + 1):
        data = fetch_draw(rn)
        if not data or data.get("returnValue") in ("fail", None) and "drwtNo1" not in data:
            # 일부 회차에서는 형식이 다르거나 아직 존재하지 않을 수 있음 — 무시
            # continue rather than break, because early rounds exist while later may not
            continue
        # 기본 필드 추출 (회차, 날짜, 6개 번호)
        try:
            draw_date = data.get("drwNoDate")  # "YYYY-MM-DD"
            numbers = [
                data.get(f"drwtNo{i}") for i in range(1, 7)
            ]
            if None in numbers:
                continue
            draws.append({
                "round": int(data.get("drwNo")),
                "date": draw_date,
                "numbers": numbers
            })
        except Exception:
            continue

    # 정렬 및 캐시 저장
    draws = sorted(draws, key=lambda x: x["round"])
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(draws, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return draws

# ---------------------------
# 가중치 계산: 최근
