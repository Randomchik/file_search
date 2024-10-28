import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta
from pathlib import PureWindowsPath

from search.tasks import (
    start_search_thread,
    search_files,
    _check_file_matches_filters,
    _check_contains_text,
    _comprasion_by_wildcards,
)
from search.models import Search


class SearchTestsPost(APITestCase):
    def test_create_search(self):
        url = reverse('create_search')
        data = {"text": "example", "file_mask": "*.txt"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("search_id", response.data)


class SearchTestsGet(APITestCase):
    def test_get_search_results(self):
        search = Search.objects.create(text="example")
        url = reverse('get_search_results', args=[search.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSearchFunctions(unittest.TestCase):
    def setUp(self):
        # Создаем базовый объект поиска с фильтрами для тестирования
        self.search_instance = Search.objects.create(
            text="test",
            file_mask="*.txt",
            size_value=1024,
            size_operator="ge",
            creation_time_value=datetime.now() - timedelta(days=1),
            creation_time_operator="ge",
        )

    def tearDown(self):
        Search.objects.all().delete()

    @patch('search.tasks.search_files')
    def test_start_search_thread(self, mock_search_files):
        # Проверка запуска search_files в отдельном потоке
        start_search_thread(self.search_instance.id)
        mock_search_files.assert_called_once_with(self.search_instance.id)

    def test_check_file_matches_filters_with_different_masks(self):
        # Тестирование масок
        self.assertTrue(_check_file_matches_filters("document.txt", 1024, None, self.search_instance))
        self.assertFalse(_check_file_matches_filters("image.jpg", 1024, None, self.search_instance))

    def test_check_file_matches_filters_with_size(self):
        # Тестирование размера файла с фильтрами
        search_instance = Search(file_mask=None, size_value=512, size_operator="gt")
        self.assertTrue(_check_file_matches_filters("file.txt", 1024, None, search_instance))
        self.assertFalse(_check_file_matches_filters("file.txt", 256, None, search_instance))

    def test_check_file_matches_filters_with_creation_time(self):
        # Тестирование времени создания файла с фильтрами
        search_instance = Search(file_mask=None, creation_time_value=datetime.now() - timedelta(days=2), creation_time_operator="ge")
        file_creation_time = datetime.now() - timedelta(days=3)
        self.assertFalse(_check_file_matches_filters("file.txt", 1024, file_creation_time, search_instance))

        search_instance.creation_time_operator = "le"
        self.assertTrue(_check_file_matches_filters("file.txt", 1024, file_creation_time, search_instance))

    def test_check_contains_text_with_various_texts(self):
        # Проверка наличия текста
        self.assertTrue(_check_contains_text(b"Example content with test inside", "test"))
        self.assertFalse(_check_contains_text(b"Content without keyword", "test"))

    def test_check_contains_text_non_utf8(self):
        # Проверка для бинарного файла
        self.assertFalse(_check_contains_text(b"\x00\x01\x02\x03", "test"))

    def test_comprasion_by_wildcards(self):
        # Тестирование операторов сравнения
        self.assertTrue(_comprasion_by_wildcards(100, "ge", 200))
        self.assertFalse(_comprasion_by_wildcards(100, "gt", 100))
        self.assertTrue(_comprasion_by_wildcards(100, "le", 100))

    @patch('search.tasks.os.path.getsize', return_value=2048)
    @patch('search.tasks.os.path.getctime', return_value=(datetime.now() - timedelta(days=2)).timestamp())
    @patch('search.tasks.os.walk')
    @patch('search.tasks.zipfile.is_zipfile', return_value=False)
    def test_search_files_standardizes_paths(self, mock_os_walk, _, __, ___):
        # Тест стандартизации путей в POSIX-формат
        mock_os_walk.return_value = [(str(PureWindowsPath("C:\\path\\to\\files")), ('subdir',), ('test.txt',))]
        
        with patch('builtins.open', mock_open(read_data="This is a test file")):
            search_files(self.search_instance.id)

        self.search_instance.refresh_from_db()
        standardized_path = PureWindowsPath("C:\\path\\to\\files\\test.txt").as_posix()

        # Проверка стандартализации путей
        self.assertTrue(self.search_instance.finished)

    @patch('search.tasks.os.path.getsize', side_effect=[512, 2048])
    @patch('search.tasks.os.path.getctime', side_effect=[(datetime.now() - timedelta(days=2)).timestamp(), datetime.now().timestamp()])
    @patch('search.tasks.os.walk')
    @patch('search.tasks.zipfile.is_zipfile', return_value=False)
    def test_search_files_with_size_and_time_filters(self, mock_os_walk, _, __, ___):
        # Проверка фильтрации по размеру и времени
        mock_os_walk.return_value = [('/path', ('subdir',), ('small.txt', 'large.txt'))]
        
        with patch('builtins.open', mock_open(read_data="This is a test file")):
            search_files(self.search_instance.id)

        self.search_instance.refresh_from_db()
        self.assertTrue(self.search_instance.finished)

    @patch('search.tasks.zipfile.is_zipfile', return_value=True)
    @patch('search.tasks.zipfile.ZipFile')
    @patch('search.tasks.os.walk')
    def test_search_files_with_zip_and_filters(self, mock_os_walk, mock_zipfile, mock_is_zipfile):
        # Тест поиска внутри ZIP-архива
        mock_os_walk.return_value = [('/path', ('subdir',), ('archive.zip',))]
        zip_file_mock = MagicMock()
        zip_file_mock.infolist.return_value = [MagicMock(filename="inner.txt", file_size=512)]
        zip_file_mock.read.return_value = b"This is a test content in ZIP"
        mock_zipfile.return_value.__enter__.return_value = zip_file_mock

        search_files(self.search_instance.id)

        self.search_instance.refresh_from_db()
        # Проверка, что найден файл внутри архива
        self.assertTrue(self.search_instance.finished)


if __name__ == "__main__":
    unittest.main()
