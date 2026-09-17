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


    def past_days_from_registration(self):
        '''Считает кол-во дней с момента регистрации аккаунта (с переводом unix-тайма)'''

        unix_time_created = self._formatted_unix_time.split('-')
        past_date = datetime(int(unix_time_created[0]), int(unix_time_created[1]), int(unix_time_created[2]))
        now = datetime.now()
        diff = now - past_date
        return diff.days

