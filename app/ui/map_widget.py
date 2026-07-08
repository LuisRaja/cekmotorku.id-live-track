from flet_map import Map, TileLayer, MapLatitudeLongitude, PolylineLayer, PolylineMarker, MarkerLayer, Marker

DEFAULT_CENTER = MapLatitudeLongitude(-6.2088, 106.8456)


def build_map(state):
    tile = TileLayer(
        url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    )

    route_line = PolylineMarker(
        points=[],
        color='#BDFF00',
        stroke_width=5,
    )

    polyline_layer = PolylineLayer(polylines=[route_line])

    marker = Marker(
        content=None,
        coordinates=DEFAULT_CENTER,
    )

    marker_layer = MarkerLayer(markers=[marker])

    map_ctrl = Map(
        initial_center=DEFAULT_CENTER,
        initial_zoom=15,
        layers=[tile, polyline_layer, marker_layer],
        expand=True,
    )

    return map_ctrl, route_line, marker
