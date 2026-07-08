import flet as ft
from .. import theme as t

def build_bottom_nav(state):
    return ft.Container(
        content=ft.Row(
            controls=[
                _nav_item('SPEED', ft.Icons.SPEED, True),
                _record_button(state),
                _nav_item('TOURING', ft.Icons.ROUTE, False),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        padding=ft.Padding(8, 8, 8, 8 + 0),
    )

def _nav_item(label, icon, active):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(icon, size=20,
                        color=t.C_BRAND if active else t.C_TEXT_3),
                ft.Text(label, size=9, weight=ft.FontWeight.W_700,
                        letter_spacing=0.3,
                        color=t.C_BRAND if active else t.C_TEXT_3),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=3,
        ),
        padding=ft.Padding(14, 6, 14, 6),
        border_radius=12,
        bgcolor=t.C_BRAND_DIM if active else None,
        border=ft.border.all(1, ft.Colors.with_opacity(0.08, '#BDFF00')) if active else None,
    )

def _record_button(state):
    recording = state.is_tracking

    def on_click(e):
        pass

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(
                    ft.Icons.STOP if recording else ft.Icons.PLAY_ARROW,
                    size=18, color='#09090D' if not recording else t.C_DANGER,
                ),
                ft.Text('MULAI' if not recording else 'STOP',
                        size=9, weight=ft.FontWeight.W_900,
                        color='#09090D' if not recording else t.C_DANGER,
                        letter_spacing=0.5),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        ),
        padding=ft.Padding(20, 8, 20, 7),
        border_radius=16,
        gradient=ft.LinearGradient(
            colors=['#BDFF00', '#8CE600'],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
        ) if not recording else None,
        bgcolor=t.C_DANGER_DIM if recording else None,
        border=ft.border.all(1, ft.Colors.with_opacity(0.35, '#FF4757')) if recording else None,
        animate=ft.Animation(200, 'ease'),
    )
