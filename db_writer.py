import re
import psycopg2
from config import DB_CONFIG
# Параметры подключения к базе



pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(INFO|ERROR|WARNING)\s+(.+)$')

def parse_log_file(path_file: str) -> list[tuple]:
    
    log_list = []
    
    with open(path_file, 'r', encoding="utf-8") as log_file:
        for line in log_file:
            
            cur_line = pattern.search(line)
            
            if cur_line:
                log_list.append((
                    cur_line.group(1),
                    cur_line.group(2),
                    cur_line.group(3)
                ))
            
    return log_list

# print(parse_log_file("logs.txt"))

def save_to_db(records: list[tuple]) -> None:
    
    
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO logs (log_date, log_level, message) VALUES (%s, %s, %s)",
                records
            )
            
            
if __name__ == "__main__":
    records = parse_log_file("logs.txt")
    save_to_db(records)
    print(f"Сохранено {len(records)} записей!")
            
        