from django.core.management.base import BaseCommand
from books.models import Book
from openai import OpenAI
import pickle
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Command(BaseCommand):
    help = "책 설명을 임베딩하고 embedding_vectors.pkl로 저장"

    def handle(self, *args, **kwargs):
        books = Book.objects.all()
        texts = [book.description for book in books if book.description]

        if not texts:
            self.stdout.write(self.style.WARNING("책 설명이 없습니다."))
            return

        # OpenAI Embedding 호출
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )

        # 벡터 추출
        vectors = [item.embedding for item in response.data]

        # 저장 경로 지정 (books/data 폴더 사용)
        output_path = os.path.join("books", "data", "embedding_vectors.pkl")
        with open(output_path, "wb") as f:
            pickle.dump(vectors, f)

        self.stdout.write(self.style.SUCCESS(f" 저장 완료: {output_path}"))
