from database.models import (
    make_booking, 
    get_progress, 
    get_balance, 
    get_tour_by_id, 
    get_user
)
from utils.keyboard import main_menu
from utils.progress import get_progress_bar

def register(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("book_"))
    def handle_book_tour(call):
        tour_id = int(call.data.split("_")[1])
        user_id = call.from_user.id
        
        tour = get_tour_by_id(tour_id)
        balance = get_balance(user_id)
        progress = get_progress(user_id, tour_id)
        user = get_user(user_id)
        
        print(f"[DEBUG] book_: tour_id={tour_id}, balance={balance}, progress={progress}, price={tour['price']}")
        
        # == Проверяем достаточно ли накоплено ==
        if progress >= tour['price']:
            # == Проверяем есть ли email ==
            if not user['email']:
                bot.answer_callback_query(call.id, "❌ Добавьте email для бронирования!", show_alert=True)
                return
            
            # == Вычитаем стоимость тура из прогресса ==
            make_booking(user_id, tour_id)
            text = f"""
✅ <b>Тур забронирован!</b>

🎉 {tour['name']} ваш!
📧 Подтверждение отправлено на: {user['email']}
🌍 Тур: {tour['name']}
💰 Стоимость: {tour['price']}₽
⏱️ Продолжительность: {tour['duration_days']} дней
            """
            bot.edit_message_text(text, user_id, call.message.message_id, 
                                 parse_mode="HTML", reply_markup=main_menu())
        else:
            # == Недостаточно накоплено ==
            needed = tour['price'] - progress
            text = f"""
⏳ <b>Недостаточно накопленных средств</b>

🌍 Тур: {tour['name']}
💰 Цена: {tour['price']}₽
📊 Накоплено: {get_progress_bar(int(progress), int(tour['price']))}
❌ Не хватает: {needed}₽

Пополните баланс для завершения бронирования.
            """
            bot.edit_message_text(text, user_id, call.message.message_id, 
                                 parse_mode="HTML", reply_markup=main_menu())
        
        bot.answer_callback_query(call.id)
