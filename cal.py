import calendar


class Calendar:
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.day_names = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
        self.month_names = (
            "Январь",
            "Февраль",
            "Март",
            "Апрель",
            "Май",
            "Июнь",
            "Июль",
            "Август",
            "Сентябрь",
            "Октябрь",
            "Ноябрь",
            "Декабрь",
        )

    def get_month(self):
        return self.month_names[self.month - 1]
