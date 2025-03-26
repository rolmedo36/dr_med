# import_books.py
import csv
from datetime import datetime
from models import CodigoPostal  # Replace 'myapp' with your actual app name


def import_books(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            CodigoPostal.objects.create(
                ciudad=row['ciudad'],
                codigo_postal=row['CP'],
                estado=row['estado'],
                municipio=row['municipio'],
                colonia=row['colonia'],
            )


if __name__ == '__main__':
    csv_file_path = 'CP.csv'  # Replace with your actual file path
    import_books(csv_file_path)
