from datetime import date

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

    def __init__(self, period: str, initial_data: date) -> None:
        period = period.split(',')  # like 0,0,0,0
        self.days = int(period[0])
        self.weeks = int(period[1])
        self.months = int(period[2])
        self.years = int(period[3])
        self.initial_data = initial_data

    def get_next_date(self):
        """Verification (comparison) of the transmitted data"""

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

    def get_D(self):  # 1
        """Getting next day by Day"""
        self.initial_data
        self.days
        next_date = None
        return next_date

    def get_DW(self):  # 2
        """Getting next day by Day, Week"""
        self.initial_data
        self.days
        self.weeks
        next_date = None
        return next_date

    def get_DWM(self):  # 3
        """Getting next day by Day, Week, Month"""
        self.initial_data
        self.days
        self.weeks
        self.months
        next_date = None
        return next_date

    def get_DM(self):  # 4
        """Getting next day by Day, Month"""
        self.initial_data
        self.days
        self.months
        next_date = None
        return next_date

    def get_DY(self):  # 5
        """Getting next day by Day, Year"""
        self.initial_data
        self.days
        self.years
        next_date = None
        return next_date

    def get_DWY(self):  # 6
        """Getting next day by Day, Week, Year"""
        self.initial_data
        self.days
        self.weeks
        self.years
        next_date = None
        return next_date

    def get_DWMY(self):  # 7
        """Getting next day by Day, Week, Month, Year"""
        self.initial_data
        self.days
        self.weeks
        self.months
        self.years
        next_date = None
        return next_date

    def get_DMY(self):  # 8
        """Getting next day by Day, Month, Year"""
        self.initial_data
        self.days
        self.months
        self.years
        next_date = None
        return next_date
