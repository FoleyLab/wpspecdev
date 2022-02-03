"""
Unit and regression test for the wpspec package.
"""

# Import package, test suite, and other packages as needed
import wpspecdev
import numpy as np
import pytest
import sys


def test_compute_power_density():
    test_args = {
        "wavelength_list": [100e-9, 30000e-9, 10000],
        "material_list": ["Air", "W", "Air"],
        "thickness_list": [0, 800e-9, 0],
        "temperature": 1500,
        "therml": True,
    }
    sf = wpspecdev.SpectrumFactory()
    test = sf.spectrum_factory("Tmm", test_args)

    """will test _compute_power_density method to
    see if the power density computed by integration
    of the blackbody spectrum is close to the prediction
    by the Stefan-Boltzmann law, where the latter should be exact
    """
    assert np.isclose(test.blackbody_power_density, test.stefan_boltzmann_law, 1e-2)


def test_compute_stpv_power_density():

    # define basic structure at 1500 K
    test_args = {
        "wavelength_list": [400e-9, 7000e-9, 1000],
        "material_list": ["Air", "TiN", "Air"],
        "thickness_list": [0, 400e-9, 0],
        "temperature": 5000,
        "therml": True,
    }
    sf = wpspecdev.SpectrumFactory()
    test = sf.spectrum_factory("Tmm", test_args)
    """will test _compute_stpv_power_density method to
    see if the power density computed by integration
    of the thermal emission spectrum of TiN at 5000 K is close to 
    the value that is generated by v1.0.0 of wptherml
    """
    assert np.isclose(test.stpv_power_density, 3863945.0, 1e4)


def test_compute_stpv_efficiency():
    # define basic structure at 1500 K
    test_args = {
        "wavelength_list": [400e-9, 7000e-9, 1000],
        "material_list": ["Air", "TiN", "Air"],
        "thickness_list": [0, 400e-9, 0],
        "temperature": 5000,
        "therml": True,
    }
    sf = wpspecdev.SpectrumFactory()
    test = sf.spectrum_factory("Tmm", test_args)
    """will test _compute_stpv_power_density method to
    see if the power density computed by integration
    of the thermal emission spectrum of TiN at 5000 K is close to 
    the value that is generated by v1.0.0 of wptherml
    """
    assert np.isclose(test.stpv_spectral_efficiency, 0.1074296366771825, 1e-2)


def test_compute_luminous_efficiency():
    # define basic structure at 1500 K
    test_args = {
        "wavelength_list": [400e-9, 7000e-9, 1000],
        "material_list": ["Air", "TiN", "Air"],
        "thickness_list": [0, 400e-9, 0],
        "temperature": 5000,
        "therml": True,
    }
    sf = wpspecdev.SpectrumFactory()
    test = sf.spectrum_factory("Tmm", test_args)
    """will test _compute_stpv_power_density method to
    see if the power density computed by integration
    of the thermal emission spectrum of TiN at 5000 K is close to 
    the value that is generated by v1.0.0 of wptherml
    """
    assert np.isclose(test.luminous_efficiency, 0.20350729803724107, 1e-2)