import os
import zipfile
from threading import Thread
from datetime import datetime
from fnmatch import fnmatch  
from django.conf import settings
from pathlib import PureWindowsPath

from .models import Search


def start_search_thread(search_id):
    """
    Функция для запуска задачи поиска в отдельном потоке.
    """
    thread = Thread(target=search_files, args=(search_id,))
    thread.start()


def search_files(search_id):
    search = Search.objects.get(id=search_id)
    search_dir = settings.SEARCH_DIRECTORY
    results = []
    # print(glob('**/*', recursiverecursive=True))

    for root, _, files in os.walk(search_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Будем проверять отдельно архивы
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, 'r') as zip_file:
                    for zip_info in zip_file.infolist():
                          # Применяем фильтры для файлов в архиве
                        if not _check_file_matches_filters(
                            zip_info.filename,
                            zip_info.file_size,
                            None,  # Время создания недоступно для файлов в архиве
                            search
                        ):
                            continue

                        if not _check_contains_text(zip_file.read(zip_info.filename), search.text):
                            continue
                        results.append(f"{file_path}/{zip_info.filename}")
                continue

            # Применяем фильтры для обычного файла
            file_size = os.path.getsize(file_path)
            file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if not _check_file_matches_filters(file_name, file_size, file_creation_time, search):
                continue

            # Поиск текста в файле
            if search.text:
                with open(file_path, "rb") as file:
                    if not _check_contains_text(file.read(), search.text):
                        continue

            results.append(file_path)


    # Стандартизируем под posix формат
    if os.path.sep == '\\':
        results = [PureWindowsPath(path).as_posix() for path in results]

    search.results = results
    search.finished = True
    search.save()


def _check_file_matches_filters(file_name, file_size, file_creation_time, search):
    """
    Проверяет, удовлетворяет ли файл заданным фильтрам поиска.
    """
    # Проверка маски имени файла
    if search.file_mask and not fnmatch(file_name, search.file_mask):
        return False

    # Проверка размера файла
    if search.size_value and not __comprasion_by_wildcards(search.size_value, search.size_operator, file_size):
        return False

    # Проверка времени создания файла
    if search.creation_time_value and file_creation_time:
        if not __comprasion_by_wildcards(search.creation_time_value, search.creation_time_operator, file_creation_time):
            return False

    return True


def _check_contains_text(file_content, search_text):
    """
    Проверяет, содержит ли содержимое файла указанный текст.
    """
    if search_text:
        try:
            content = file_content.decode("utf-8", errors="ignore")
            return search_text in content
        except:
            return False  # Если файл не является текстовым
    return True


def __comprasion_by_wildcards(border_value, operator, value):
    operators = {
        "eq": value == border_value,
        "gt": value > border_value,
        "lt": value < border_value,
        "ge": value >= border_value,
        "le": value <= border_value,
    }
    return operators.get(operator, True)
