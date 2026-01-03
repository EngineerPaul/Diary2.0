from datetime import datetime, date, time, timedelta
from typing import List


class ChildrenMixin:
    """Миксин для формирования children из nested_folders и nested_objects"""

    def get_children(self, obj):
        nested_folders = []
        nested_objects = []
        if obj.nested_folders:
            nested_folders = [f'f{f_id}' for f_id in obj.nested_folders.split(',')]
        if obj.nested_objects:
            nested_objects = [f'n{r_id}' for r_id in obj.nested_objects.split(',')]
        return ','.join(nested_folders + nested_objects)


class PeriodicDate:
    """ The class of searching the next notice date using period and
    initial_date """

    def __init__(self, period: str, initial_date: date, time: time) -> None:
        period = period.split(',')  # like 0,0,0,0
        self.days = int(period[0])
        self.weeks = int(period[1])
        self.months = int(period[2])
        self.years = int(period[3])
        self.initial_date = initial_date
        self.time = time
        self.current_time = datetime.now().time()

    def get_next_date(self) -> date:
        """Verification (comparison) of the transmitted data"""

        # проверка, что initial_date и time еще не наступили

        # variants
        # № | days | weeks | months | years
        # 1 | 1-365|   0   |   0    |   0
        # 2 | 1-7  |  1-54 |   0    |   0
        # 3 | 1-7  |  1-6  |  1-12  |   0
        # 4 | 1-31 |   0   |  1-12  |   0
        # 5 | 1-365|   0   |   0    |   1
        # 6 | 1-7  |  1-54 |   0    |   1
        # 7 | 1-7  |  1-6  |  1-12  |   1
        # 8 | 1-31 |   0   |  1-12  |   1

        days365 = 1 <= self.days <= 365
        days31 = 1 <= self.days <= 31
        days7 = 1 <= self.days <= 7
        weeks54 = 1 <= self.weeks <= 54
        weeks6 = 1 <= self.weeks <= 6
        months12 = 1 <= self.months <= 12

        week0 = self.weeks == 0
        month0 = self.months == 0
        year0 = self.years == 0
        year1 = self.years == 1

        if all([days365, week0, month0, year0]):  # 1
            print(1)
            return self.get_D()
        elif all([days7, weeks54, month0, year0]):  # 2
            print(2)
            return self.get_DW()
        elif all([days7, weeks6, months12, year0]):  # 3
            print(3)
            return self.get_DWM()
        elif all([days31, week0, months12, year0]):  # 4
            print(4)
            return self.get_DM()
        elif all([days365, week0, month0, year1]):  # 5
            print(5)
            return self.get_DY()
        elif all([days7, weeks54, month0, year1]):  # 6
            print(6)
            return self.get_DWY()
        elif all([days7, weeks6, months12, year1]):  # 7
            print(7)
            return self.get_DWMY()
        elif all([days31, week0, months12, year1]):  # 8
            print(8)
            return self.get_DMY()
        else:
            print('Неверный period')
            return None

    def get_D(self) -> date:  # 1
        """Getting next day by Day"""

        # self.days  # 1-365
        if self.initial_date == date.today() and self.current_time < self.time:  # в тот же день
            next_date = self.initial_date
        elif self.initial_date > date.today():  # в будущий день
            next_date = self.initial_date
        else:  # если в нужный день время уже вышло (для повторов)
            next_date = self.initial_date + timedelta(days=self.days)
        return next_date

    def get_DW(self) -> date:  # 2
        """Getting next day by Day, Week"""

        # self.initial_date
        # self.days  # 1-7
        # self.weeks  # 1-54
        initial_weekday = self.initial_date.isoweekday()  # 1-7

        condition_1 = self.days > initial_weekday
        condition_2 = (self.days == initial_weekday and
                       self.time > self.current_time)
        if condition_1 or condition_2:
            # на этой неделе
            next_date = self.initial_date + timedelta(days=self.days-initial_weekday)
            next_date = datetime.combine(next_date, self.time)
        else:
            # прибавляем недели
            next_date = datetime.combine(self.initial_date, self.time)
            next_date = next_date + timedelta(days=self.weeks*7)

        return next_date.date()

    def get_DWM(self) -> date:  # 3
        """Getting next day by Day, Week, Month"""

        # self.initial_date
        # self.days  # 1-7
        # self.weeks  # 1-6
        # self.months  # 1-12

        target_day_number = self.get_month_day_by_weekday(  # получаем день месяца
            self.initial_date, self.weeks, self.days)

        target_day_is_later = target_day_number > self.initial_date.day
        target_day_is_same_time_later = (
            target_day_number == self.initial_date.day and
            self.time > self.current_time
        )
        if target_day_is_later or target_day_is_same_time_later:
            next_date = date(
                year=self.initial_date.year,
                month=self.initial_date.month,
                day=target_day_number
            )
        else:
            new_month = self.initial_date.month + self.months  # can be more than 12
            new_year = self.initial_date.year + (new_month - 1) // 12
            new_month = ((new_month - 1) % 12) + 1
            new_start_month = date(year=new_year, month=new_month, day=1)

            new_day_number = self.get_month_day_by_weekday(  # получаем день месяца
                new_start_month, self.weeks, self.days)

            next_date = date(
                year=new_year,
                month=new_month,
                day=new_day_number
            )

        return next_date

    def get_month_day_by_weekday(
            self, any_month_day: date, weeks: int, weekdays: int) -> int:
        """Получение номера дня месяца по номеру недели и дню недели"""

        full_initial_month = self.get_full_month(any_month_day)

        # Проверяем, не выходит ли индекс недели за границы списка
        week_index = weeks - 1
        if week_index >= len(full_initial_month):
            week_index = weeks - 2

        target_day_number = full_initial_month[week_index][weekdays - 1]

        if target_day_number == 0:
            if week_index + 1 == len(full_initial_month):
                week_index -= 1
            if week_index == 0:
                week_index += 1

            target_day_number = full_initial_month[week_index][weekdays - 1]

        return target_day_number

    def get_full_month(self, any_date: date) -> List:
        """ Создание месяца, как в календаре.
        Дни других месяцев заменены на 0 """

        first_day = date(year=any_date.year, month=any_date.month, day=1)

        # найдем начало первой недели (м.б. в другом месяце)
        first_weekday = first_day.isoweekday()
        days_to_subtract = first_weekday - 1  # Сколько дней до понедельника
        calendar_start = first_day - timedelta(days=days_to_subtract)

        current_date = calendar_start
        calendar = []
        for _week in range(6):
            week_days = []

            for _day in range(7):
                # дни других месяцев заполняем нулями
                if current_date.month == first_day.month:
                    week_days.append(current_date.day)
                else:
                    week_days.append(0)
                current_date += timedelta(days=1)

            calendar.append(week_days)

            # отсекаем лишние недели (их м.б. меньше 6)
            if (current_date.month != first_day.month and
                    current_date.isoweekday() == 1):
                break

        return calendar

    def get_DM(self) -> date:  # 4
        """Getting next day by Day, Month"""

        # self.initial_date
        # self.days  # 1-31
        # self.months  # 1-12

        init_date = datetime.combine(self.initial_date, self.current_time)
        target_date = datetime.combine(
            date=self.set_day(self.initial_date, self.days),
            time=self.time
        )
        if (init_date < target_date):
            return target_date.date()

        new_month = self.initial_date.month + self.months
        new_year = self.initial_date.year + (new_month - 1) // 12
        new_month = ((new_month - 1) % 12) + 1
        new_start_month = date(
            year=new_year,
            month=new_month,
            day=1
        )
        new_start_month = self.set_day(new_start_month, self.days)
        return new_start_month

    def set_day(self, any_date: date, target_day: int) -> date:
        """Устанавливает день месяца (полследний день при превышении в
        месяце)"""

        if any_date.month == 12:
            next_month_first = date(any_date.year + 1, 1, 1)
        else:
            next_month_first = date(any_date.year, any_date.month + 1, 1)
        last_day_month = (next_month_first - timedelta(days=1)).day
        day_to_use = min(target_day, last_day_month)

        target_date = date(
            year=any_date.year,
            month=any_date.month,
            day=day_to_use
        )
        return target_date

    def get_DY(self) -> date:  # 5
        """Getting next day by Day, Year"""

        # self.initial_date
        # self.days  # 1-366
        # self.years  # 1-1

        current_year = self.initial_date.year
        target_date = date(current_year, 1, 1) + timedelta(days=self.days - 1)
        if target_date.year > current_year:
            target_date -= timedelta(days=1)

        target_datetime = datetime.combine(target_date, self.time)
        current_datetime = datetime.combine(
            self.initial_date, self.current_time
        )
        if target_datetime <= current_datetime:
            current_year += self.years

        next_date = date(current_year, 1, 1) + timedelta(days=self.days - 1)
        if next_date.year > current_year:
            next_date -= timedelta(days=1)
        return next_date

    def get_DWY(self) -> date:  # 6
        """Getting next day by Day, Week, Year"""

        # self.initial_date
        # self.days  # 1-7 день недели
        # self.weeks  # 1-54 неделя года
        # self.years  # 1-1

        # Получаем дату в текущем году
        current_year = self.initial_date.year
        target_date = self.get_date_by_weeks_and_weekdays(current_year)

        target_datetime = datetime.combine(target_date, self.time)
        current_datetime = datetime.combine(
            self.initial_date, self.current_time
        )
        if target_datetime <= current_datetime:
            # Получаем дату в следующем году
            current_year += self.years
            target_date = self.get_date_by_weeks_and_weekdays(current_year)

        next_date = target_date
        return next_date

    def get_date_by_weeks_and_weekdays(self, year: int) -> date:
        """В указанном году находим день по неделе и дню недели"""

        # Находим первый день года
        first_day_of_year = date(year, 1, 1)
        first_day_weekday = first_day_of_year.isoweekday()  # 1-7

        # Находим первый день нужного дня недели в году
        days_to_add = self.days - first_day_weekday
        if days_to_add < 0:  # [-6;6]
            days_to_add += 7
        first_target_day = first_day_of_year + timedelta(days=days_to_add)

        # Добавляем недели
        target_date = first_target_day + timedelta(days=(self.weeks - 1) * 7)
        while target_date.year > year:
            target_date -= timedelta(days=7)

        return target_date

    def get_DWMY(self) -> date:  # 7
        """Getting next day by Day, Week, Month, Year"""

        # self.initial_date
        # self.days  # 1-7 день недели
        # self.weeks  # 1-6 неделя месяца
        # self.months  # 1-12 месяц года
        # self.years  # 1-1

        # Получаем дату в текущем году
        current_year = self.initial_date.year
        target_date = self.get_date_by_months_and_weekdays(current_year)

        target_datetime = datetime.combine(target_date, self.time)
        current_datetime = datetime.combine(
            self.initial_date, self.current_time
        )
        if target_datetime <= current_datetime:
            # Получаем дату в следующем году
            current_year += self.years
            target_date = self.get_date_by_months_and_weekdays(current_year)

        next_date = target_date
        return next_date

    def get_date_by_months_and_weekdays(self, year: int) -> date:
        """В указанном году находим день по месяцу, неделе и дню недели"""

        # Создаем дату первого дня нужного месяца в году
        target_month_start = date(year=year, month=self.months, day=1)

        # Получаем номер дня месяца по неделе и дню недели
        target_day_number = self.get_month_day_by_weekday(
            target_month_start, self.weeks, self.days
        )

        target_date = date(
            year=year,
            month=self.months,
            day=target_day_number
        )
        return target_date

    def get_DMY(self) -> date:  # 8
        """Getting next day by Day, Month, Year"""

        # self.initial_date
        # self.days  # 1-31 день месяца
        # self.months  # 1-12 месяц года
        # self.years  # 1-1

        # Получаем дату в текущем году
        current_year = self.initial_date.year
        target_date = self.get_date_by_month_and_day(current_year)

        target_datetime = datetime.combine(target_date, self.time)
        current_datetime = datetime.combine(
            self.initial_date, self.current_time
        )
        if target_datetime <= current_datetime:
            # Получаем дату в следующем году
            current_year += self.years
            target_date = self.get_date_by_month_and_day(current_year)

        next_date = target_date
        return next_date

    def get_date_by_month_and_day(self, year: int) -> date:
        """В указанном году находим день по месяцу и дню месяца"""

        month_start = date(year=year, month=self.months, day=1)
        target_date = self.set_day(month_start, self.days)

        return target_date
