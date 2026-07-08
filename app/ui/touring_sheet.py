import flet as ft
from .. import theme as t
from ..state import AppState

def build_touring_sheet(page, state):
    route_input = ft.TextField(
        hint_text='Contoh: Jakarta - Bandung',
        value=state.form_data['route'],
        text_size=12,
        color=t.C_TEXT,
        bgcolor=ft.Colors.with_opacity(0.04, '#FFFFFF'),
        border=ft.InputBorder.OUTLINE,
        border_color=t.C_BORDER,
        border_radius=10,
        focused_border_color=t.C_BRAND_GLOW,
        content_padding=ft.Padding(12, 10, 12, 10),
        on_change=lambda e: state.form_data.__setitem__('route', e.control.value),
    )

    motor_input = ft.TextField(
        hint_text='Nama Motor',
        value=state.form_data['motor'],
        text_size=12,
        color=t.C_TEXT,
        bgcolor=ft.Colors.with_opacity(0.04, '#FFFFFF'),
        border=ft.InputBorder.OUTLINE,
        border_color=t.C_BORDER,
        border_radius=10,
        focused_border_color=t.C_BRAND_GLOW,
        content_padding=ft.Padding(12, 10, 12, 10),
        on_change=lambda e: state.form_data.__setitem__('motor', e.control.value),
    )

    odo_input = ft.TextField(
        hint_text='KM Odometer',
        value=state.form_data['odometer'],
        text_size=12,
        color=t.C_TEXT,
        bgcolor=ft.Colors.with_opacity(0.04, '#FFFFFF'),
        border=ft.InputBorder.OUTLINE,
        border_color=t.C_BORDER,
        border_radius=10,
        focused_border_color=t.C_BRAND_GLOW,
        content_padding=ft.Padding(12, 10, 12, 10),
        on_change=lambda e: state.form_data.__setitem__('odometer', e.control.value),
    )

    notes_input = ft.TextField(
        hint_text='Catatan touring...',
        value=state.form_data['notes'],
        text_size=12,
        color=t.C_TEXT,
        bgcolor=ft.Colors.with_opacity(0.04, '#FFFFFF'),
        border=ft.InputBorder.OUTLINE,
        border_color=t.C_BORDER,
        border_radius=10,
        focused_border_color=t.C_BRAND_GLOW,
        content_padding=ft.Padding(12, 10, 12, 10),
        multiline=True,
        min_lines=2,
        max_lines=3,
        on_change=lambda e: state.form_data.__setitem__('notes', e.control.value),
    )

    photo_container = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED, size=16, color=t.C_BRAND),
                ft.Text('Pasang Foto Latar', size=12, weight=ft.FontWeight.W_600, color=t.C_BRAND),
            ],
            spacing=8,
        ),
        padding=ft.Padding(14, 10, 14, 10),
        border=ft.border.all(2, ft.Colors.with_opacity(0.25, '#BDFF00'), ft.BorderStyle.DASHED),
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.03, '#FFFFFF'),
    )

    form_content = ft.Column(
        controls=[
            ft.Text('TOURING SETUP', size=10, weight=ft.FontWeight.W_800,
                    letter_spacing=1.5, color=t.C_TEXT_2),
            _form_group('Nama Rute', route_input),
            ft.Row(
                controls=[
                    ft.Column([_form_group('Motor', motor_input)], expand=True),
                    ft.Column([_form_group('ODO Awal', odo_input)], expand=True),
                ],
                spacing=10,
            ),
            _form_group('Catatan', notes_input),
            photo_container,
        ],
        spacing=10,
    )

    return ft.Container(
        content=form_content,
        padding=ft.Padding(16, 4, 16, 20),
        bgcolor=t.C_SURFACE,
        border=ft.border.only(top=ft.BorderSide(1, t.C_BORDER2)),
        border_radius=ft.border_radius.only(top_left=22, top_right=22),
        shadow=ft.BoxShadow(0, -16, ft.Colors.with_opacity(0.6, '#000000'), blur_radius=48),
    )

def _form_group(label, control):
    return ft.Column(
        controls=[
            ft.Text(label, size=9, weight=ft.FontWeight.W_700,
                    letter_spacing=1, color=t.C_TEXT_3),
            control,
        ],
        spacing=4,
    )
