#!/usr/bin/env python3
"""
Точка входа в приложение.
"""

from hospital.app import HospitalApp

def main():
    app = HospitalApp()
    app.run()

if __name__ == '__main__':
    main()
