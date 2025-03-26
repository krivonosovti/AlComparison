# Идея - запустить mvn test и пропарсить ответ, собрать все полученные данные о тестах и сохранить их таблицы
import subprocess
import re
import csv


def run_mvn_tests():
    """
    Запускает mvn test и парсит результат.
    """
    try:
        result = subprocess.run(["mvn", "test"], capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = e.stdout + "\n" + e.stderr  # Объединяем stdout и stderr в случае ошибки

    return output


def parse_mvn_output(output):
    """
    Извлекает статистику из вывода mvn test.
    """
    stats = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "skipped": 0,
        "time": 0.0
    }

    # Парсим строку с общей статистикой, например:
    # "Tests run: 10, Failures: 2, Errors: 1, Skipped: 0, Time elapsed: 5.678 sec"
    match = re.search(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+), Time elapsed: ([\d\.]+) sec",
                      output)
    if match:
        stats["total"] = int(match.group(1))
        stats["failed"] = int(match.group(2))
        stats["errors"] = int(match.group(3))
        stats["skipped"] = int(match.group(4))
        stats["time"] = float(match.group(5))
        stats["passed"] = stats["total"] - stats["failed"] - stats["errors"]

    return stats


def save_results_to_csv(stats, filename="test_results.csv"):
    """
    Сохраняет результаты в CSV-файл.
    """
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [stats["total"], stats["passed"], stats["failed"], stats["errors"], stats["skipped"], stats["time"]])


def main():
    print("Запуск mvn test...")
    output = run_mvn_tests()
    stats = parse_mvn_output(output)
    print("Результаты тестов:", stats)
    save_results_to_csv(stats)
    print("Данные сохранены в test_results.csv")


if __name__ == "__main__":
    main()
