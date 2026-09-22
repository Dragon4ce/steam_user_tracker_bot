import datetime
from datetime import datetime

class Time:
    def __init__(self, unix_time):
        self._unix_time = str(unix_time)
        self._formatted_unix_time = datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d')
        self._sp = datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d').split('-')

    def unix_turn(self):
        return self._formatted_unix_time

    def days_amount_from_registration(self):
        past_date = datetime(int(self._sp[0]), int(self._sp[1]), int(self._sp[2]))
        date_now = datetime.now()
        delta = date_now - past_date
        return delta.days

    def pretty_time(self):
        months_ru = [' ', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                     'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        return f"{int(self._sp[2])} {months_ru[int(self._sp[1])]} {self._sp[0]}"

    # def last_logoff_time(self):
    #     return datetime.fromtimestamp(int(self._unix_time)).strftime("%H:%M")

    def time_since_last_logoff(self) -> str:
        """
        Возвращает строку вида:
        - "только что" (меньше 60 секунд)
        - "5 минут назад"
        - "2 часа назад"
        - "3 дня назад"
        - "2 месяца назад"
        - "1 год назад"
        """
        if not self._unix_time:
            return "Неизвестно"
        unix_time = int(self._unix_time)
        now = datetime.now()
        last_seen = datetime.fromtimestamp(unix_time)

        diff = now - last_seen
        seconds = int(diff.total_seconds())

        if seconds < 60:
            return "только что"

        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} {'минуту' if minutes == 1 else 'минуты' if 2 <= minutes <= 4 else 'минут'} назад"

        hours = minutes // 60
        if hours < 24:
            return f"{hours} {'час' if hours == 1 else 'часа' if 2 <= hours <= 4 else 'часов'} назад"

        days = hours // 24
        if days < 30:
            return f"{days} {'день' if days == 1 else 'дня' if 2 <= days <= 4 else 'дней'} назад"

        months = days // 30
        if months < 12:
            return f"{months} {'месяц' if months == 1 else 'месяца' if 2 <= months <= 4 else 'месяцев'} назад"

        years = months // 12
        return f"{years} {'год' if years == 1 else 'года' if 2 <= years <= 4 else 'лет'} назад"


    def past_days_from_registration(self):
        '''Считает кол-во дней с момента регистрации аккаунта (с переводом unix-тайма)'''

        unix_time_created = self._formatted_unix_time.split('-')
        past_date = datetime(int(unix_time_created[0]), int(unix_time_created[1]), int(unix_time_created[2]))
        now = datetime.now()
        diff = now - past_date
        return diff.days

