import os
import sys
import glob
import subprocess
from pathlib import Path

def main():
    models = ['lama3.3', 'deepseek-r1', 'codellama']

    print("Доступные модели:")
    for idx, model in enumerate(models):
        print(f"{idx + 1}. {model}")

    choice = input("Выберите модель (введите номер): ")
    try:
        model_choice = models[int(choice) - 1]
    except Exception as e:
        print("Неверный выбор. Завершаем работу.")
        sys.exit(1)

    # prompt_folder = os.path.join("promts", model_choice)
    prompt_folder = Path("promts/notOptimized")
    if not os.path.exists(prompt_folder):
        print(f"Папка с промтами для модели '{model_choice}' не найдена: {prompt_folder}")
        sys.exit(1)

    response_folder = os.path.join("response", model_choice)
    os.makedirs(response_folder, exist_ok=True)

    prompt_files = glob.glob(os.path.join(prompt_folder, "*"))
    if not prompt_files:
        print(f"В папке '{prompt_folder}' не найдено промтов.")
        sys.exit(1)

    for prompt_file in prompt_files:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_text = f.read()

        print(f"\nОтправка промта из файла '{prompt_file}' для модели '{model_choice}'...")

        try:
            result = subprocess.run(
                ["ollama", "run", model_choice],
                input=prompt_text.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            response_text = result.stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode('utf-8')
            print(f"Ошибка при выполнении команды для файла '{prompt_file}':\n{error_msg}")
            continue

        # Формирование имени файла для сохранения ответа
        base_name = os.path.basename(prompt_file)[:-10]
        response_file = os.path.join(response_folder, base_name + "Text")

        with open(response_file, 'w', encoding='utf-8') as f:
            f.write(response_text)
        print(f"Ответ сохранён в файл: '{response_file}'")


if __name__ == "__main__":
    main()
