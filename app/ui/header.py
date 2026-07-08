from .. import theme as t

def build_header(page, state):
    gps_dot = t.C_TEXT_3  # placeholder

    import flet as ft

    return ft.Row(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        width=30, height=30,
                        bgcolor=t.C_BRAND_DIM,
                        border=ft.border.all(1, t.C_BRAND_GLOW),
                        border_radius=12,
                        content=ft.Icon(ft.Icons.MOTORCYCLE_OUTLINED,
                                        size=15, color=t.C_BRAND),
                        shadow=ft.BoxShadow(0, 0, ft.Colors.with_opacity(0.12, '#BDFF00'), blur_radius=12),
                    ),
                    ft.Row(
                        controls=[
                            ft.Text('cek', size=14, weight=ft.FontWeight.W_700,
                                    letter_spacing=-0.2, color=t.C_TEXT),
                            ft.Text('Motormu', size=14, weight=ft.FontWeight.W_700,
                                    letter_spacing=-0.2, color=t.C_BRAND),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=10,
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        width=6, height=6,
                        border_radius=3,
                        bgcolor=t.C_TEXT_3,
                    ),
                    ft.Text('GPS', size=8, weight=ft.FontWeight.W_700,
                            color=t.C_TEXT_2, letter_spacing=0.6),
                ],
                spacing=5,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
