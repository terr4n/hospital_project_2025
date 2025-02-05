#!/usr/bin/env python3
"""
Unit‑тесты для бизнес‑логики (модуль Hospital).
"""

import unittest
from hospital.models import Hospital

class TestHospital(unittest.TestCase):
    def setUp(self):
        self.hospital = Hospital(5)

    def test_get_patient_status_valid(self):
        # Все пациенты изначально в статусе "Болен" (код 1)
        self.assertEqual(self.hospital.get_patient_status(3), 1)

    def test_get_patient_status_invalid(self):
        # Неправильный ID: 0 или превышающий количество пациентов
        with self.assertRaises(ValueError):
            self.hospital.get_patient_status(0)
        with self.assertRaises(ValueError):
            self.hospital.get_patient_status(6)

    def test_set_patient_status(self):
        # Изменяем статус пациента
        self.hospital.set_patient_status(2, 2)
        self.assertEqual(self.hospital.get_patient_status(2), 2)

    def test_set_patient_status_invalid(self):
        # Попытка установить статус для несуществующего пациента
        with self.assertRaises(ValueError):
            self.hospital.set_patient_status(0, 2)
        with self.assertRaises(ValueError):
            self.hospital.set_patient_status(6, 2)

    def test_discharge(self):
        # Выписываем пациента и проверяем уменьшение числа пациентов
        self.hospital.discharge(3)
        self.assertEqual(len(self.hospital.patients), 4)
        # После выписки, пациент с новым ID=3 ранее имел ID=4 и его статус "Болен" (код 1)
        self.assertEqual(self.hospital.get_patient_status(3), 1)
        with self.assertRaises(ValueError):
            self.hospital.get_patient_status(6)

    def test_discharge_invalid(self):
        # Попытка выписать пациента с неверным ID
        with self.assertRaises(ValueError):
            self.hospital.discharge(0)
        with self.assertRaises(ValueError):
            self.hospital.discharge(6)

    def test_calculate_statistics(self):
        # Меняем статусы для проверки статистики
        self.hospital.set_patient_status(1, 0)
        self.hospital.set_patient_status(2, 2)
        stats = self.hospital.calculate_statistics()
        self.assertEqual(stats.get(0), 1)
        self.assertEqual(stats.get(1), 3)  # оставшиеся пациенты
        self.assertEqual(stats.get(2), 1)
        self.assertIsNone(stats.get(3))

    def test_calculate_statistics_empty(self):
        # Больница с 0 пациентами
        empty_hospital = Hospital(0)
        stats = empty_hospital.calculate_statistics()
        self.assertEqual(stats, {})

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
