import requests
import os
from dotenv import load_dotenv
from pprint import pprint
import re
import json
from pathlib import Path
from .models import Book, Category
load_dotenv()

MY_TTBKEY = os.getenv('ALADIN_API_KEY')
ALADIN_SERRCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemList.aspx'
BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "data" / "categories.json"
def select_category(CID):
    """
    CID에 따른 카테고리 분류를 마친 데이터를 불러와 조회 후 반환
    """
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        categories = json.load(f)
    cid_int = int(CID)
    for category in categories:
        cid_list = category.get("cid", [])
        if cid_int in cid_list:
            # print(category["name"])
            return category["name"]

def get_book_data(page_num, max_result):
    url = ALADIN_SERRCH_URL
    params = {
        "TTBKEY": MY_TTBKEY,
        "QueryType": 'Bestseller',
        "SearchTarget": 'Book',
        "Start": page_num,
        "MaxResults": max_result,
        "Output": 'JS',
        "Version": '20131101',   
    }
    response = requests.get(url, params=params)
    data = response.json()
    for b in data.get("item", []):
        book = Book()
        book.title = b['title']
        original_author = b['author']   # author 정보에 여는 괄호 뒤는 제거
        match = re.search(r'^(.*?)\(', original_author)
        print(match)
        if match:   # 괄호가 있다면 제거 후 반환
            processed_author = match.group(1).strip()
        else:   # 없다면 그대로 사용
            processed_author = original_author
        book.author = processed_author
        book.cover_image = b['cover']
        book.pub_date = b['pubDate']
        book.aladin_link = b['link']
        book.description = b['description']
        book.isbn = b['isbn13']
        book.publisher = b['publisher']
        book.customer_review_rank = b['customerReviewRank']
        # 카테고리 정보를 따로 추출하는 함수를 호출한다.
        try:
            book.category = Category.objects.get(name=select_category(b['categoryId']))
        except:
            continue
        book.save()
    """
    할 일:
    중복 데이터 제거 O
    CID 최소화 O
    받아온 데이터를 즉시 저장 O
    """