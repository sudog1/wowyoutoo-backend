import csv
from django.core.management.base import BaseCommand
from english.models import Word


class Command(BaseCommand):
    help = "Import data from a CSV file"

    # 인자 "csv_file"을 받음
    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file to import")

    # 실제로 command가 실행되는 부분
    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        data_to_insert = []

        # csv파일을 데이터베이스로 저장
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data_to_insert.append(Word(term=row[0], meaning=row[1]))
                if len(data_to_insert) >= 100:
                    # 효율을 위해 bulk_create사용
                    Word.objects.bulk_create(
                        data_to_insert, batch_size=len(data_to_insert)
                    )
                    data_to_insert = []
            if data_to_insert:
                Word.objects.bulk_create(data_to_insert, batch_size=len(data_to_insert))
