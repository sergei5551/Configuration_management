import pkg_resources
from graphviz import Digraph
import argparse
import os



class PackageAnalyzer:
    def __init__(self, package_name, max_depth=1, output_file=None):
        self.package_name = package_name
        self.max_depth = max_depth
        self.output_file = output_file
        self.visited_packages = set()
        self.dot = Digraph(comment=f'Граф зависимостей для {package_name}')


    def _get_dependencies(self, package_name, depth):
        if not package_name:
            return []
        if depth == 0:
            return []
        dependencies = []
        try:
            package = pkg_resources.get_distribution(package_name)
        except pkg_resources.DistributionNotFound as e:
            raise ValueError(f"Пакет {package_name} не найден.") from e

        for requirement in package.requires():
            dependency = str(requirement)
            dependencies.append(dependency)

            # Рекурсивный вызов для получения зависимостей текущей зависимости
            sub_dependencies = self._get_dependencies(dependency, depth - 1)
            dependencies.extend(sub_dependencies)

        return list(set(dependencies))  # Убираем дубликаты

    def _add_node_and_edges(self, package, depth):
        if package not in self.visited_packages:
            self.visited_packages.add(package)

            if depth > 0:
                dependencies = self._get_dependencies(package, depth)

                for dep in dependencies:
                    self.dot.edge(package, dep)
                    self._add_node_and_edges(dep, depth - 1)

    def analyze_package(self):
        self._add_node_and_edges(self.package_name, self.max_depth)

        if self.output_file is None:
            print(self.dot.source)
        else:
            # Создаём директорию, если она не существует
            directory = os.path.dirname(self.output_file)

            # Проверка существования директории
            if not os.path.exists(directory):
                raise FileNotFoundError(f"Директория {directory} не найдена.")

            # Создание директории
            os.makedirs(directory, exist_ok=True)

            with open(self.output_file, 'w') as f:
                f.write(self.dot.source)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Инструмент для визуализации графа зависимостей.')
    parser.add_argument('package', help='Имя анализируемого пакета')
    parser.add_argument('-o', '--output-file', help='Путь к файлу-результату в виде кода')
    parser.add_argument('-d', '--max-depth', type=int, default=1, help='Максимальная глубина анализа зависимостей')
    args = parser.parse_args()

    analyzer = PackageAnalyzer(args.package, args.max_depth, args.output_file)
    try:
        analyzer.analyze_package()
    except Exception as e:
        print(f"Произошла ошибка: {e}")