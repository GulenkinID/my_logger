import re


pattern = re.compile(r'\b(INFO|ERROR|WARNING)\b')

def analyze_logs(file_path: str) -> dict:
    type_log_counter = {}
    
    with open(file_path, 'r', encoding='utf-8') as log_file:
        
        for line in log_file:
            match = pattern.search(line)
            if match:
                log_type = match.group(1)
                type_log_counter[log_type] = type_log_counter.get(log_type, 0) + 1
                    
                     
    return type_log_counter
