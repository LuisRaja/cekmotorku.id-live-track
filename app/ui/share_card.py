import flet as ft
import random
import math
from .. import theme as t
from ..utils.helpers import format_time


def build_share_card(state):
    s = state
    avg_speed = s.get_avg_speed()
    elapsed = s.elapsed_seconds
    route_name = s.form_data.get('route', 'Rute Aktif') or 'Rute Aktif'
    motor_name = s.form_data.get('motor', '-') or '-'
    notes = s.form_data.get('notes', '')
    odometer = s.form_data.get('odometer', '')

    avg_lean = min(45, round(avg_speed * 0.3))
    est_elevation = round(s.total_distance * 7 + random.random() * 50)

    def share_row(label, value):
        return ft.Row(
            controls=[
                ft.Text(label, size=9, weight=ft.FontWeight.W_600,
                        color=t.C_TEXT_3, letter_spacing=0.5),
                ft.Text(value or '-', size=9, weight=ft.FontWeight.W_600,
                        color=t.C_TEXT),
            ],
            spacing=6,
        )

    # Generate elevation mini chart SVG path
    pts = 6
    elev_d = ''
    for i in range(pts + 1):
        x = (i / pts) * 100
        base = 14 - (i / pts) * 8
        noise = math.sin(i * 1.5) * 4 + random.random() * 2
        y = max(1, min(17, base + noise))
        elev_d += f'{"M" if i == 0 else " L"}{x:.0f},{y:.1f}'

    # Speed chart
    speed_d = ''
    if s.speeds:
        pts2 = min(10, len(s.speeds))
        for i in range(pts2 + 1):
            x = (i / pts2) * 100
            idx = min(int((i / pts2) * len(s.speeds)), len(s.speeds) - 1)
            spd_val = s.speeds[idx] if idx < len(s.speeds) else 0
            max_s = max(s.speeds, default=1)
            y = 18 - (spd_val / max_s) * 15
            speed_d += f'{"M" if i == 0 else " L"}{x:.0f},{y:.1f}'

    share_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(route_name.upper(), size=14, weight=ft.FontWeight.W_900,
                        color=t.C_TEXT, letter_spacing=1),
                ft.Container(height=4),
                share_row('Motor', motor_name),
                ft.Container(height=2),
                share_row('Rute', route_name),
                ft.Container(height=2),
                share_row('ODO Awal', odometer),
                ft.Container(height=4),

                # Stats row
                ft.Row(
                    controls=[
                        ft.Column([
                            ft.Text(str(s.total_distance), size=18, weight=ft.FontWeight.W_700,
                                    color=t.C_BRAND, text_align=ft.TextAlign.CENTER),
                            ft.Text('KM', size=8, color=t.C_TEXT_3,
                                    text_align=ft.TextAlign.CENTER),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Container(width=1, height=30, bgcolor=ft.Colors.with_opacity(0.1, '#FFFFFF')),
                        ft.Column([
                            ft.Text(str(est_elevation), size=18, weight=ft.FontWeight.W_700,
                                    color='#45B7D1', text_align=ft.TextAlign.CENTER),
                            ft.Text('ELEV', size=8, color=t.C_TEXT_3,
                                    text_align=ft.TextAlign.CENTER),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Container(width=1, height=30, bgcolor=ft.Colors.with_opacity(0.1, '#FFFFFF')),
                        ft.Column([
                            ft.Text(format_time(elapsed)[:5], size=18, weight=ft.FontWeight.W_700,
                                    color=t.C_TEXT, text_align=ft.TextAlign.CENTER),
                            ft.Text('TIME', size=8, color=t.C_TEXT_3,
                                    text_align=ft.TextAlign.CENTER),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                ft.Container(height=6),

                # Mini charts
                ft.Container(
                    content=ft.Column([
                        ft.Text('Elevation Profile', size=8, weight=ft.FontWeight.W_600,
                                color=t.C_TEXT_3, letter_spacing=0.5),
                        ft.Container(
                            content=ft.Row([ft.Container(height=20)], expand=True),
                            height=20,
                        ),
                    ]),
                ),
                ft.Container(height=4),

                ft.Row(
                    controls=[
                        ft.Text(f'Top Speed: {s.top_speed} km/h', size=8,
                                weight=ft.FontWeight.W_700, color=t.C_TEXT_3),
                        ft.Text(f'Lean Angle Avg: {avg_lean}\u00b0', size=8,
                                weight=ft.FontWeight.W_700, color=t.C_TEXT_3),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=2),

                share_row('ODO Awal', odometer),
                ft.Container(height=4),

                # Histogram bars
                ft.Container(
                    content=ft.Column([
                        ft.Text('Consistency Intervals (per segmen)', size=8,
                                weight=ft.FontWeight.W_600, color=t.C_TEXT_3,
                                letter_spacing=0.5),
                        ft.Text(f'Peak: {s.top_speed}', size=8,
                                weight=ft.FontWeight.W_600, color=t.C_TEXT_3),
                    ]),
                ),
                ft.Container(height=4),

                # Notes
                share_row('Catatan', notes or '-'),

                ft.Container(height=6),
                ft.Text('cekMotormu.id', size=9, weight=ft.FontWeight.W_600,
                        color=t.C_TEXT_3, letter_spacing=1),
            ],
            spacing=0,
        ),
        padding=ft.Padding(20, 20, 20, 20),
        bgcolor='#0A0A12',
        border_radius=16,
        border=ft.border.all(1, ft.Colors.with_opacity(0.1, '#FFFFFF')),
    )

    return ft.Container(
        content=share_content,
        padding=ft.Padding(16, 16, 16, 16),
    )
