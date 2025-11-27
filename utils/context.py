"""Хранилище контекста пользователя"""

user_context = {}

def set_user_tour(user_id, tour_id):
    """Сохранить, какой тур пополняет пользователь"""
    user_context[user_id] = tour_id

def get_user_tour(user_id):
    """Получить текущий тур пользователя"""
    return user_context.get(user_id)

def clear_user_tour(user_id):
    """Очистить контекст"""
    if user_id in user_context:
        del user_context[user_id]
