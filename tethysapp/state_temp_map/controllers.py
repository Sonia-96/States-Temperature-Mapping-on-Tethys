import json
from pathlib import Path
from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import StateTempMap as app

@controller(name="home", app_workspace=True)
class StateTempMap(MapLayout):
    app = app
    base_template = 'state_temp_map/base.html'
    map_title = 'U.S. States Temprature'
    map_subtitle = ''

    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs):
        """
        Add layers to the MapLayout and create associated layer group objects.
        """
        # Load GeoJSON from files
        input_directory = Path(app_workspace.path) / 'states_temp' / 'input'

        # Nexus Points
        states_path = input_directory / 'us-states-5m_4326.json'
        with open(states_path) as file:
            states_geojson = json.loads(file.read())

        geojson_layer = self.build_geojson_layer(
            geojson=states_geojson,
            layer_name='states',
            layer_title='States',
            layer_variable='states',
            visible=True,
            selectable=True,
            plottable=True,
        )

        # Create layer groups
        layer_groups = [
            self.build_layer_group(
                id='states-path',
                display_name='GeoJSON Layer',
                layer_control='radio',  # 'checkbox' or 'radio'
                layers=[
                    geojson_layer,
                ]
            )
        ]

        return layer_groups