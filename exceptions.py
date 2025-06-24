class BaseException(Exception):
    @property
    def message(self):
        return "Произошла ошибка"

class InvalidColumnName(BaseException):
    def __init__(self, column_name: str):
        self.column_name: str = column_name

    @property
    def message(self):
        return f"Столбца {self.column_name} нет в таблице"

class InvalidFormat(BaseException):
    @property
    def message(self):
        return "Аргументы записаны в неверном формате"

class EmptyValue(BaseException):
    @property
    def message(self):
        return "Переданы пустые значения"

class InvalidAggregateValue(BaseException):
    def __init__(self, aggr_value: str):
        self.aggr_value: str = aggr_value

    @property
    def message(self):
        return f"Неверное значение для агрегации: {self.aggr_value}"
    
class InvalidOrderByValue(BaseException):
    def __init__(self, value: str):
        self.value = value
        
    @property
    def message(self):
        return f"Неверное значение для сортировки: {self.value}"