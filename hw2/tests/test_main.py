# Импортируем класс PackageAnalyzer
from hw2.src.command_line_graphs import PackageAnalyzer
import sys
import os
import shutil
sys.path.insert(0, '.')  # Указываем путь к основному файлу с нашим кодом

def test_get_dependencies():
    analyzer = PackageAnalyzer('requests', max_depth=2)
    dependencies = analyzer._get_dependencies('requests', 2)
    assert len(dependencies) >= 1
    assert 'urllib3<3,>=1.21.1' in dependencies
    assert 'certifi>=2017.4.17' in dependencies



def test_create_graph():
    os.chdir(os.path.dirname(__file__))

    analyzer = PackageAnalyzer('requests', max_depth=2, output_file='./result.dot')
    analyzer.analyze_package()
    with open('result.dot', 'r') as f:
        content = f.read()
        assert 'digraph' in content
        assert 'requests' in content
        assert 'certifi' in content
        assert 'urllib3' in content


def test_invalid_package():
    analyzer = PackageAnalyzer('nonexistent_package', max_depth=2)
    try:
        analyzer._get_dependencies('nonexistent_package', 2)
        assert False, "Не должно быть возможности получить зависимости для несуществующего пакета."
    except ValueError as e:
        assert "Пакет nonexistent_package не найден." in str(e)

def test_max_depth():
    analyzer = PackageAnalyzer('requests', max_depth=1)
    dependencies = analyzer._get_dependencies('requests', 1)
    assert len(dependencies) >= 1
    assert 'certifi>=2017.4.17' in dependencies
    assert 'urllib3<3,>=1.21.1' in dependencies

def test_output_file_not_found():
    analyzer = PackageAnalyzer('requests', max_depth=2, output_file='/invalid/path/result.dot')
    directory = os.path.dirname('/invalid/path/result.dot')
    if os.path.exists(directory):
        shutil.rmtree(directory)  # Удаление директории, если она вдруг существует
    try:
        analyzer.analyze_package()
        assert False, "Должно возникнуть исключение, если файл не найден."
    except FileNotFoundError as e:
        assert "Директория /invalid/path не найдена." in str(e)

def test_empty_package():
    analyzer = PackageAnalyzer('', max_depth=2)
    dependencies = analyzer._get_dependencies('', 2)

    assert len(dependencies) == 0