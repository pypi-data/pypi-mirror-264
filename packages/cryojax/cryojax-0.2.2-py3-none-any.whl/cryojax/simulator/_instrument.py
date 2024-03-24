"""
Abstraction of the electron microscope. This includes models
for the optics, electron dose, and detector.
"""

from typing import Optional, overload

import jax.numpy as jnp
from equinox import Module
from jaxtyping import PRNGKeyArray

from ..image import ifftn, rfftn
from ..typing import ComplexImage, Image, RealImage, RealNumber
from ._config import ImageConfig
from ._detector import AbstractDetector, NullDetector
from ._dose import ElectronDose
from ._optics import AbstractOptics, NullOptics


class Instrument(Module, strict=True):
    """An abstraction of an electron microscope.

    **Attributes:**

    - `optics`: The model for the instrument optics.
    - `dose`: The model for the exposure to electrons
              during image formation.
    - `detector` : The model of the detector.
    """

    optics: AbstractOptics
    dose: ElectronDose
    detector: AbstractDetector

    @overload
    def __init__(self): ...

    @overload
    def __init__(self, optics: AbstractOptics): ...

    @overload
    def __init__(self, optics: AbstractOptics, dose: ElectronDose): ...

    @overload
    def __init__(
        self, optics: AbstractOptics, dose: ElectronDose, detector: AbstractDetector
    ): ...

    def __init__(
        self,
        optics: Optional[AbstractOptics] = None,
        dose: Optional[ElectronDose] = None,
        detector: Optional[AbstractDetector] = None,
    ):
        if (optics is None or dose is None) and isinstance(detector, AbstractDetector):
            raise AttributeError(
                "Cannot set Instrument.detector without passing an AbstractOptics and "
                "an ElectronDose."
            )
        self.optics = optics or NullOptics()
        self.dose = dose or ElectronDose(electrons_per_angstrom_squared=100.0)
        self.detector = detector or NullDetector()

    def propagate_to_detector_plane(
        self,
        fourier_potential_at_exit_plane: ComplexImage,
        config: ImageConfig,
        defocus_offset: RealNumber | float = 0.0,
    ) -> Image:
        """Propagate the scattering potential with the optics model."""
        fourier_contrast_or_wavefunction_at_detector_plane = self.optics(
            fourier_potential_at_exit_plane, config, defocus_offset=defocus_offset
        )

        return fourier_contrast_or_wavefunction_at_detector_plane

    def compute_fourier_squared_wavefunction(
        self,
        fourier_contrast_or_wavefunction_at_detector_plane: ComplexImage,
        config: ImageConfig,
    ) -> ComplexImage:
        """Compute the squared wavefunction at the detector plane, given either the
        contrast or the wavefunction.
        """
        N1, N2 = config.padded_shape
        if isinstance(self.optics, NullOptics):
            # If there is no optics model, assume that the potential is being passed
            # and return unchanged
            fourier_potential_in_exit_plane = (
                fourier_contrast_or_wavefunction_at_detector_plane
            )
            return fourier_potential_in_exit_plane
        elif self.optics.is_linear:
            # ... compute the squared wavefunction directly from the image contrast
            # as |psi|^2 = 1 + 2C.
            fourier_contrast_at_detector_plane = (
                fourier_contrast_or_wavefunction_at_detector_plane
            )
            fourier_squared_wavefunction_at_detector_plane = (
                (2 * fourier_contrast_at_detector_plane).at[0, 0].add(1.0 * N1 * N2)
            )
            return fourier_squared_wavefunction_at_detector_plane
        else:
            # ... otherwise, take the modulus squared
            fourier_wavefunction_at_detector_plane = (
                fourier_contrast_or_wavefunction_at_detector_plane
            )
            fourier_squared_wavefunction_at_detector_plane = rfftn(
                jnp.abs(ifftn(fourier_wavefunction_at_detector_plane)) ** 2
            )
            raise NotImplementedError(
                "Functionality for AbstractOptics.is_linear = False not supported."
            )

    def compute_expected_electron_events(
        self,
        fourier_squared_wavefunction_at_detector_plane: ComplexImage,
        config: ImageConfig,
    ) -> ComplexImage:
        """Compute the expected electron events from the detector."""
        fourier_expected_electron_events = self.detector(
            fourier_squared_wavefunction_at_detector_plane, self.dose, config, key=None
        )

        return fourier_expected_electron_events

    def measure_detector_readout(
        self,
        key: PRNGKeyArray,
        fourier_squared_wavefunction_at_detector_plane: RealImage,
        config: ImageConfig,
    ) -> ComplexImage:
        """Measure the readout from the detector."""
        fourier_detector_readout = self.detector(
            fourier_squared_wavefunction_at_detector_plane, self.dose, config, key
        )

        return fourier_detector_readout
