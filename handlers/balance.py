from database.models import update_balance, get_balance, add_progress
from utils.keyboard import main_menu
from utils.context import get_user_tour, clear_user_tour

def register(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("add_balance_"))
    def handle_add_balance(call):
        amount = int(call.data.split("_")[2])
        user_id = call.from_user.id
        
        # == Сначала пополнение ==
        update_balance(user_id, amount)
        new_balance = get_balance(user_id)
        
        # == Получаем тур, который пополняется ==
        tour_id = get_user_tour(user_id)
        
        if tour_id:
            # == Перевод ВСЕХ средств баланса в прогресс ==
            add_progress(user_id, tour_id, new_balance)
            
            # == После перевода в прогресс обнуляем баланс ==
            update_balance(user_id, -new_balance)
            
            clear_user_tour(user_id)
            
            from database.models import get_tour_by_id, get_progress
            from utils.progress import get_progress_bar
            
            tour = get_tour_by_id(tour_id)
            progress = get_progress(user_id, tour_id)
            bar = get_progress_bar(int(progress), int(tour['price']))
            current_balance = get_balance(user_id)
            
            text = f"""
✅ <b>Средства переведены в прогресс!</b>

🌍 Тур: {tour['name']}
💰 Цена: {tour['price']}₽
💵 Ваш баланс: {current_balance}₽
📊 Прогресс: {bar}

{'🎉 Готово к бронированию!' if progress >= tour['price'] else 'Продолжайте пополнять...'}
            """
        else:
            # == Пополнение из основного меню (без привязки к туру) ==
            text = f"✅ Баланс пополнен на {amount}₽\n💰 Новый баланс: {new_balance}₽"
        
        bot.edit_message_text(
            text,
            user_id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=main_menu()
        )
        bot.answer_callback_query(call.id)
