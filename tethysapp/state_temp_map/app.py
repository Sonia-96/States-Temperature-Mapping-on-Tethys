from tethys_sdk.base import TethysAppBase
from tethys_sdk.app_settings import SpatialDatasetServiceSetting


class StateTempMap(TethysAppBase):
    """
    Tethys app class for States Temprature Mapping.
    """

    name = 'States Population & Temperature'
    description = 'U.S. States Population & Temperature Mapping'
    package = 'state_temp_map'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/icon.png'
    root_url = 'state-temp-map'
    color = '#003087'
    tags = 'Temperature, Timesetires'
    enable_feedback = False
    feedback_emails = []

    def spatial_dataset_service_settings(self):
        """
        Example spatial_dataset_service_settings method.
        """
        sds_settings = (
            SpatialDatasetServiceSetting(
                name='primary_geoserver',
                description='spatial dataset service for app to use',
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=True,
            ),
        )

        return sds_settings