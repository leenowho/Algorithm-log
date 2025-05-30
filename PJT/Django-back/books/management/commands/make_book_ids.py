from django.core.management.base import BaseCommand
from books.models import Book
import pickle
import os

class Command(BaseCommand):
    help = "책 ID 리스트를 book_ids.pkl 파일로 저장"

    def handle(self, *args, **kwargs):
        ids = list(Book.objects.values_list("id", flat=True))

        output_path = os.path.join("books", "data", "book_ids.pkl")
        with open(output_path, "wb") as f:
            pickle.dump(ids, f)

        self.stdout.write(self.style.SUCCESS(f" 저장 완료: {output_path}"))
