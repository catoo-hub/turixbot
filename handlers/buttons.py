def register(bot):
    from utils.keyboard import main_menu
    from database.models import get_balance
    from utils.keyboard import balance_keyboard, topup_tour_keyboard
    from utils.progress import get_progress_bar
    
    # == Хэндлер для кнопок ==
    @bot.callback_query_handler(func=lambda call: call.data == "btn_tours")
    def handle_tours_button(call):
        from handlers.tours import show_tours_page
        show_tours_page(bot, call.from_user.id, page=1, message_id=call.message.message_id)
        bot.answer_callback_query(call.id)
    
    # == Избранное ==
    @bot.callback_query_handler(func=lambda call: call.data == "btn_favorites")
    def handle_favorites_button(call):
        from database.models import get_favorites, get_tour_by_id, get_progress
        import telebot
        
        favs = get_favorites(call.from_user.id)
        if not favs:
            bot.edit_message_text("Нет избранных туров.", 
                                 call.from_user.id,
                                 call.message.message_id,
                                 reply_markup=main_menu())
            bot.answer_callback_query(call.id)
            return
        
        text = "⭐ <b>Твои избранные туры:</b>\n\n"
        markup = telebot.types.InlineKeyboardMarkup()
        
        # == Перебираем избранные туры + прогресс ==
        for t in favs:
            progress = get_progress(call.from_user.id, t['tour_id'])
            percent = (progress / t['price']) * 100 if t['price'] > 0 else 0
            bar = get_progress_bar(int(progress), int(t['price']))
            
            text += f"<b>{t['name']}</b>\n💰 {t['price']}₽\n📊 {bar}\n\n"
            markup.add(telebot.types.InlineKeyboardButton(
                f"💳 Пополнить", 
                callback_data=f"topup_{t['tour_id']}"
            ))
        
        markup.add(telebot.types.InlineKeyboardButton("↩️ Меню", callback_data="main_menu"))
        
        bot.edit_message_text(text, 
                             call.from_user.id,
                             call.message.message_id,
                             parse_mode="HTML",
                             reply_markup=markup)
        bot.answer_callback_query(call.id)
    
    # == Баланс ==
    @bot.callback_query_handler(func=lambda call: call.data == "btn_balance")
    def handle_balance_button(call):
        balance = get_balance(call.from_user.id)
        text = f"💰 <b>Ваш баланс: {balance}₽</b>\n\nВыберите сумму для пополнения:"
        bot.edit_message_text(text, 
                             call.from_user.id,
                             call.message.message_id,
                             parse_mode="HTML",
                             reply_markup=balance_keyboard())
        bot.answer_callback_query(call.id)
    
    # == Бронирования ==
    @bot.callback_query_handler(func=lambda call: call.data == "btn_bookings")
    def handle_bookings_button(call):
        from database.models import get_favorites, get_progress, get_tour_by_id
        import telebot
        
        favs = get_favorites(call.from_user.id)
        if not favs:
            bot.edit_message_text("Нет забронированных туров.", 
                                 call.from_user.id,
                                 call.message.message_id,
                                 reply_markup=main_menu())
            bot.answer_callback_query(call.id)
            return
        
        text = "📔 <b>Доступные туры для бронирования:</b>\n\n"
        markup = telebot.types.InlineKeyboardMarkup()
        
        # == Перебираем избранные туры + прогресс ==
        for t in favs:
            progress = get_progress(call.from_user.id, t['tour_id'])
            percent = (progress / t['price']) * 100 if t['price'] > 0 else 0
            
            if percent >= 100:
                text += f"✅ <b>{t['name']}</b> (готово к бронированию)\n\n"
                markup.add(telebot.types.InlineKeyboardButton(
                    f"🎫 Забронировать {t['name']}", 
                    callback_data=f"book_{t['tour_id']}"
                ))
            else:
                text += f"⏳ <b>{t['name']}</b> ({int(percent)}% - не готово)\n\n"
        
        markup.add(telebot.types.InlineKeyboardButton("↩️ Меню", callback_data="main_menu"))
        
        bot.edit_message_text(text, 
                             call.from_user.id,
                             call.message.message_id,
                             parse_mode="HTML",
                             reply_markup=markup)
        bot.answer_callback_query(call.id)
    
    # == Помощь ==
    @bot.callback_query_handler(func=lambda call: call.data == "btn_help")
    def handle_help_button(call):
        text = ("ℹ️ <b>TurixBot помогает:</b>\n"
                "🌏 Просмотреть туры\n"
                "⭐ Добавить в избранное\n"
                "💰 Пополнить баланс\n"
                "🎫 Забронировать туры\n"
                "👤 Управлять профилем")
        bot.edit_message_text(text,
                            call.from_user.id,
                            call.message.message_id,
                            parse_mode="HTML",
                            reply_markup=main_menu())
        bot.answer_callback_query(call.id)

    # == Главное меню ==
    @bot.callback_query_handler(func=lambda call: call.data == "main_menu")
    def handle_main_menu(call):
        bot.edit_message_text("👋 <b>Главное меню</b>",
                             call.from_user.id,
                             call.message.message_id,
                             parse_mode="HTML",
                             reply_markup=main_menu())
        bot.answer_callback_query(call.id)
    
    # == Пополнение прогресса тура ==
    @bot.callback_query_handler(func=lambda call: call.data.startswith("topup_") and not call.data.startswith("topup_amount_") and not call.data.startswith("topup_all_"))
    def handle_topup(call):
        from database.models import get_tour_by_id, get_balance, get_progress
        from utils.context import set_user_tour
        
        tour_id = int(call.data.split("_")[1])
        user_id = call.from_user.id
        
        set_user_tour(user_id, tour_id)
        
        tour = get_tour_by_id(tour_id)
        balance = get_balance(user_id)
        progress = get_progress(user_id, tour_id)
        needed = max(0, tour['price'] - progress)  # fixed: не может быть отрицательным
        
        text = f"""
💳 <b>Пополнить средства для тура:</b>

🌍 Тур: {tour['name']}
💰 Цена: {tour['price']}₽
💵 Ваш баланс: {balance}₽
📊 Накоплено: {progress}₽ / {tour['price']}₽

{'🎉 Готово к бронированию!' if progress >= tour['price'] else f'❌ Не хватает: {needed}₽'}
        """
        
        bot.edit_message_text(text,
                             user_id,
                             call.message.message_id,
                             parse_mode="HTML",
                             reply_markup=topup_tour_keyboard(tour_id))
        bot.answer_callback_query(call.id)
    
    # == Обработка пополнения на конкретную сумму ==
    @bot.callback_query_handler(func=lambda call: call.data.startswith("topup_amount_"))
    def handle_topup_amount(call):
        from database.models import get_tour_by_id, get_balance, get_progress, add_progress
        from utils.progress import get_progress_bar
        
        parts = call.data.split("_")
        tour_id = int(parts[2])
        amount = int(parts[3])
        user_id = call.from_user.id
        
        balance = get_balance(user_id)
        
        if balance < amount:
            bot.answer_callback_query(call.id, f"❌ Недостаточно баланса! Есть: {balance}₽, нужно: {amount}₽", show_alert=True)
            return
        
        # == Переводим средства из баланса в прогресс ==
        from database.models import update_balance
        update_balance(user_id, -amount)
        add_progress(user_id, tour_id, amount)
        
        tour = get_tour_by_id(tour_id)
        progress = get_progress(user_id, tour_id)
        new_balance = get_balance(user_id)
        bar = get_progress_bar(int(progress), int(tour['price']))
        
        text = f"""
✅ <b>Пополнено на {amount}₽</b>

🌍 Тур: {tour['name']}
💰 Цена: {tour['price']}₽
💵 Ваш баланс: {new_balance}₽
📊 Прогресс: {bar}

{'🎉 Готово к бронированию!' if progress >= tour['price'] else 'Продолжайте пополнять...'}
        """
        
        bot.edit_message_text(text,
                             user_id,
                             call.message.message_id,
                             parse_mode="HTML",
                             reply_markup=topup_tour_keyboard(tour_id))
        bot.answer_callback_query(call.id)
    
    # == Обработка пополнения всего баланса ==
    @bot.callback_query_handler(func=lambda call: call.data.startswith("topup_all_"))
    def handle_topup_all(call):
        from database.models import get_tour_by_id, get_balance, get_progress, add_progress, update_balance
        from utils.progress import get_progress_bar
        
        tour_id = int(call.data.split("_")[2])
        user_id = call.from_user.id
        
        balance = get_balance(user_id)
        
        if balance <= 0:
            bot.answer_callback_query(call.id, "❌ На балансе нет средств!", show_alert=True)
            return
        
        # Переводим ВСЕ средства из баланса в прогресс
        update_balance(user_id, -balance)
        add_progress(user_id, tour_id, balance)
        
        tour = get_tour_by_id(tour_id)
        progress = get_progress(user_id, tour_id)
        new_balance = get_balance(user_id)
        bar = get_progress_bar(int(progress), int(tour['price']))
        
        text = f"""
✅ <b>Весь баланс переведен ({balance}₽)</b>

🌍 Тур: {tour['name']}
💰 Цена: {tour['price']}₽
💵 Ваш баланс: {new_balance}₽
📊 Прогресс: {bar}

{'🎉 Готово к бронированию!' if progress >= tour['price'] else 'Продолжайте пополнять...'}
        """
        
        bot.edit_message_text(text,
                             user_id,
                             call.message.message_id,
                             parse_mode="HTML",
                             reply_markup=topup_tour_keyboard(tour_id))
        bot.answer_callback_query(call.id)
