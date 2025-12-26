"""Утилита для отображения прогресс-бара"""

def get_progress_bar(current, total, length=20):
    if total == 0:
        return '[нет данных]'
    percent = current / total
    fill = int(percent * length)
    bar = '█' * fill + '-' * (length - fill)
    return f"[{bar}] {int(percent * 100)}%"
