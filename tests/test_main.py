#!/usr/bin/env python3
"""
Unit‑тест для точки входа (main.py).
"""

import unittest
from unittest.mock import patch
from io import StringIO
import runpy
import main

class TestMain(unittest.TestCase):
    def test_main_entry_runpy(self):
        # Запускаем main.py как модуль __main__ через runpy
        with patch('builtins.input', side_effect=["стоп"]), \
             patch('sys.stdout', new=StringIO()) as fake_out:
            runpy.run_module("main", run_name="__main__")
            output = fake_out.getvalue()
            self.assertIn("Сеанс завершён.", output)

    def test_main_direct(self):
        # Вызываем main.main() напрямую и проверяем, что вызывается метод run
        with patch('hospital.app.HospitalApp.run', return_value=None) as fake_run:
            main.main()
            fake_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
