import itertools
from tqdm import tqdm
import os

def generate_combinations(
    charset: str,
    min_length: int = 1,
    max_length: int = 5,
    output_file: str = "combinations.txt",
    buffer_size: int = 100_000,
):
    """
    Генерирует комбинации без сокращений и проверяет размер.
    """
    total_combinations = sum(len(charset) ** length for length in range(min_length, max_length + 1))
    print(f"Всего комбинаций: {total_combinations:,}")
    
    estimated_size = total_combinations * (max_length + 1)  # +1 для '\n'
    print(f"Примерный размер файла: {estimated_size / (1024**3):.2f} ГБ")
    
    if input("Продолжить? (y/n): ").lower() != 'y':
        return

    with open(output_file, 'w', encoding='utf-8') as f:
        for length in range(min_length, max_length + 1):
            print(f"\nДлина {length}: {len(charset) ** length:,} комбинаций")
            buffer = []
            
            for combo in tqdm(itertools.product(charset, repeat=length), 
                             desc=f"Length {length}", unit="comb"):
                buffer.append(''.join(combo) + '\n')
                
                if len(buffer) >= buffer_size:
                    f.writelines(buffer)
                    buffer.clear()
            
            if buffer:
                f.writelines(buffer)
    
    print(f"Файл сохранен: {output_file}")
    print(f"Реальный размер: {os.path.getsize(output_file) / (1024**3):.2f} ГБ")

if __name__ == "__main__":
    chars = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        "0123456789"
        "!@#$%^&*()_+-=[]{}|;:,.<>?"
    )
    
    generate_combinations(
        charset=chars,
        min_length=1,
        max_length=5,  # Осторожно! 492 ГБ+
        output_file="full_combinations.txt",
    )