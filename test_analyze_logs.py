import pytest
from analyze_logs import analyze_logs

def test_basic_logic(tmp_path):
    log_file = tmp_path / "basic_logs.txt"
    
    log_file.write_text(
        "2026-10-05 14:23:01 INFO User 42 logged in\n"
        "2026-10-05 14:23:05 ERROR User 42 failed to upload file report.pdf\n"
        "2026-10-05 14:23:10 INFO User 43 logged in\n"
        "2026-10-05 14:23:15 WARNING User 42 session timeout\n"
        "2026-10-05 14:23:20 ERROR User 44 database connection failed\n",
        encoding="utf-8"
    )
    result = analyze_logs(str(log_file))
    assert result == {'INFO': 2, 'ERROR': 2, 'WARNING': 1}
    
def test_empty_file(tmp_path):
    log_file = tmp_path / "empty_logs.txt"
    
    log_file.write_text("",
        encoding="utf-8"
    )
    result = analyze_logs(str(log_file))
    assert result == {}
    
def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        analyze_logs("Nonexistent_logs.txt")
        
def test_garbage_line_ignored(tmp_path):
    log_file = tmp_path / "garbage_logs.txt"
    
    log_file.write_text(
        "2026-10-05 14:23:01 User 42 logged in\n" # garbage string
        "2026-10-05 14:23:05 ERROR User 42 failed to upload file report.pdf\n"
        "\n"  # empty string must be ignored
        "garbage string\n"
        "2026-10-05 14:23:20 ERROR User 44 database connection failed\n"
        "\n",  # empty string must be ignored
        encoding="utf-8"
    )
    result = analyze_logs(str(log_file))
    assert result == {"ERROR": 2}
    