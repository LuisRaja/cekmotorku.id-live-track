import flet as ft
from .. import theme as t

def build_live_row(state):
    return ft.Container(
        content=ft.Row(
            controls=[
                _live_cell('G-Force', state.g_force, 'g', 'gforce'),
                _divider(),
                _live_cell('Lean', state.lean_angle, '\u00b0', 'lean'),
                _divider(),
                _live_cell('Alt', f'{int(state.altitude)}' if state.altitude else '--', 'm', 'alt'),
                _divider(),
                _live_cell('Apex', state.top_speed, 'km/h', 'apex'),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
        padding=ft.Padding(12, 10, 12, 8),
        border=ft.border.only(top=ft.BorderSide(1, t.C_BORDER)),
    )

def _live_cell(label, value, unit, metric):
    color = t.LIVE_COLORS.get(metric, t.C_TEXT)
    val_text = str(value) if value is not None else '--'
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(label, size=8, weight=ft.FontWeight.W_800,
                        letter_spacing=0.8, color=t.C_TEXT_3,
                        text_align=ft.TextAlign.CENTER),
                ft.Text(val_text, size=16, weight=ft.FontWeight.W_700,
                        color=color, text_align=ft.TextAlign.CENTER),
                ft.Text(unit, size=7, weight=ft.FontWeight.W_600,
                        color=t.C_TEXT_3, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=1,
        ),
        expand=True,
    )

def _divider():
    return ft.Container(
        width=1,
        height=24,
        bgcolor=ft.Colors.with_opacity(0.05, '#FFFFFF'),
    )
