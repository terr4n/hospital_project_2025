#!/usr/bin/env python3
"""
Модуль приложения для управления больницей.
Содержит класс HospitalApp, реализующий консольное взаимодействие с пользователем.
"""

from hospital.models import Hospital, STATUS_TEXT


class HospitalApp:
    """
    Класс приложения для управления больницей.
    Обрабатывает команды пользователя и взаимодействует с модулем управления пациентами (Hospital).
    """
    def __init__(self):
        self.hospital = Hospital(200)
        self.status_text = STATUS_TEXT
        # Словарь доступных команд (на русском и английском) и соответствующих методов.
        self.commands = {
            "узнать статус пациента": self.cmd_get_status,
            "get status": self.cmd_get_status,
            "повысить статус пациента": self.cmd_status_up,
            "status up": self.cmd_status_up,
            "понизить статус пациента": self.cmd_status_down,
            "status down": self.cmd_status_down,
            "выписать пациента": self.cmd_discharge,
            "discharge": self.cmd_discharge,
            "рассчитать статистику": self.cmd_calculate_statistics,
            "calculate statistics": self.cmd_calculate_statistics,
            "стоп": self.cmd_stop,
            "stop": self.cmd_stop,
        }
        self.running = True

    def run(self):
        """
        Основной цикл обработки команд пользователя.
        """
        while self.running:
            command = input("Введите команду: ").strip().lower()
            if command in self.commands:
                self.commands[command]()
            else:
                print("Неизвестная команда! Попробуйте ещё раз")

    def read_patient_id(self):
        """
        Считывает ID пациента с консоли и проверяет корректность.
        :return: ID пациента (целое число) или None в случае ошибки
        """
        pid_str = input("Введите ID пациента: ").strip()
        try:
            pid = int(pid_str)
            if pid <= 0:
                raise ValueError
            if pid > len(self.hospital.patients):
                print("Ошибка. В больнице нет пациента с таким ID")
                return None
            return pid
        except ValueError:
            print("Ошибка. ID пациента должно быть числом (целым, положительным)")
            return None

    def cmd_get_status(self):
        """
        Обработка команды "узнать статус пациента" / "get status".
        Выводит статус пациента.
        """
        pid = self.read_patient_id()
        if pid is None:
            return
        try:
            status_code = self.hospital.get_patient_status(pid)
            print(f'Статус пациента: "{self.status_text[status_code]}"')
        except ValueError as e:
            print(e)

    def cmd_status_up(self):
        """
        Обработка команды "повысить статус пациента" / "status up".
        Если пациент не на максимальном статусе, повышает его статус.
        Если пациент на максимальном статусе, запрашивает подтверждение выписки.
        """
        pid = self.read_patient_id()
        if pid is None:
            return
        try:
            current_status = self.hospital.get_patient_status(pid)
        except ValueError as e:
            print(e)
            return
        if current_status < 3:
            new_status = current_status + 1
            self.hospital.set_patient_status(pid, new_status)
            print(f'Новый статус пациента: "{self.status_text[new_status]}"')
        else:
            answer = input("Желаете этого клиента выписать? (да/нет): ").strip().lower()
            if answer == "да":
                self.hospital.discharge(pid)
                print("Пациент выписан из больницы")
            elif answer == "нет":
                print(f'Пациент остался в статусе "{self.status_text[current_status]}"')
            else:
                print(f'Пациент остался в статусе "{self.status_text[current_status]}"')

    def cmd_status_down(self):
        """
        Обработка команды "понизить статус пациента" / "status down".
        Если пациент не на минимальном статусе, понижает его статус.
        Если пациент уже на минимальном статусе, выводит сообщение об ошибке.
        """
        pid = self.read_patient_id()
        if pid is None:
            return
        try:
            current_status = self.hospital.get_patient_status(pid)
        except ValueError as e:
            print(e)
            return
        if current_status > 0:
            new_status = current_status - 1
            self.hospital.set_patient_status(pid, new_status)
            print(f'Новый статус пациента: "{self.status_text[new_status]}"')
        else:
            print("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)")

    def cmd_discharge(self):
        """
        Обработка команды "выписать пациента" / "discharge".
        Выписывает пациента из больницы.
        """
        pid = self.read_patient_id()
        if pid is None:
            return
        try:
            self.hospital.discharge(pid)
            print("Пациент выписан из больницы")
        except ValueError as e:
            print(e)

    def cmd_calculate_statistics(self):
        """
        Обработка команды "рассчитать статистику" / "calculate statistics".
        Выводит статистику по количеству пациентов в каждом статусе.
        """
        stats = self.hospital.calculate_statistics()
        total = len(self.hospital.patients)
        print(f'В больнице на данный момент находится {total} чел., из них:')
        for code in sorted(self.status_text.keys()):
            count = stats.get(code, 0)
            if count > 0:
                print(f'\t- в статусе "{self.status_text[code]}": {count} чел.')

    def cmd_stop(self):
        """
        Обработка команды "стоп" / "stop".
        Завершает сеанс работы приложения.
        """
        print("Сеанс завершён.")
        self.running = False
