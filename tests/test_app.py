#!/usr/bin/env python3
"""
Unit‑тесты для консольного приложения (HospitalApp).
Используется симуляция ввода/вывода с помощью patch.
"""

import unittest
from io import StringIO
from unittest.mock import patch
from hospital.app import HospitalApp

class TestHospitalApp(unittest.TestCase):
    def setUp(self):
        # Каждый тест создаёт новое приложение
        self.app = HospitalApp()

    def run_app_with_inputs(self, inputs):
        """
        Вспомогательная функция для запуска приложения с заданной последовательностью ввода.
        :param inputs: список строк, которые будут поданы на input()
        :return: строка, содержащая весь вывод (stdout)
        """
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.app.run()
                return fake_out.getvalue()

    def test_acceptance_scenario_1(self):
        # Приёмочный тест №1: базовый сценарий
        inputs = [
            "узнать статус пациента", "200",
            "status up", "2",
            "status down", "3",
            "discharge", "4",
            "рассчитать статистику",
            "стоп"
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn('Статус пациента: "Болен"', output)
        self.assertIn('Новый статус пациента: "Слегка болен"', output)
        self.assertIn('Новый статус пациента: "Тяжело болен"', output)
        self.assertIn("Пациент выписан из больницы", output)
        self.assertIn('В больнице на данный момент находится 199 чел., из них:', output)
        self.assertIn('\t- в статусе "Тяжело болен": 1 чел.', output)
        self.assertIn('\t- в статусе "Болен": 197 чел.', output)
        self.assertIn('\t- в статусе "Слегка болен": 1 чел.', output)

    def test_acceptance_scenario_2_unknown_command(self):
        # Приёмочный тест №2: неизвестная команда
        inputs = [
            "выписать всех пациентов",
            "STOP"  # команда стоп, регистронезависимая
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn("Неизвестная команда! Попробуйте ещё раз", output)
        self.assertIn("Сеанс завершён.", output)

    def test_acceptance_scenario_3_invalid_id(self):
        # Приёмочный тест №3: некорректный ввод ID
        inputs = [
            "узнать статус пациента", "два",
            "повысить статус пациента", "-2",
            "понизить статус пациента", "201",
            "стоп"
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn("Ошибка. ID пациента должно быть числом (целым, положительным)", output)
        self.assertIn("Ошибка. В больнице нет пациента с таким ID", output)
        self.assertIn("Сеанс завершён.", output)

    def test_acceptance_scenario_4_status_up_then_discharge(self):
        # Приёмочный тест №4: повышение статуса с выпиской
        inputs = [
            "повысить статус пациента", "1",  # 1: "Болен" -> "Слегка болен"
            "повысить статус пациента", "1",  # -> "Готов к выписке"
            "повысить статус пациента", "1",  # запрос на выписку
            "да",                           # подтверждаем выписку
            "рассчитать статистику",
            "стоп"
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn('Новый статус пациента: "Слегка болен"', output)
        self.assertIn('Новый статус пациента: "Готов к выписке"', output)
        self.assertIn("Пациент выписан из больницы", output)
        self.assertIn('В больнице на данный момент находится 199 чел., из них:', output)
        self.assertIn('\t- в статусе "Болен": 199 чел.', output)

    def test_acceptance_scenario_5_status_up_no_discharge(self):
        # Приёмочный тест №5: повышение статуса, но отказ от выписки
        inputs = [
            "повысить статус пациента", "1",  # 1 -> 2 ("Слегка болен")
            "повысить статус пациента", "1",  # 2 -> 3 ("Готов к выписке")
            "повысить статус пациента", "1",  # запрос на выписку
            "нет",                         # отказываемся от выписки
            "рассчитать статистику",
            "стоп"
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn('Новый статус пациента: "Слегка болен"', output)
        self.assertIn('Новый статус пациента: "Готов к выписке"', output)
        self.assertIn('Пациент остался в статусе "Готов к выписке"', output)
        self.assertIn('В больнице на данный момент находится 200 чел., из них:', output)
        self.assertIn('\t- в статусе "Болен": 199 чел.', output)
        self.assertIn('\t- в статусе "Готов к выписке": 1 чел.', output)

    def test_acceptance_scenario_6_status_down_min(self):
        # Приёмочный тест №6: попытка понизить статус ниже минимального
        inputs = [
            "понизить статус пациента", "1",  # 1 -> 0 ("Тяжело болен")
            "понизить статус пациента", "1",  # уже 0, ошибка
            "рассчитать статистику",
            "стоп"
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn('Новый статус пациента: "Тяжело болен"', output)
        self.assertIn("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)", output)
        self.assertIn('В больнице на данный момент находится 200 чел., из них:', output)
        self.assertIn('\t- в статусе "Тяжело болен": 1 чел.', output)
        self.assertIn('\t- в статусе "Болен": 199 чел.', output)

    def test_stop_command_case_insensitive(self):
        # Проверка команды стоп в разных регистрах
        inputs = [
            "StOp"
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn("Сеанс завершён.", output)

    def test_unknown_command_then_valid(self):
        # Сначала неизвестная команда, затем корректная команда
        inputs = [
            "unknown command",
            "стоп"
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn("Неизвестная команда! Попробуйте ещё раз", output)
        self.assertIn("Сеанс завершён.", output)

    def test_status_up_default_answer(self):
        # Тест для ветки, когда ответ не "да" и не "нет"
        # Устанавливаем для пациента 1 максимальный статус (3)
        self.app.hospital.set_patient_status(1, 3)
        inputs = [
            "повысить статус пациента", "1",  # попадаем в ветку максимального статуса
            "maybe",  # ответ не "да" и не "нет"
            "стоп"
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn('Пациент остался в статусе "Готов к выписке"', output)

    def test_cmd_get_status_exception(self):
        # Переопределяем метод get_patient_status, чтобы он выбрасывал исключение
        self.app.hospital.get_patient_status = lambda pid: (_ for _ in ()).throw(ValueError("Test Error"))
        inputs = [
            "узнать статус пациента", "1",
            "стоп"
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn("Test Error", output)

    def test_cmd_discharge_exception(self):
        # Переопределяем метод discharge, чтобы он выбрасывал исключение
        self.app.hospital.discharge = lambda pid: (_ for _ in ()).throw(ValueError("Test Discharge Error"))
        inputs = [
            "выписать пациента", "1",
            "стоп"
        ]
        output = self.run_app_with_inputs(inputs)
        self.assertIn("Test Discharge Error", output)

    def test_cmd_status_up_exception(self):
        # Переопределяем метод get_patient_status, чтобы он выбрасывал исключение при вызове cmd_status_up
        self.app.hospital.get_patient_status = lambda pid: (_ for _ in ()).throw(ValueError("Status up error"))
        with patch('sys.stdout', new=StringIO()) as fake_out, \
             patch('builtins.input', return_value="1"):
            self.app.cmd_status_up()
            output = fake_out.getvalue()
            self.assertIn("Status up error", output)

    def test_cmd_status_down_exception(self):
        # Переопределяем метод get_patient_status, чтобы он выбрасывал исключение при вызове cmd_status_down
        self.app.hospital.get_patient_status = lambda pid: (_ for _ in ()).throw(ValueError("Status down error"))
        with patch('sys.stdout', new=StringIO()) as fake_out, \
             patch('builtins.input', return_value="1"):
            self.app.cmd_status_down()
            output = fake_out.getvalue()
            self.assertIn("Status down error", output)

    def test_cmd_discharge_no_id(self):
        # Тест для ветки, когда read_patient_id возвращает None (например, из-за неверного ввода)
        with patch('builtins.input', return_value="0"):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.app.cmd_discharge()
                output = fake_out.getvalue()
                self.assertIn("Ошибка. ID пациента должно быть числом (целым, положительным)", output)

    def test_cmd_status_down_no_id(self):
        # Тест для ветки, когда read_patient_id возвращает None при вызове cmd_status_down
        with patch('builtins.input', return_value="abc"):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                self.app.cmd_status_down()
                output = fake_out.getvalue()
                self.assertIn("Ошибка. ID пациента должно быть числом (целым, положительным)", output)

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
