#!/usr/bin/env python3
"""
Модуль моделей для проекта Hospital.
Содержит определения бизнес-логики: класс Hospital и словарь описания статусов пациентов.
"""

# Словарь с описанием статусов пациентов.
STATUS_TEXT = {
    0: "Тяжело болен",
    1: "Болен",
    2: "Слегка болен",
    3: "Готов к выписке"
}


class Hospital:
    """
    Класс, представляющий больницу и базу пациентов.
    База пациентов реализована как список целых чисел (коды статусов).
    Пациенты идентифицируются по порядковому номеру (ID = индекс + 1).
    """
    def __init__(self, count=200):
        # Инициализируем больницу с count пациентами, все в статусе "Болен" (код 1)
        self.patients = [1] * count

    def get_patient_status(self, patient_id):
        """
        Получает статус пациента по его ID.
        :param patient_id: целое число, 1-индексированный ID пациента
        :return: код статуса пациента
        :raises ValueError: если ID некорректен
        """
        index = patient_id - 1
        if index < 0 or index >= len(self.patients):
            raise ValueError("Ошибка. В больнице нет пациента с таким ID")
        return self.patients[index]

    def set_patient_status(self, patient_id, status):
        """
        Устанавливает статус пациента по его ID.
        :param patient_id: целое число, 1-индексированный ID пациента
        :param status: новый код статуса
        :raises ValueError: если ID некорректен
        """
        index = patient_id - 1
        if index < 0 or index >= len(self.patients):
            raise ValueError("Ошибка. В больнице нет пациента с таким ID")
        self.patients[index] = status

    def discharge(self, patient_id):
        """
        Выписывает пациента из больницы (удаляет его из базы).
        :param patient_id: целое число, 1-индексированный ID пациента
        :raises ValueError: если ID некорректен
        """
        index = patient_id - 1
        if index < 0 or index >= len(self.patients):
            raise ValueError("Ошибка. В больнице нет пациента с таким ID")
        del self.patients[index]

    def calculate_statistics(self):
        """
        Рассчитывает статистику по статусам пациентов.
        :return: словарь {код статуса: количество пациентов}
        """
        stats = {}
        for status in self.patients:
            stats[status] = stats.get(status, 0) + 1
        return stats
