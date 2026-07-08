import flet as ft
from .. import theme as t

def build_hud_card(state, on_pause, on_stop):
    stats = state.get_stats()
    is_recording = state.is_tracking

    speed_text = ft.Text(
        str(stats['speed']),
        size=82, weight=ft.FontWeight.W_700,
        letter_spacing=-3,
        color=t.C_BRAND if stats['speed'] > 80 else t.C_TEXT,
        text_align=ft.TextAlign.CENTER,
    )

    speed_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    height=76,
                    content=ft.Stack(
                        width=140, height=76,
                        controls=[
                            ft.Container(height=76),
                        ],
                    ),
                ),
                speed_text,
                ft.Text('KM/H', size=10, weight=ft.FontWeight.W_700,
                        letter_spacing=2.5, color=t.C_TEXT_3,
                        text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        ),
        padding=ft.Padding(20, 16, 20, 10),
    )

    def stat_cell(label, value, sub=''):
        return ft.Column(
            controls=[
                ft.Text(label, size=9, weight=ft.FontWeight.W_800,
                        letter_spacing=1, color=t.C_TEXT_3,
                        text_align=ft.TextAlign.CENTER),
                ft.Text(str(value), size=17, weight=ft.FontWeight.W_700,
                        letter_spacing=-0.3, color=t.C_TEXT,
                        text_align=ft.TextAlign.CENTER),
                ft.Text(sub, size=8, color=t.C_TEXT_3,
                        text_align=ft.TextAlign.CENTER) if sub else ft.Container(height=8),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=1,
        )

    stats_row = ft.Container(
        content=ft.Row(
            controls=[
                stat_cell('TOP', stats['top_speed'], 'KM/H'),
                ft.Container(width=1, height=24, bgcolor=ft.Colors.with_opacity(0.05, '#FFFFFF')),
                stat_cell('JARAK', stats['distance'], 'KM'),
                ft.Container(width=1, height=24, bgcolor=ft.Colors.with_opacity(0.05, '#FFFFFF')),
                stat_cell('WAKTU', stats['time']),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        padding=ft.Padding(16, 10, 16, 12),
        border=ft.border.only(top=ft.BorderSide(1, t.C_BORDER)),
    )

    ride_controls = ft.Container(
        content=ft.Row(
            controls=[
                ft.ElevatedButton(
                    'PAUSE',
                    icon=ft.Icons.PAUSE,
                    on_click=on_pause,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.06, '#FFFFFF'),
                        color=t.C_TEXT,
                        shape=ft.RoundedRectangleBorder(12),
                        side=ft.BorderSide(1, t.C_BORDER2),
                    ),
                    expand=True,
                ),
                ft.ElevatedButton(
                    'STOP',
                    icon=ft.Icons.STOP,
                    on_click=on_stop,
                    style=ft.ButtonStyle(
                        bgcolor=t.C_DANGER_DIM,
                        color=t.C_DANGER,
                        shape=ft.RoundedRectangleBorder(12),
                        side=ft.BorderSide(1, ft.Colors.with_opacity(0.25, '#FF4757')),
                    ),
                    expand=True,
                ),
            ],
            spacing=8,
        ),
        padding=ft.Padding(14, 8, 14, 12),
        animate=ft.Animation(300, 'ease'),
    )

    content_items = [speed_section, stats_row]

    card = ft.Container(
        content=ft.Column(
            controls=content_items,
            spacing=0,
        ),
        bgcolor=ft.Colors.with_opacity(0.96, '#0A0A12'),
        border_radius=t.R_CARD,
        border=ft.border.all(1, t.C_BORDER2),
    )

    return card
