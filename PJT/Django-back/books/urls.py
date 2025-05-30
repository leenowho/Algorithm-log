from django.urls import path
from . import views

urlpatterns = [
    # book
    path('books/', views.books),
    path('books/<int:book_id>/', views.book_detail),  #  GET /books/3/
    path('books/<int:book_id>/recommend-pickle/', views.recommend_similar_books_from_pickle),
    path('books/recommend-interest/', views.recommend_books_by_interest),
    path('books/favorites/', views.my_favorite_books),  # 유저가 좋아하는 책 목록 반환
    path('books/<int:book_id>/favorite/', views.toggle_favorite_book),

    # thread
    path('books/<int:book_id>/threads/', views.create_thread),  # Thread 생성
    path('threads/', views.thread_list),
    path('threads/<int:thread_id>/', views.thread_detail),
    path('threads/<int:thread_id>/like/', views.thread_like_toggle),
    path('threads/calendar/', views.reading_calendar),  #  읽은 날짜별 Thread 개수 집계
    path('threads/by-date/', views.threads_by_date), #날짜별 읽은 Thread 목록 조회 (쿼리 파라미터: ?date=YYYY-MM-DD)
    path('threads/<int:thread_id>/analyze/', views.thread_review_analysis),  # GPT 감성 분석
    path('threads/spell-check/', views.thread_spell_check),
    path('threads/hot/', views.hot_threads),

    
    # comment
    path('threads/<int:thread_id>/comments/', views.comment_list_create),
    path('comments/<int:comment_id>/', views.comment_delete),

    path('categories/', views.category_list),   # app.vue가 mounted 될때만 호출, 그 이외에는 불필요(변화가 없기 때문)
    # path('books/<int:book_id>/recommend/', views.recommend_similar_books),  #유사도
    path('chatbot/', views.chatbot_interact), #챗봇
    path('youtube/', views.youtube_video_search),




]
