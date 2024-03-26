#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import NoReturn
from PyMieSim.experiment.source import Gaussian
from PyMieSim.gui.base_tab import BaseTab
from PyMieSim.gui.utils import Widget, WidgetCollection


class SourceTab(BaseTab):
    """
    A GUI tab for configuring the light source parameters for simulations in PyMieSim.

    This class provides a user interface for setting up the light source by specifying
    parameters such as wavelength, polarization, optical power, and numerical aperture (NA).
    User inputs are used to configure a Gaussian light source in the simulation.

    Attributes:
        variables (WidgetCollection): A collection of widgets for source configuration.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the SourceTab with UI components for source configuration.

        Parameters:
            *args: Variable length argument list for BaseTab.
            **kwargs: Arbitrary keyword arguments for BaseTab.
        """
        self._init_widgets()

        super().__init__(*args, **kwargs)

    def _init_widgets(self):
        """Initializes widgets for source configuration with default values and labels."""
        self.widget_collection = WidgetCollection(
            Widget(default_value='400:950:200', label='Wavelength [nm]', component_label='wavelength', multiplicative_factor=1e-9),
            Widget(default_value='0', label='Polarization angle [degree]', component_label='polarization_value'),
            Widget(default_value='1.0', label='Optical Power [mW]', component_label='optical_power', multiplicative_factor=1e-3),
            Widget(default_value='0.2', label='Numerical Aperture (NA)', component_label='NA')
        )

    def setup_tab(self) -> NoReturn:
        """
        Configures the GUI elements for the Source tab.

        This method sets up labels and entry fields for each source parameter, facilitating
        user interaction for the configuration of the light source.
        """
        self.widget_collection.setup_widgets(frame=self.frame)
        self.setup_component()

    def setup_component(self) -> NoReturn:
        """
        Initializes the Gaussian source component based on user input.

        This method reads input values from the UI widgets and uses them to configure
        a Gaussian source component for the simulation.
        """
        self.update_user_input()
        self.component = Gaussian(**self.widget_collection.to_component_dict())
        self._update_mapping()

    def _update_mapping(self):
        """
        Updates the mapping attribute with current component values.

        This private method extracts relevant parameters from the configured Gaussian
        component and updates the mapping attribute to reflect these values.
        """
        self.mapping = {
            'wavelength': self.component.wavelength,
            'polarization': self.component.polarization_value
        }
