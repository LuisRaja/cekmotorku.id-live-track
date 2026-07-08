import flet as ft
from . import theme as t
from .state import AppState
from .logic.websocket import WSClient
from .logic.tracking import TrackingManager
from .ui.header import build_header
from .ui.hud_card import build_hud_card
from .ui.live_row import build_live_row
from .ui.touring_sheet import build_touring_sheet
from .ui.bottom_nav import build_bottom_nav
from .ui.map_widget import build_map
from .ui.share_card import build_share_card


class CekMotormuApp:
    def __init__(self):
        self.page = None
        self.state = AppState()
        self.ws = WSClient()
        self.tracker = None

        self.header_row = None
        self.hud_container = None
        self.live_row_container = None
        self.touring_sheet_container = None
        self.nav_container = None
        self.map_column = None
        self.gps_dot = None

        self._sheet_open = True

    def build(self, page: ft.Page):
        self.page = page
        page.title = 'cekMotormu.id - Live Tracking & Speedometer'
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = t.C_BG
        page.padding = 0
        page.spacing = 0

        self.tracker = TrackingManager(self.state, self.ws, self._refresh)
        self.ws.connect()

        self._build_ui()
        page.update()

    def _build_ui(self):
        p = self.page

        map_ctrl, route_line, marker = build_map(self.state)

        map_area = ft.Stack(
            controls=[
                map_ctrl,
                ft.Container(
                    expand=True,
                    gradient=ft.LinearGradient(
                        colors=['#00000000', ft.Colors.with_opacity(0.8, '#000000')],
                        begin=ft.Alignment(0, 0),
                        end=ft.Alignment(0, 1),
                    ),
                ),
                # Dashboard overlay
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self._build_hud(),
                            self._build_live_row(),
                        ],
                        spacing=0,
                    ),
                    border_radius=t.R_CARD,
                    bottom=12, left=12, right=12,
                ),
                # Touring sheet
                ft.AnimatedContainer(
                    content=self._build_touring_sheet(),
                    visible=True,
                    bottom=0, left=0, right=0,
                ),
            ],
            expand=True,
        )

        self.header_row = build_header(p, self.state)
        self.nav_container = build_bottom_nav(self.state)

        main_col = ft.Column(
            controls=[
                self.header_row,
                map_area,
                self.nav_container,
            ],
            spacing=0,
            expand=True,
        )

        p.add(main_col)
        self._sheet_open = True

    def _build_hud(self):
        stats = self.state.get_stats()
        is_recording = self.state.is_tracking

        speed_text = ft.Text(
            str(stats['speed']),
            size=72, weight=ft.FontWeight.W_700,
            color=t.C_BRAND if stats['speed'] > 80 else t.C_TEXT,
            text_align=ft.TextAlign.CENTER,
        )

        speed_section = ft.Container(
            content=ft.Column([
                speed_text,
                ft.Text('KM/H', size=10, weight=ft.FontWeight.W_700,
                        letter_spacing=2.5, color=t.C_TEXT_3, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.Padding(20, 16, 20, 8),
        )

        def stat_cell(label, value, sub=''):
            return ft.Column([
                ft.Text(label, size=9, weight=ft.FontWeight.W_800,
                        letter_spacing=1, color=t.C_TEXT_3, text_align=ft.TextAlign.CENTER),
                ft.Text(str(value), size=17, weight=ft.FontWeight.W_700,
                        color=t.C_TEXT, text_align=ft.TextAlign.CENTER),
                ft.Text(sub, size=8, color=t.C_TEXT_3, text_align=ft.TextAlign.CENTER) if sub else ft.Container(height=8),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1)

        stats_row = ft.Container(
            content=ft.Row([
                stat_cell('TOP', stats['top_speed'], 'KM/H'),
                ft.Container(width=1, height=24, bgcolor=ft.Colors.with_opacity(0.05, '#FFFFFF')),
                stat_cell('JARAK', stats['distance'], 'KM'),
                ft.Container(width=1, height=24, bgcolor=ft.Colors.with_opacity(0.05, '#FFFFFF')),
                stat_cell('WAKTU', stats['time']),
            ], spacing=0, alignment=ft.MainAxisAlignment.SPACE_AROUND),
            padding=ft.Padding(16, 10, 16, 12),
            border=ft.border.only(top=ft.BorderSide(1, t.C_BORDER)),
        )

        controls = [speed_section, stats_row]

        self.hud_container = ft.Container(
            content=ft.Column(controls, spacing=0),
            bgcolor=t.C_SURFACE,
            border_radius=t.R_CARD,
            border=ft.border.all(1, t.C_BORDER2),
            visible=True,
        )
        return self.hud_container

    def _build_live_row(self):
        s = self.state
        if not s.is_tracking:
            self.live_row_container = ft.Container(visible=False)
            return self.live_row_container

        def cell(label, value, unit, color):
            return ft.Container(
                content=ft.Column([
                    ft.Text(label, size=8, weight=ft.FontWeight.W_800,
                            letter_spacing=0.8, color=t.C_TEXT_3, text_align=ft.TextAlign.CENTER),
                    ft.Text(str(value), size=16, weight=ft.FontWeight.W_700,
                            color=color, text_align=ft.TextAlign.CENTER),
                    ft.Text(unit, size=7, weight=ft.FontWeight.W_600,
                            color=t.C_TEXT_3, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
                expand=True,
            )

        def div():
            return ft.Container(width=1, height=24, bgcolor=ft.Colors.with_opacity(0.05, '#FFFFFF'))

        alt_val = f'{int(s.altitude)}' if s.altitude is not None else '--'

        self.live_row_container = ft.Container(
            content=ft.Row([
                cell('G-Force', s.g_force, 'g', '#FF6B6B'),
                div(),
                cell('Lean', s.lean_angle, '\u00b0', '#4ECDC4'),
                div(),
                cell('Alt', alt_val, 'm', '#45B7D1'),
                div(),
                cell('Apex', s.top_speed, 'km/h', '#FFD93D'),
            ], spacing=0, alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            padding=ft.Padding(12, 10, 12, 8),
            border=ft.border.only(top=ft.BorderSide(1, t.C_BORDER)),
            bgcolor=t.C_SURFACE,
            visible=True,
        )
        return self.live_row_container

    def _build_touring_sheet(self):
        s = self.state
        route_input = ft.TextField(
            hint_text='Contoh: Jakarta - Bandung', value=s.form_data['route'],
            text_size=12, color=t.C_TEXT,
            bgcolor=ft.Colors.with_opacity(0.04, '#FFFFFF'),
            border=ft.InputBorder.OUTLINE, border_color=t.C_BORDER,
            border_radius=10,
            on_change=lambda e: s.form_data.__setitem__('route', e.control.value),
        )
        motor_input = ft.TextField(
            hint_text='Nama Motor', value=s.form_data['motor'],
            text_size=12, color=t.C_TEXT,
            bgcolor=ft.Colors.with_opacity(0.04, '#FFFFFF'),
            border=ft.InputBorder.OUTLINE, border_color=t.C_BORDER,
            border_radius=10,
            on_change=lambda e: s.form_data.__setitem__('motor', e.control.value),
        )
        odo_input = ft.TextField(
            hint_text='KM Odometer', value=s.form_data['odometer'],
            text_size=12, color=t.C_TEXT,
            bgcolor=ft.Colors.with_opacity(0.04, '#FFFFFF'),
            border=ft.InputBorder.OUTLINE, border_color=t.C_BORDER,
            border_radius=10,
            on_change=lambda e: s.form_data.__setitem__('odometer', e.control.value),
        )
        notes_input = ft.TextField(
            hint_text='Catatan touring...', value=s.form_data['notes'],
            text_size=12, color=t.C_TEXT,
            bgcolor=ft.Colors.with_opacity(0.04, '#FFFFFF'),
            border=ft.InputBorder.OUTLINE, border_color=t.C_BORDER,
            border_radius=10,
            multiline=True, min_lines=2, max_lines=3,
            on_change=lambda e: s.form_data.__setitem__('notes', e.control.value),
        )

        form = ft.Column([
            ft.Text('TOURING SETUP', size=10, weight=ft.FontWeight.W_800,
                    letter_spacing=1.5, color=t.C_TEXT_2),
            ft.Column([ft.Text('Nama Rute', size=9, weight=ft.FontWeight.W_700,
                               letter_spacing=1, color=t.C_TEXT_3), route_input], spacing=4),
            ft.Row([
                ft.Column([ft.Text('Motor', size=9, weight=ft.FontWeight.W_700,
                                   letter_spacing=1, color=t.C_TEXT_3), motor_input], spacing=4, expand=True),
                ft.Column([ft.Text('ODO Awal', size=9, weight=ft.FontWeight.W_700,
                                   letter_spacing=1, color=t.C_TEXT_3), odo_input], spacing=4, expand=True),
            ], spacing=10),
            ft.Column([ft.Text('Catatan', size=9, weight=ft.FontWeight.W_700,
                               letter_spacing=1, color=t.C_TEXT_3), notes_input], spacing=4),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED, size=16, color=t.C_BRAND),
                    ft.Text('Pasang Foto Latar', size=12, weight=ft.FontWeight.W_600, color=t.C_BRAND),
                ], spacing=8),
                padding=ft.Padding(14, 10, 14, 10),
                border=ft.border.all(2, ft.Colors.with_opacity(0.25, '#BDFF00'), ft.BorderStyle.DASHED),
                border_radius=12,
            ),
        ], spacing=10)

        self.touring_sheet_container = ft.Container(
            content=form,
            padding=ft.Padding(16, 4, 16, 20),
            bgcolor=t.C_SURFACE,
            border=ft.border.only(top=ft.BorderSide(1, t.C_BORDER2)),
            border_radius=ft.border_radius.only(top_left=22, top_right=22),
        )
        return self.touring_sheet_container

    def _refresh(self):
        if not self.page:
            return
        try:
            self._rebuild_dashboard()
            self.page.update()
        except Exception:
            pass

    def _rebuild_dashboard(self):
        pass

    def _toggle_sheet(self):
        self._sheet_open = not self._sheet_open
        if self.touring_sheet_container:
            self.touring_sheet_container.offset = ft.Offset(0, 0) if self._sheet_open else ft.Offset(0, 2)
            self.page.update()
