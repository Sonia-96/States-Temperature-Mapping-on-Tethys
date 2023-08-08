import json
from pathlib import Path
import pandas as pd
from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import StateTempMap as app

MODEL_OUTPUT_FOLDER_NAME = 'states_temp'

@controller(name="home", app_workspace=True)
class StateTempMap(MapLayout):
    app = app
    base_template = 'state_temp_map/base.html'
    map_title = 'U.S. States Temprature'
    map_subtitle = ''
    show_properties_popup = True
    plot_slide_sheet = True

    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs):
        """
        Add layers to the MapLayout and create associated layer group objects.
        """

        # WMS Layer
        usa_population = self.build_wms_layer(
            endpoint='http://localhost:8080/geoserver/wms',
            server_type='geoserver',
            layer_name='topp:states',
            layer_title='USA Population',
            layer_variable='population',
            visible=False,  # Set to False if the layer should be hidden initially
            selectable=True,
            geometry_attribute='the_geom',
            excluded_properties=['STATE_FIPS', 'SUB_REGION'],
        )

        # Add layer to map
        map_view.layers.append(usa_population)

        # Load GeoJSON from files
        input_directory = Path(app_workspace.path) / MODEL_OUTPUT_FOLDER_NAME / 'input'

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
            excluded_properties=['GEO_ID', 'STATE', 'LSAD']
        )

        # Create layer groups
        layer_groups = [
            self.build_layer_group(
                id='states-path',
                display_name='GeoJSON Layer',
                layer_control='radio',  # 'checkbox' or 'radio'
                layers=[
                    usa_population,
                    geojson_layer,
                ]
            )
        ]

        return layer_groups

    # TODO what is classmethod?
    # @classmethod
    # def get_vector_style_map(cls):
    #     pass

    def get_plot_for_layer_feature(self, request, layer_name, feature_id, layer_data, feature_props, app_workspace,
                                *args, **kwargs):
        """
        Retrieves plot data for given feature on given layer.

        Args:
            layer_name (str): Name/id of layer.
            feature_id (str): ID of feature.
            layer_data (dict): The MVLayer.data dictionary.
            feature_props (dict): The properties of the selected feature.

        Returns:
            str, list<dict>, dict: plot title, data series, and layout options, respectively.
        """
        output_directory = Path(app_workspace.path) / MODEL_OUTPUT_FOLDER_NAME / 'output'

        # Get the feature id
        name = feature_props.get('NAME')

        layout = {
            'yaxis': {
                'title': 'Temperature (°F)'
            }, 
            'xaxis': {
                'title': 'Year'
            }
        }

        output_path = output_directory / f'{name}.csv'
        if not output_path.exists():
            print(f'WARNING: no such file {output_path}')
            return f'No Data Found for "{name}"', [], layout
        
        # parse with pandas
        df = pd.read_csv(output_path)
        data = [
            {
                    'name': 'Temperature',
                    'mode': 'lines',
                    'x': df['Year'].to_list(),
                    'y': df.iloc[:, 1].to_list(),
                    'line': {
                        'width': 2,
                        'color': 'red'
                    }
                },
        ]

        return f'Evapotranspiration at Catchment "{name}"', data, layout

            
