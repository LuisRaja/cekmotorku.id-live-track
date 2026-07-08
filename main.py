import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import flet as ft
from app.app import CekMotormuApp


def main(page: ft.Page):
    app = CekMotormuApp()
    app.build(page)


if __name__ == '__main__':
    ft.run(main=main)
