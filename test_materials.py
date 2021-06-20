"""
Unit tests for the Materials class
"""

# Import package, test suite, and other packages as needed
import wpspecdev
import numpy as np
import pytest
import sys

material_test = wpspecdev.Materials()

    
def test_material_sio2():
    """ tests material_sio2 method using tabulated n and k at lambda=636 nm """
    
    expected_n = 1.45693 
    expected_k = 0.00000 
  
    # create test multilayer that has 3 layers and wavelength array centered at 636 nm 
    material_test._create_test_multilayer(central_wavelength=636e-9)
    # define central layer as SiO2
    material_test.material_SiO2(1)

    result_n = np.real(material_test._refractive_index_array[1,1])
    result_k = np.imag(material_test._refractive_index_array[1,1]) 

    assert np.isclose(result_n, expected_n, 1e-3)
    assert np.isclose(result_k, expected_k, 1e-3)


def test_material_tio2():
    """ tests material_tio2 method using tabulated n and k at lambda=664 nm """
    expected_n = 2.377021563
    expected_k = 6.79E-10

    # create test multilayer that has 3 layers and wavelength array centered at 664 nm 
    material_test._create_test_multilayer(central_wavelength=664e-9)
    # define central layer as TiO2
    material_test.material_TiO2(1)

    result_n = np.real(material_test._refractive_index_array[1,1])
    result_k = np.imag(material_test._refractive_index_array[1,1])

    assert np.isclose(result_n, expected_n, 1e-3)
    assert np.isclose(result_k, expected_k, 1e-3)

def test_material_ta2o5():
    """ tests material_Ta2O5 method using tabulated n and k at lambda=667 nm: 
        6.6782e-07 2.1137e+00 1.0506e-03 """
    expected_n = 2.1137e+00
    expected_k = 1.0506e-03

    # create test multilayer that has 3 layers and wavelength array centered at 647 nm 
    material_test._create_test_multilayer(central_wavelength=6.6782e-07)
    # define central layer as Ta2O5
    material_test.material_Ta2O5(1)

    result_n = np.real(material_test._refractive_index_array[1,1])
    result_k = np.imag(material_test._refractive_index_array[1,1])

    assert np.isclose(result_n, expected_n, 1e-3)
    assert np.isclose(result_k, expected_k, 1e-3)

def test_material_tin():
    """ tests material_TiN method using tabulated n and k at lambda=1106 nm 
        1.106906906906907e-06 2.175019337515494 5.175973473259225 """

    expected_n = 2.175019337515494
    expected_k = 5.175973473259225

    # create test multilayer that has 3 layers and wavelength array centered at 664 nm 
    material_test._create_test_multilayer(central_wavelength=1.106906906906907e-06)
    # define central layer as TiN
    material_test.material_TiN(1)

    result_n = np.real(material_test._refractive_index_array[1,1])
    result_k = np.imag(material_test._refractive_index_array[1,1])

    assert np.isclose(result_n, expected_n, 1e-3)
    assert np.isclose(result_k, expected_k, 1e-3)

def test_material_Al():
    """ tests material_Al method using tabulated n and k at lambda=206.64 nm 
        2.0664E-01 1.2677E-01 2.3563E+00 """

    expected_n = 1.2677E-01
    expected_k = 2.3563E+00

    # create test multilayer that has 3 layers and wavelength array centered at 206 nm 
    material_test._create_test_multilayer(central_wavelength=2.0664E-01)
    # define central layer as TiN
    material_test.material_Al(1)

    result_n = np.real(material_test._refractive_index_array[1,1])
    result_k = np.imag(material_test._refractive_index_array[1,1])

    assert np.isclose(result_n, expected_n, 1e-3)
    assert np.isclose(result_k, expected_k, 1e-3)


def test_material_W():
    """ tests material_W method using tabulated n and k at lambda=4000.00 nm 
        4.00 1.9949739 17.694770 """

    expected_n = 1.9949739
    expected_k = 17.694770

    # create test multilayer that has 3 layers and wavelength array centered at 4000 nm 
    material_test._create_test_multilayer(central_wavelength=4.000)
    # define central layer as W
    material_test.material_W(1)

    result_n = np.real(material_test._refractive_index_array[1,1])
    result_k = np.imag(material_test._refractive_index_array[1,1])

    assert np.isclose(result_n, expected_n, 1e-3)
    assert np.isclose(result_k, expected_k, 1e-3)

def test_material_AlN():
    """ tests material_AlN method using tabulated n and k at lambda=2965.60 nm 
        2.96560 2.00739 0.00018 """

    expected_n = 2.00739
    expected_k = 0.00018

    # create test multilayer that has 3 layers and wavelength array centered at 2965.6 nm 
    material_test._create_test_multilayer(central_wavelength=2.96560)
    # define central layer as AlN
    material_test.material_AlN(1)

    result_n = np.real(material_test._refractive_index_array[1,1])
    result_k = np.imag(material_test._refractive_index_array[1,1])

    assert np.isclose(result_n, expected_n, 1e-3)
    assert np.isclose(result_k, expected_k, 1e-3)