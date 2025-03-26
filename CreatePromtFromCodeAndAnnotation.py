import os
from pathlib import Path

def main():
    # Директория с Java-кодом
    base_dir = Path("javaProjects/ToPromtCode/main/java/backend/academy/bot/")
    save_dir = Path("promts/notOptimized")

    # Проходим рекурсивно по всем .java файлам в указанной директории
    for java_file in base_dir.rglob("*.java"):
        try:
            with java_file.open("r", encoding="utf-8") as jf:
                java_code = jf.read()
        except Exception as e:
            print(f"Ошибка чтения {java_file}: {e}")
            continue

        # Определяем имя Java-класса (из названия файла без расширения)
        class_name = java_file.stem

        # Ищем описание – одноимённый .txt файл в той же папке
        description_file = java_file.with_suffix(".txt")
        description = ""
        if description_file.exists():
            try:
                with description_file.open("r", encoding="utf-8") as df:
                    description = df.read().strip()
            except Exception as e:
                print(f"Ошибка чтения {description_file}: {e}")

        # Формируем промт по заданному формату
        prompt_content = (
            f"Задача: Проанализируй следующий Java-код. Напиши на него JUnit тесты. "
            f"Каждый тест должен иметь название <ИмяМетода>_Where<условие>_Then<ожидание>. Ответом должен быть просто Java Test class без лишнего текста.\n\n"
            f"Описание кода: {description}\n\n"
            f"Код:\n\n"
            f"--- Начало кода ---\n"
            f"{java_code}\n\n"
            f"--- Конец кода ---\n"
        )

        # Определяем путь для сохранения промта
        prompt_filename = save_dir / f"{class_name}_Promt.txt"

        try:
            with prompt_filename.open("w", encoding="utf-8") as pf:
                pf.write(prompt_content)
            print(f"Промт сохранён: {prompt_filename}")
        except Exception as e:
            print(f"Ошибка записи в файл {prompt_filename}: {e}")

if __name__ == "__main__":
    main()
