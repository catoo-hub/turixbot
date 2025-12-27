def register(bot):
    # == Просмотр туров (Пагинация) ==
    @bot.callback_query_handler(func=lambda call: call.data.startswith("tours_page_"))
    def handle_tours_pagination(call):
        try:
            page = int(call.data.split("_")[2])
            show_tours_page(bot, call.from_user.id, page, message_id=call.message.message_id)
        except (ValueError, IndexError) as e:
            print(f"[ERROR] Ошибка в tours_page: {e}, data={call.data}")
            bot.answer_callback_query(call.id, "❌ Ошибка")
            return
        bot.answer_callback_query(call.id)
    
    # == Просмотр деталей тура ==
    @bot.callback_query_handler(func=lambda call: call.data.startswith("tour_detail_"))
    def handle_tour_detail(call):
        from database.models import get_tour_by_id, is_favorite, get_progress
        from utils.keyboard import tour_detail_keyboard
        from utils.progress import get_progress_bar
        
        try:
            tour_id = int(call.data.split("_")[2])
            print(f"[DEBUG] tour_detail нажат, tour_id={tour_id}")
        except (ValueError, IndexError) as e:
            print(f"[ERROR] Ошибка парсинга tour_detail: {e}, data={call.data}")
            bot.answer_callback_query(call.id, "❌ Ошибка")
            return
        
        tour = get_tour_by_id(tour_id)
        
        if not tour:
            bot.answer_callback_query(call.id, "❌ Тур не найден")
            return
        
        is_fav = is_favorite(call.from_user.id, tour_id)
        progress = get_progress(call.from_user.id, tour_id)
        bar = get_progress_bar(int(progress), int(tour['price']))
        
        if is_fav:
            text = f"""
🌍 <b>{tour['name']}</b>

📝 {tour['description']}

💰 Цена: <b>{tour['price']}₽</b>
⏱️ Продолжительность: <b>{tour['duration_days']} дней</b>

⭐ <b>В избранном!</b>
📊 Прогресс накопления: {bar}
            """
        else:
            text = f"""
🌍 <b>{tour['name']}</b>

📝 {tour['description']}

💰 Цена: <b>{tour['price']}₽</b>
⏱️ Продолжительность: <b>{tour['duration_days']} дней</b>
            """
        
        bot.edit_message_text(
            text,
            call.from_user.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=tour_detail_keyboard(tour_id)
        )
        bot.answer_callback_query(call.id)
    
    # == Добавление/удаление из избранного ==
    @bot.callback_query_handler(func=lambda call: call.data.startswith("add_fav_"))
    def handle_add_favorite(call):
        from database.models import add_favorite, remove_favorite, is_favorite, get_tour_by_id, get_progress
        from utils.keyboard import tour_detail_keyboard
        from utils.progress import get_progress_bar
        
        try:
            tour_id = int(call.data.split("_")[2])
        except (ValueError, IndexError) as e:
            print(f"[ERROR] Ошибка в add_fav: {e}, data={call.data}")
            bot.answer_callback_query(call.id, "❌ Ошибка")
            return
        
        user_id = call.from_user.id
        
        if is_favorite(user_id, tour_id):
            remove_favorite(user_id, tour_id)
            bot.answer_callback_query(call.id, "❌ Удалено из избранного")
        else:
            if add_favorite(user_id, tour_id):
                bot.answer_callback_query(call.id, "✅ Добавлено в избранное!")
            else:
                bot.answer_callback_query(call.id, "⚠️ Уже в избранном")
        
        tour = get_tour_by_id(tour_id)
        is_fav = is_favorite(user_id, tour_id)
        progress = get_progress(user_id, tour_id)
        bar = get_progress_bar(int(progress), int(tour['price']))
        
        if is_fav:
            text = f"""
🌍 <b>{tour['name']}</b>

📝 {tour['description']}

💰 Цена: <b>{tour['price']}₽</b>
⏱️ Продолжительность: <b>{tour['duration_days']} дней</b>

⭐ <b>В избранном!</b>
📊 Прогресс накопления: {bar}
            """
        else:
            text = f"""
🌍 <b>{tour['name']}</b>

📝 {tour['description']}

💰 Цена: <b>{tour['price']}₽</b>
⏱️ Продолжительность: <b>{tour['duration_days']} дней</b>
            """
        
        bot.edit_message_text(
            text,
            user_id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=tour_detail_keyboard(tour_id)
        )

# == Функция отображения страницы туров ==
def show_tours_page(bot, user_id, page, message_id=None):
    from database.models import get_tours
    from utils.keyboard import tours_pagination_keyboard
    import telebot
    
    tours, total_pages = get_tours(page=page, per_page=3)
    
    if not tours:
        text = "❌ Туры не найдены"
    else:
        text = f"🌏 <b>Доступные туры (Страница {page}/{total_pages})</b>\n\n"
        for t in tours:
            text += f"<b>{t['name']}</b>\n💰 {t['price']}₽ | ⏱️ {t['duration_days']} дней\n\n"
    
    markup = telebot.types.InlineKeyboardMarkup()
    
    tours, _ = get_tours(page=page, per_page=3)
    for t in tours:
        tour_id = t['tour_id']
        print(f"[DEBUG] Добавляю кнопку: tour_detail_{tour_id}")
        markup.add(telebot.types.InlineKeyboardButton(f"📍 {t['name']}", callback_data=f"tour_detail_{tour_id}"))
    
    nav_markup = tours_pagination_keyboard(page, total_pages)
    for row in nav_markup.keyboard:
        markup.add(*row)
    
    if message_id:
        bot.edit_message_text(text, user_id, message_id, parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(user_id, text, parse_mode="HTML", reply_markup=markup)
