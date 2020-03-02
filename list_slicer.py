# -*- coding: utf-8 -*-

input_list = [2, 11, 4, 1, 5, 2, 2, 10, 3, 3, 3, 2, 5, 7, 3, 1, 4, 1, 2, 3]

COL = 6  # Целевое количество колонок
peak_ = max(input_list)/2  # Половина максимального значения в одной "букве"


class MenuSplit:
    def __init__(self, _input_list):
        average_ = sum(input_list)/COL  # Среднее значение кол-ва элементов в одном столбце
        self.middle = peak_ if peak_ > average_ else average_
        self.out_list = []
        self._input_list = _input_list
        self._next = None
        self._local_sum = 0
        self._row = []
        self._menu_split()
        [i.reverse() for i in self.out_list]
        self.out_list.reverse()

    @staticmethod
    def deviation(_middle, _menu_list):
        """
        Сумма отклонений по всем колонкам. Дает грубую оценку эффективности алгоритма
        :param _middle: целевое значение количества пунктов в колонке
        :param _menu_list: итоговый список
        :return: Отклонение
        """

        _deviation = 0
        for liter in _menu_list:
            _deviation += abs(_middle - sum(liter))
        return _deviation

    def _menu_split(self):
        """
        Нарезка списка
        """

        def last_is_fat(current, next_):
            return len(self.out_list) == 0 and self._local_sum + current + next_ > self.middle

        def left_larger(current, next_):
            return self._local_sum + current + next_ < self.middle or \
                   (abs(self.middle - (self._local_sum + current)) >= abs(self.middle -
                                                                          (self._local_sum + current + next_)))

        def left_under(current, next_):
            return abs(self.middle - (self._local_sum + current)) < abs(self.middle -
                                                                        (self._local_sum + current + next_))

        def is_last_row():
            return len(self._input_list) == 1 and len(self.out_list) == COL-1

        def stay_in_row(current):
            self._local_sum += current

        def go_next_row():
            self.out_list.append(self._row)
            self._row = []
            self._local_sum = 0

        while self._input_list:
            _current = self._input_list.pop()
            _next = self._input_list[-1] if self._input_list else 0
            self._row.append(_current)
            if not last_is_fat(_current, _next) and (is_last_row() or left_larger(_current, _next)):
                stay_in_row(_current)
            elif last_is_fat(_current, _next) or left_under(_current, _next):
                go_next_row()
        self.out_list.append(self._row)


if __name__ == "__main__":
    for correction in [0, ]:  # Пробуем разные поправки к кол-ву элементов в одном столбце
        menu_list = MenuSplit(input_list)
        print(u"Среднее значение: {}\n"
              u"Поправка: {}\n"
              u"Суммарное отклонение: {}\n"
              u"Результат: {}\n".format(menu_list.middle,
                                        correction,
                                        MenuSplit.deviation(menu_list.middle, menu_list.out_list),
                                        menu_list.out_list))
