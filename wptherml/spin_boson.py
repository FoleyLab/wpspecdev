import numpy as np
from matplotlib import pyplot as plt
from .spectrum_driver import SpectrumDriver


class SpinBosonDriver(SpectrumDriver):
    """A class for computing the dynamics and spectra of coupled exciton-boson (e.g. QD - plasmon, exciton-polariton, etc) systems using 
       the spin boson for N 2-level systems coupled to an N'-level Harmonic oscillator 

    Attributes
    ----------
    number_of_excitons : int
        number of excitonic subsystems
    
    number_of_boson_levels : int
        number of boson levels

    exciton_energy_ev : float
        energy of each exciton subsystem in eV

    boson_energy_ev : float
        fundamental energy of the boson subsystem in eV

    exciton_energy_au : float
        energy of each exciton subsystem in atomic units

    boson_energy_au : float
        fundamental energy of the boson subsystem in atomic units

    exciton_boson_coupling_ev : float
        coupling between each exciton subsystem and the boson subsystem in eV

    exciton_boson_coupling_au : float
        coupling between each exciton subsystem and the boson subsystem in atomic units
        
    single_exciton_basis : numpy matrix
        basis states for a single excition

    n_exciton_basis : numpy matrix
        basis states for the collection of N excitons

    boson_basis : numpy matrix
        basis states for the N-level Harmonic oscillator

    exciton_boson_basis : numpy matrix
        basis states for the collection of N excitons and the N'-level Harmonic oscillator


    Returns
    -------
    None

    Examples
    --------
    >>> fill_in_with_actual_example!
    """

    def __init__(self, args):
        """ constructor for the SpinBosonDriver class
        """
        # make sure all keys are lowercase only
        args = {k.lower(): v for k, v in args.items()}

        # conversion from eV to atomic units
        self.ev_to_au = 3.6749322175665e-2

        # parse user inputs
        self.parse_input(args)


    def parse_input(self, args):
        if "number_of_excitons" in args:
            self.number_of_excitons = args["number_of_excitons"]
        else:
            self.exciton_energy = 1

        if "number_of_boson_levels" in args:
            self.number_of_boson_levels = args["number_of_boson_levels"]
        else:
            self.number_of_boson_levels = 2 # includes |0> and |1>

        if "exciton_energy_ev" in args:
           self.exciton_energy_ev = args["exciton_energy_ev"]
        else:
           self.exciton_energy_ev = 1.0
        
        if "boson_energy_ev" in args:
           self.boson_energy_ev = args["boson_energy_ev"]
        else:
           self.boson_energy_ev = 1.0

        # convert energies from eV to au
        self.exciton_energy_au = self.exciton_energy_ev * self.ev_to_au
        self.boson_energy_au = self.boson_energy_ev * self.ev_to_au


    def build_boson_basis(self):
        """ build the basis for the N-level Harmonic oscillator

        Args
        ------
        None

        Attributes
        ----------
        number_of_boson_levels : int
            number of boson levels

        boson_basis : numpy matrix
            basis states for the N-level Harmonic oscillator

        Returns
        -------
        None
        
        """
        self.boson_basis = np.eye(self.number_of_boson_levels)

    def build_exciton_basis(self):
      """ build the basis for the N excitonic subsystems

      Args
      ------
      None

      Attributes
      ----------
      number_of_excitons : int
          number of excitonic subsystems

      single_exciton_basis : numpy matrix
          basis states for a single excition

      exciton_basis_dimension : int
          dimension of the N-exciton hilbert space

      n_exciton_basis : numpy matrix
          basis states for the collection of N excitons

      Returns
      -------
      None
      
      """

      self.single_exciton_basis = np.matrix('1 0 ; 0 1')
      self.exciton_basis_dimension = 2 ** self.number_of_excitons
      self.n_exciton_basis = np.eye(self.exciton_basis_dimension)
      
    def build_exciton_boson_basis(self):
      """ build the basis for the N excitonic subsystems and the N'-level Harmonic oscillator in order 
          |s> \otimes |q_1> \otimes |q_2> \otimes ... \otimes |q_N>

      Arguments
      ----------
      None

      Attributes
      ----------
      n_exciton_basis : numpy matrix
          basis states for the collection of N excitons

      boson_basis : numpy matrix
          basis states for the N'-level Harmonic oscillator

      exciton_boson_basis : numpy matrix
          basis states for the collection of N excitons and the N'-level Harmonic oscillator in order 
          |s> \otimes |q_1> \otimes |q_2> \otimes ... \otimes |q_N>

      Returns
      -------
      None
      
      """
      self.exciton_boson_basis = np.kron(self.boson_basis, self.n_exciton_basis)

    def build_bosonic_ladder_operators(self):
      """ build the bosonic raising and lowering operators

      Arguments
      ----------
      None

      Attributes
      ----------
      number_of_boson_levels : int
          number of boson levels

      b_matrix : numpy matrix
          matrix representation of the lowering operator

      b_dagger_matrix : numpy matrix
          matrix representation of the raising operator


      Returns
      -------
      None
      
      """
      self.b_matrix = np.zeros((self.number_of_boson_levels, self.number_of_boson_levels))
      for i in range(1, self.number_of_boson_levels):
        self.b_matrix[i - 1, i] = np.sqrt(i)

      self.b_dagger_matrix = self.b_matrix.transpose().conjugate()


    def build_boson_energy_operator(self):
      """ build the boson energy operator in the N-qd N'-level coupled Hilbert space

      Arguments
      ----------
      None

      Attributes
      ----------

      boson_energy_au : float
          fundamental energy of the boson subsystem in atomic units

      b_matrix : numpy matrix
          matrix representation of the lowering operator

      b_dagger_matrix : numpy matrix
          matrix representation of the raising operator

      boson_number_operator : numpy matrix
          matrix representation of the bosonic number operator in the N'-level bosonic Hilbert space

      boson_energy_operator : numpy matrix
          matrix representation of the bosonic energy operator in the N-excitonic N'-level bosonic Hilbert space

      Returns
      -------
      None
      """
      # build number operator in the N'-level bosonic Hilbert space
      self.boson_number_operator = np.dot(self.b_dagger_matrix, self.b_matrix)

      # create the energy operator on the boson Hilbert space: \hbar \omega (\hat{N} + 1/2 I_S)
      _energy_operator_on_boson_space = self.boson_energy_au * self.boson_number_operator + 0.5 * self.boson_energy_au * np.eye(self.number_of_boson_levels)
      print("Printing energy operator on boson space")
      print(_energy_operator_on_boson_space) 

      # build the boson energy operator in the coupled Hilbert space
      self.boson_energy_operator = np.kron(_energy_operator_on_boson_space, self.n_exciton_basis)

    
    def compute_boson_energy_element(self, bra, ket):
      """ compute the energy elements of the bosonic basis states

      Arguments
      ----------
      bra : numpy matrix
          bra state in the coupled Hilbert space

      ket : numpy matrix
          ket state in the coupled Hilbert space

      Attributes
      ----------

      boson_energy_operator : numpy matrix
          matrix representation of the bosonic energy operator in the N-exciton N'-level boson hilbert space

      Returns
      -------
      None
      """


      E_boson_element = np.dot(bra,  np.dot(self.boson_energy_operator, ket)) 

      return E_boson_element


    def compute_spectrum(self):
        """method that will take values computed from spectrum_array and plot them vs wavelength
    
        """
        spectrum_plot = np.zeros(2) # plt.plot(self.wvlngth_variable, test_spec, 'b-')

        return spectrum_plot 
