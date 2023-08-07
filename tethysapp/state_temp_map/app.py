from tethys_sdk.base import TethysAppBase


class StateTempMap(TethysAppBase):
    """
    Tethys app class for States Temprature Mapping.
    """

    name = 'States Temprature Mapping'
    description = 'US States Temperature Mapping'
    package = 'state_temp_map'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/icon.gif'
    root_url = 'state-temp-map'
    color = '#003087'
    tags = 'Temperature, Timesetires'
    enable_feedback = False
    feedback_emails = []