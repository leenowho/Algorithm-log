from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Book, Thread, Category, Comment
from .serializers import (BookSerializer, BookListSerializer, 
                        CategorySerializer, ThreadSerializer, ThreadListSerializer,CommentSerializer
                        )
from .utils import create_thread_cover
from django.db.models import Q
import numpy as np  # 유사도
from django.db.models import Count
from datetime import datetime
from django.conf import settings
# --- 감성 분석용 GPT API 호출 View ---
import os  #  이 줄 추가
from openai import OpenAI  # 최신 버전 방식
import json
from django.core.paginator import Paginator
import requests
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 환경변수에서 API 키 읽기


# from .loads import get_book_data

@api_view(['GET'])
def books(request):
    page = request.GET.get('page', '1')
    category = request.GET.get('category', '')
    query = request.GET.get('query', '')

    books = Book.objects.annotate(favorite_count=Count('favorited_by')).order_by('id')

    if category:
        books = books.filter(category__name__icontains=category)
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(books, 24)
    page_obj = paginator.get_page(page)

    serializer = BookListSerializer(page_obj, many=True , context={'request': request})
    return Response({
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'results': serializer.data
    }, status=status.HTTP_200_OK)
        
@api_view(['GET']) #추가
def book_detail(request, book_id):
    if request.method == 'GET':
        book = Book.objects.annotate(favorite_count=Count('favorited_by')).get(pk=book_id)
        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_thread(request, book_id):
    if request.method == 'POST':
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            book = get_object_or_404(Book, pk=book_id)
            thread = serializer.save(book=book, user=request.user)
            create_thread_cover(thread, book)
            return Response(ThreadSerializer(thread).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def thread_list(request):
    if request.method == 'GET':
        threads = Thread.objects.annotate(
            like_count=Count('like_users')
        ).prefetch_related('like_users')  # 좋아요 정보 한 번에 미리 가져오기
        if not threads.exists():
            return Response({'detail': 'Thread가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ThreadListSerializer(threads, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET', 'PUT', 'DELETE'])
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    # Thread 상세 조회
    if request.method == 'GET':
        serializer = ThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif thread.user != request.user:   # 작성한 유저만 쓰레드에 접근할 수 있음
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        if request.method == 'PUT': # 수정
            # 수정할 때 사진을 다시 생성할지 말지 고민해볼 부분
            serializer = ThreadSerializer(thread, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                book = get_object_or_404(Book, pk=thread.book.id)
                create_thread_cover(thread, book)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':   # 삭제
            data = {"delete": f"{thread.pk}번 Thread가 삭제되었습니다."}
            thread.delete()
            return Response(data, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = get_list_or_404(Category)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
def comment_list_create(request, thread_id):
    """
    GET: 특정 쓰레드에 달린 댓글 목록 조회
    POST: 댓글 작성
    """
    if request.method == 'GET':
        comments = Comment.objects.filter(thread_id=thread_id).order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            thread = get_object_or_404(Thread, pk=thread_id)
            serializer.save(user=request.user, thread=thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def comment_delete(request, comment_id):
    """
    DELETE: 댓글 삭제 (본인만 가능)
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user != request.user:
        return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def thread_like_toggle(request, thread_id):
    """
    좋아요 토글 기능 (POST)
    """
    thread = get_object_or_404(Thread, pk=thread_id)
    user = request.user

    if user in thread.like_users.all():
        thread.like_users.remove(user)
        liked = False
    else:
        thread.like_users.add(user)
        liked = True

    return Response({
        'liked': liked,
        'like_count': thread.like_users.count()
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite_book(request, book_id):
    """
    POST: 책 찜하기 토글
    """
    book = get_object_or_404(Book, pk=book_id)
    user = request.user

    if user in book.favorited_by.all():
        book.favorited_by.remove(user)
        favorited = False
    else:
        book.favorited_by.add(user)
        favorited = True

    return Response({
        'favorited': favorited,
        'favorite_count': book.favorited_by.count()
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_favorite_books(request):
    """
    GET: 로그인 사용자가 찜한 책 목록 조회
    """
    user = request.user
    print(user)
    books = Book.objects.annotate(favorite_count=Count('favorited_by')).filter(favorited_by=user)
    serializer = BookListSerializer(books, many=True, context={ 'request': request })
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reading_calendar(request):
    """
    GET: 로그인한 사용자의 Thread를 날짜별로 집계하여 캘린더 시각화를 위한 데이터 제공
    반환 예시: [{ "read_date": "2025-05-10", "count": 2 }, ...]
    """
    user = request.user
    threads = Thread.objects.filter(user=user)\
        .values('read_date')\
        .annotate(count=Count('id'))\
        .order_by('read_date')

    return Response(threads, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def threads_by_date(request):
    """
    GET: 특정 날짜에 읽은 Thread 목록을 반환
    쿼리 파라미터: ?date=YYYY-MM-DD
    """
    user = request.user
    date_str = request.query_params.get('date')

    if not date_str:
        return Response({'error': '날짜(date) 파라미터가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': '날짜 형식은 YYYY-MM-DD이어야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    threads = Thread.objects.annotate(like_count=Count('like_users')).filter(user=user, read_date=date_obj).order_by('-created_at')
    serializer = ThreadListSerializer(threads, many=True, context={ 'request': request })
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def thread_review_analysis(request, thread_id):
    """
    POST: 특정 쓰레드 ID를 받아서 그 content를 기반으로 GPT 감성 분석 수행
    (실제 GPT 호출만 허용, 더미 응답 없음)
    """
    thread = get_object_or_404(Thread, id=thread_id, user=request.user)
    review_text = thread.content

    system_prompt = (
        "너는 사용자의 독후감을 분석하는 감성 분석 리포터야.\n"
        "문체, 주제, 감정 톤을 파악해서\n"
        "‘당신은 이런 스타일의 독서가에요’라는 형식으로 한 문장으로 요약해줘."
    )

    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',  #  실사용 가능 모델로 수정
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"독후감:\n{review_text}"}
            ],
            temperature=0.7,
        )
        summary = response.choices[0].message.content

        #  DB에 저장
        thread.summary = summary
        thread.save()
        return Response({'summary': summary}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def thread_spell_check(request):
    """
    POST: thread content 맞춤법 및 어색한 표현 교정
    요청 데이터: { "content": "오타가 있씁니다." }
    응답 데이터: { "corrected": "오타가 있습니다." }
    """
    original = request.data.get('content')

    if not original:
        return Response({'error': 'content 필드가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # OpenAI GPT 기반 맞춤법 보정
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 사용자의 문장을 자연스럽고 맞춤법에 맞게 고쳐주는 도우미야. "
                        "또한 적절한 접두사 2개와 접미사 2개를 추천해줘. "
                        "다음과 같은 JSON 형식으로 응답해:\n"
                        '{"corrected": "교정된 문장", "prefixes": ["접두1", "접두2"], "suffixes": ["접미1", "접미2"]}'
                    )
                },
                {
                    "role": "user",
                    "content": f"다음 글을 고쳐줘:\n{original}"
                }
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content
        try:
            result = json.loads(content)
            return Response(result, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({'error': 'OpenAI 응답이 JSON이 아닙니다.', 'raw': content}, status=500)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def chatbot_interact(request):
    user = request.user
    if request.method == 'GET':     # 단순 대화 기록을 위한 조회만 실시
        history = user.chatbot_history or []
        return Response({'history': history}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        """
        사용자 입력을 받아 GPT 응답을 생성하고
        기존 기록과 함께 JSONField에 저장
        """
        message = request.data.get('message')

        if not message:
            return Response({'error': 'message가 필요합니다.'}, status=400)

        # GPT 응답 생성
        books = Book.objects.annotate(favorite_count=Count('favorited_by')).all()
        serializer = BookListSerializer(books, many=True, context={'request': request})
        books_data = json.dumps(serializer.data, ensure_ascii=False)
        system_prompt = (
            "너는 책을 정말 좋아하는 사서 AI야. "
            "사용자의 취향을 파악해 아래 제공된 도서 리스트 중 적절한 책을 추천해줘. "
            "리스트에는 제목, 설명, 작가, 카테고리 정보가 포함되어 있어. "
            "카테고리 또는 설명을 바탕으로 사용자의 질문에 가장 적합한 책을 1~3권 정도 추천해줘.\n\n"
            f"도서 목록:\n{books_data}"
        )
        try:
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7
            )
            ai_reply = response.choices[0].message.content

        except Exception as e:
            return Response({'error': str(e)}, status=500)

        # 대화 기록에 append
        chat_entry = {
            'user': message,
            'ai': ai_reply
        }
        history = user.chatbot_history or []  # 기존 기록 불러옴
        history.append(chat_entry)            # 새로운 대화 추가
        user.chatbot_history = history        # 덮어쓰기 (append 된 전체)
        user.save()                           # DB에 저장

        return Response({'reply': ai_reply, 'history': history}, status=status.HTTP_200_OK)

import pickle
import os

# 코사인 유사도 함수
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@api_view(['GET'])
def recommend_similar_books_from_pickle(request, book_id):
    """
    .pkl 파일에서 임베딩 벡터를 불러와 추천 계산
    """
    # 파일 경로
    vec_path = os.path.join("books", "data", "embedding_vectors.pkl")
    id_path = os.path.join("books", "data", "book_ids.pkl")

    # 파일 로드
    with open(vec_path, "rb") as f:
        vectors = pickle.load(f)
    with open(id_path, "rb") as f:
        book_ids = pickle.load(f)

    # 기준 인덱스 찾기
    if book_id not in book_ids:
        return Response({"error": "해당 도서가 book_ids에 존재하지 않습니다."}, status=400)

    idx = book_ids.index(book_id)
    target_vector = vectors[idx]

    # 유사도 계산
    result = []
    for i, vec in enumerate(vectors):
        if i == idx:
            continue
        similarity = cosine_similarity(target_vector, vec)
        b_id = book_ids[i]
        book = Book.objects.get(id=b_id)
        result.append({
            "id": b_id,
            "title": book.title,
            "similarity": round(similarity, 4),
            "cover_image": book.cover_image if book.cover_image else None  #  이 줄만 추가
        })

    # 유사도 순 정렬 후 상위 5개
    result.sort(key=lambda x: x["similarity"], reverse=True)
    return Response(result[:5], status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_books_by_interest(request):
    """
    GET: 로그인한 사용자의 관심 카테고리에 해당하는 도서 추천
    - 요청 헤더: Authorization: Bearer <access>
    - 응답: BookListSerializer[] (최대 20권)
    """
    user = request.user
    categories = user.interested_categories.all()

    if not categories.exists():
        return Response({"detail": "관심 카테고리가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

    books = Book.objects.annotate(favorite_count=Count('favorited_by')).filter(category__in=categories).distinct()[:20]  # 중복 제거 후 20개 제한
    # Serializer 호출 시 context에 request 포함 → favorited 필드 처리를 위함
    serializer = BookListSerializer(books, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def hot_threads(request):
    """
    GET: 좋아요 수가 많은 인기 Thread 리스트 반환 (상위 10개)
    """
    threads = Thread.objects.annotate(
        like_count=Count('like_users')
    ).order_by('-like_count', '-created_at')[:10]

    serializer = ThreadListSerializer(threads, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def youtube_video_search(request):
    query = request.GET.get('query')
    if not query:
        return Response({'error': 'query 파라미터가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'key': settings.YOUTUBE_API_KEY,
        'maxResults': 1,
    }

    r = requests.get(url, params=params)
    data = r.json()
    if r.status_code != 200:
        return Response({'error': 'YouTube API 호출 실패', 'details': r.json()}, status=r.status_code)
    if 'items' in data and data['items']:
        video_id = data['items'][0]['id']['videoId']
        print(video_id)
        return Response({'videoId': video_id}, status=status.HTTP_200_OK)
    else:
        return Response({'error': '적절한 영상이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)