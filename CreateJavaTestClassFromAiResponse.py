import re
from pathlib import Path

def main():
# Путь к файлу с ответом модели
    response_file_path = Path("response/deepseek")

    # Чтение содержимого файла
    try:
        with response_file_path.open("r", encoding="utf-8") as rf:
            content = rf.read()
    except Exception as e:
        print(f"Ошибка чтения файла {response_file_path}: {e}")
        exit(1)

    # Попытка извлечь имя тестового класса из строки "public class <ИмяКласса>"
    match = re.search(r"public\s+class\s+(\w+)", content)
    if match:
        test_class_name = match.group(1)
    else:
        print("Не удалось определить имя тестового класса. Использую 'TestClass' по умолчанию.")
        test_class_name = "TestClass"

    # Формирование пути для сохранения java файла
    output_dir = Path("generated/tests")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file_path = output_dir / f"{test_class_name}.java"

    # Сохранение содержимого в java файл
    try:
        with output_file_path.open("w", encoding="utf-8") as wf:
            wf.write(content)
        print(f"Содержимое сохранено в {output_file_path}")
    except Exception as e:
        print(f"Ошибка записи файла {output_file_path}: {e}")

if __name__ == "__main__":
    main()
