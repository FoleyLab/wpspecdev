from .spectrum_driver import SpectrumDriver
import numpy as np



class TmmDriver(SpectrumDriver):
    """ Compute the absorption, scattering, and extinction spectra of a sphere using Mie theory
    
        Attributes
        ----------
            number_of_layers : int
                the number of layers in the multilayer
            
            number_of_wavelengths : int
                the number of wavelengths in the wavelength_array
                
            thickness_array : 1 x number_of_layers numpy array of floats
                the thickness of each layer
                
            material_array : 1 x number_of_layers numpy array of str
                the materia of each layer
                
            wavelength_array : numpy array of floats
                the array of wavelengths in meters over which you will compute the spectra
                
            incident_angle : float
                the incident angle of light relative to the normal to the multilayer (0 = normal incidence!)
                
            polarization : str
                indicates if incident light is 's' or 'p' polarized

            reflectivity_array : 1 x number_of_wavelengths numpy array of floats
                the reflection spectrum 

            transmissivity_array : 1 x number_of_wavelengths numpy array of floats
                the transmission spectrum

            emissivity_array : 1 x number_of_wavelengths numpy array of floats
                the absorptivity / emissivity spectrum
                
            _refraction_angle_array : 1 x number_of_layers numpy array of complex floats
                the incident and refraction angles for each layer, including incoming layer
                
            _cos_of_refraction_angle_array : 1 x number_of_layers numpy array of complex floats
                  
            _refractive_index_array : number_of_layers x number_of_wavelengths numpy array of complex floats
                the array of refractive index values corresponding to wavelength_array
                 
            _tm : 2 x 2 x number_of_wavelengths numpy array of complex floats
                the transfer matrix for each wavelength
                 
            _kz_array : 1 x number_lf_layers x number_of_wavelengths numpy array of complex floats
                the z-component of the wavevector in each layer of the multilayer for each wavelength 
              
            _k0_array : 1 x number_of_wavelengths numpy array of floats
                the wavevector magnitude in the incident layer for each wavelength
                  
            _kx_array : 1 x number_of_wavelengths numpy array of floats
                the x-component of the wavevector for each wavelength (conserved throughout layers)
                              
                 
            _pm : 2 x 2 x (number_of_layers-2) x number_of_wavelengths numpy array of complex floats
                the P matrix for each of the finite-thickness layers for each wavelength
                 
            _dm : 2 x 2 x number_of_layers x number_of_wavelengths numpy array of complex floats
                the D matrix for each of the layers for each wavelength
                 
            _dim : 2 x 2 x number_of_layers x number_of_wavelengts numpy array of complex floats
                the inverse of the D matrix for each of the layers for each wavelength

        Returns
        -------
            None
    
    """
    def __init__(self, thickness):
        """ constructor for the TmmDriver class
    
            Assign values for attributes thickness_array, material_array then call
            compute_spectrum to compute values for attributes reflectivity_array, 
            transmissivity_array, and emissivity_array
        
        """
        
        
        ''' hard-coded a lot of this for now, we will obviously generalize soon! '''
        self.thickness = thickness
        self.number_of_wavelengths = 10
        self.number_of_layers = 3
        self.wavelength_array = np.linspace(400e-9, 800e-9, self.number_of_wavelengths)
        self.wavenumber_array = 1/ self.wavelength_array
        self.thickness_array = np.array([0, thickness, 0])
        self.polarization = 's'
        self.incident_angle = 0.
        
        # pretty pythonic way to create the _refractive_index_array
        # that will result in self._refractive_index_array[1, 3] -> RI of layer index 1 (2nd layer) 
        # at wavelength index 3 (4th wavelength in wavelength_array)
        self._refractive_index_array = np.reshape(np.tile(np.array([1+0j, 1.5+0j, 1+0j]), self.number_of_wavelengths), 
                                                  (self.number_of_wavelengths, self.number_of_layers)) 
        
        


    def compute_spectrum(self):
        """ computes the following attributes:
            
            Attributes
            ----------
                reflectivity_array 
            
                transmissivity_array
            
                emissivity_array
            
            Returns
            -------
                None
                
            
            Will compute attributes by 
            
                - calling _compute_tm method
                
                - evaluating r amplitudes from _tm
                
                - evaluationg R from rr*
                
                - evaluating t amplitudes from _tm
                
                - evaluating T from tt* n_L cos(\theta_L) / n_1 cos(\theta_L)
        
        """
        # compute k0_array
        self._k0_array = np.pi * 2 / self.wavelength_array
        
        # compute kx_array
        self._kx_array = self._refractive_index_array[:, 0] * np.sin( self.incident_angle ) * self._k0_array 

        
        

        ref_times_wn = np.array([self.wavenumber_array[x]*self._refractive_index_array[x] for x in range(len(self.wavenumber_array))])
        
        self._kzl_array = np.sqrt((ref_times_wn)**2-(ref_times_wn*np.sin(self.incident_angle)**2))
        
        """ continute to compute remaining intermediate attributes needed by _compute_tm(), including
        
            - self._refraction_angle_array
            
            - self._cos_of_refraction_angle_array
        
            - self._kz_array
            
        """
        
        # with all of these formed, you can now call _compute_tm()
        self._tm = self._compute_tm()
        
    
    def _compute_kz(self):
        
        self._kz_array = np.sqrt((ml._refractive_index_array * ml._k0_array[:, np.newaxis])**2 - ml._kx_array[:,np.newaxis]**2)
    
    def _compute_tm(self):
        """ compute the transfer matrix for each wavelength
        
            Attributes
            ----------
                thickness_array
                
                _k0
                
                _kx
                
                _kz_array
                
                _refraction_angle_array
                
                _cos_of_refraction_angle_array
                
                _dm
                
                _pm
                
                _dim
                
            
                
            Returns
            -------
            _tm
                
        """
        M = np.linalg.eye((2,2),dtype=complex)
        for x in range(len(self.wavenumber_array)):
            for y in range(len(self.number_of_layers)):
                if x == 0 or x == len(self.wavenumber_array):
                    D = self._compute_dm(x,y)
                    M = np.matmul(M,D)
                    
                    
                

        print("can _compute_tm() see the _k0_array?", self._k0_array)
        print("can _compute_tm() see the _kz_array?", self._kz_array)
        
    

    
    def _compute_dm(self,idx, num_layers):
        
        """ compute the D and D_inv matrices for each layer and wavelength
        
            Attributes
            ----------
                refractive_index_array
                
                polarization
                
                _cos_of_refraction_angle_array
                
                _dm
                
                _dim
                

                
            Returns
            -------
            None
        """
        M = np.linalg.eye((2,2),dtype=complex)
        for i in range(len(num_layers)):


            D = np.zeros((2,2),dtype=complex)
            if (self.polarization == "s"):
                D[0][0] = 1.+0j
                D[0][1] = 1.+0j
                D[1][0] = np.cos(self.incident_angle)*self._refractive_index_array[idx][i]
                D[1][1] = -1*np.cos(self.incident_angle)*self._refractive_index_array[idx][i]


            elif (self.polarization == "p"):
                D[0][0] = np.cos(self.incident_angle+0j)
                D[0][1] = np.cos(self.incident_angle+0j)
                D[1][0] = self.refractive_index_array[idx][i]
                D[1][1] = -1*self.refractive_index_array[idx][i]

            else:
                
                print("needs polarization s or p")
            D_inv = 1/((D[0][0]*D[1][1])-(D[0][1]*D[1][0]))
            print(D)
        '''if idx == 0:
            det = D_inv
            #return np.linalg.inv(D)
            # Test manual inverse
        elif idx == len(self.wavenumber_array):
            return D
        else:
            #D = np.matmul(D,np.linalg.inv(D))
            D = np.matmul(D,det)
            return D
        '''
        P = _compute_pm(idx, i)
        
        if idx == 0:
            return D_inv

        elif idx == len(self.wavenumber_array):
            return D
        else:
            inner = np.dot(D_inv,np.dot(D, P))
            return inner
        



    def _compute_pm(self, idx, i):
        """ compute the P matrices for each intermediate-layer layer and wavelength
        
            Attributes
            ----------
                thickness_array
                
                _kz_array
                
                _pm
                

                
            Returns
            -------
            None
        """

        P = np.zeros((2,2),dtype=complex)
        ci = 0+1j

        a = -1*ci*self._kxz_array[idx] * self.thickness_array[idx][i]
        b = ci*self._kxz_array[idx] * self.thickness_array[idx][i]

        P[0][1] = 0+0j
        P[1][0] = 0+0j
        P[0][0] = np.exp(a)
        P[1][1] = np.exp(b)
        print(P)
        return P
             