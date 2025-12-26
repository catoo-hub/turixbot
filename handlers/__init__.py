from .start import register as reg_start
from .buttons import register as reg_buttons
from .tours import register as reg_tours
from .balance import register as reg_balance
from .bookings import register as reg_bookings
from .profile import register as reg_profile

# == Регистрация хэндлеров ==
def register(bot):
    reg_start(bot)
    reg_buttons(bot)
    reg_tours(bot)
    reg_balance(bot)
    reg_bookings(bot)
    reg_profile(bot)
