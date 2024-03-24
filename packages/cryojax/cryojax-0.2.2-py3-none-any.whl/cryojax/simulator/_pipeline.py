"""
Image formation models.
"""

from abc import abstractmethod
from typing import Optional
from typing_extensions import override

import equinox as eqx
import jax
import jax.numpy as jnp
from equinox import AbstractVar, Module
from jaxtyping import PRNGKeyArray

from ..image import irfftn, normalize_image, rfftn
from ..image.operators import AbstractFilter, AbstractMask
from ..typing import ComplexImage, Image
from ._assembly import AbstractAssembly
from ._config import ImageConfig
from ._detector import NullDetector
from ._ice import AbstractIce, NullIce
from ._instrument import Instrument
from ._pose import AbstractPose
from ._specimen import AbstractConformation, AbstractSpecimen


class AbstractPipeline(Module, strict=True):
    """Base class for an image formation model.

    Call an `AbstractPipeline`'s `render` and `sample`,
    routines.
    """

    config: AbstractVar[ImageConfig]
    filter: AbstractVar[Optional[AbstractFilter]]
    mask: AbstractVar[Optional[AbstractMask]]

    @abstractmethod
    def render(
        self,
        *,
        view_cropped: bool = True,
        get_real: bool = True,
        normalize: bool = False,
    ) -> Image:
        """Render an image without any stochasticity.

        **Arguments:**

        - `view_cropped`: If `True`, view the cropped image.
                          If `view_cropped = False`, `ImagePipeline.filter`,
                          `ImagePipeline.mask`, and normalization with
                          `normalize = True` are not applied.
        - `get_real`: If `True`, return the image in real space.
        - `normalize`: If `True`, normalize the image to mean zero
                       and standard deviation 1.
        """
        raise NotImplementedError

    @abstractmethod
    def sample(
        self,
        key: PRNGKeyArray,
        *,
        view_cropped: bool = True,
        get_real: bool = True,
        normalize: bool = False,
    ) -> Image:
        """
        Sample an image from a realization of the `AbstractIce` and
        `AbstractDetector` models.

        **Arguments:**

        - `key`: The random number generator key.

        See `ImagePipeline.render` for documentation of keyword arguments.
        """
        raise NotImplementedError

    def __call__(
        self,
        key: Optional[PRNGKeyArray] = None,
        *,
        view_cropped: bool = True,
        get_real: bool = True,
        normalize: bool = False,
    ) -> Image:
        """Sample an image with the noise models or render an image
        without them.
        """
        if key is None:
            return self.render(
                view_cropped=view_cropped,
                get_real=get_real,
                normalize=normalize,
            )
        else:
            return self.sample(
                key,
                view_cropped=view_cropped,
                get_real=get_real,
                normalize=normalize,
            )

    def crop_and_apply_operators(
        self,
        image: ComplexImage,
        *,
        get_real: bool = True,
        normalize: bool = False,
    ) -> Image:
        """Return an image postprocessed with filters, cropping, and masking
        in either real or fourier space.
        """
        config = self.config
        if self.mask is None and config.padded_shape == config.shape:
            # ... if there are no masks and we don't need to crop,
            # minimize moving back and forth between real and fourier space
            if self.filter is not None:
                image = self.filter(image)
            if normalize:
                image = normalize_image(
                    image, is_real=False, shape_in_real_space=config.shape
                )
            return irfftn(image, s=config.shape) if get_real else image
        else:
            # ... otherwise, apply filter, crop, and mask, again trying to
            # minimize moving back and forth between real and fourier space
            is_filter_applied = True if self.filter is None else False
            if (
                self.filter is not None
                and self.filter.buffer.shape
                == config.wrapped_padded_frequency_grid.get().shape[0:2]
            ):
                # ... apply the filter here if it is the same size as the padded
                # coordinates
                is_filter_applied = True
                image = self.filter(image)
            image = irfftn(image, s=config.padded_shape)
            if self.mask is not None:
                image = self.mask(image)
            image = config.crop_to_shape(image)
            if is_filter_applied or self.filter is None:
                # ... normalize and return if the filter has already been applied
                if normalize:
                    image = normalize_image(image, is_real=True)
                return image if get_real else rfftn(image)
            else:
                # ... otherwise, apply the filter here, normalize, and return. assume
                # the filter is the same size as the non-padded coordinates
                image = self.filter(rfftn(image))
                if normalize:
                    image = normalize_image(
                        image, is_real=False, shape_in_real_space=config.shape
                    )
                return irfftn(image, s=config.shape) if get_real else image

    def _get_final_image(
        self,
        image: ComplexImage,
        *,
        view_cropped: bool = True,
        get_real: bool = True,
        normalize: bool = False,
    ) -> Image:
        config = self.config
        if view_cropped:
            return self.crop_and_apply_operators(
                image,
                get_real=get_real,
                normalize=normalize,
            )
        else:
            return irfftn(image, s=config.padded_shape) if get_real else image


class ImagePipeline(AbstractPipeline, strict=True):
    """Standard image formation pipeline.

    **Attributes:**

    - `config`: The image configuration.
    - `specimen`: The abstraction of the biological specimen.
    - `instrument`: The abstraction of the electron microscope.
    - `solvent: `The solvent around the specimen.
    - `filter: `A filter to apply to the image.
    - `mask`: A mask to apply to the image.
    """

    config: ImageConfig
    specimen: AbstractSpecimen
    instrument: Instrument
    solvent: AbstractIce

    filter: Optional[AbstractFilter]
    mask: Optional[AbstractMask]

    def __init__(
        self,
        config: ImageConfig,
        specimen: AbstractSpecimen,
        instrument: Optional[Instrument] = None,
        solvent: Optional[AbstractIce] = None,
        *,
        filter: Optional[AbstractFilter] = None,
        mask: Optional[AbstractMask] = None,
    ):
        self.config = config
        self.specimen = specimen
        self.instrument = instrument or Instrument()
        self.solvent = solvent or NullIce()
        self.filter = filter
        self.mask = mask

    def render(
        self,
        *,
        view_cropped: bool = True,
        get_real: bool = True,
        normalize: bool = False,
    ) -> Image:
        """Render an image without any stochasticity."""
        # Compute the scattering potential in the exit plane
        fourier_potential_at_exit_plane = self.specimen.scatter_to_exit_plane(
            self.config
        )
        # ... propagate the potential to the detector plane
        fourier_contrast_or_wavefunction_at_detector_plane = (
            self.instrument.propagate_to_detector_plane(
                fourier_potential_at_exit_plane,
                self.config,
                defocus_offset=self.specimen.pose.offset_z_in_angstroms,
            )
        )
        # ... compute the squared wavefunction
        fourier_squared_wavefunction_at_detector_plane = (
            self.instrument.compute_fourier_squared_wavefunction(
                fourier_contrast_or_wavefunction_at_detector_plane,
                self.config,
            )
        )
        # ... now measure the expected electron events at the detector
        fourier_expected_electron_events = (
            self.instrument.compute_expected_electron_events(
                fourier_squared_wavefunction_at_detector_plane, self.config
            )
        )

        return self._get_final_image(
            fourier_expected_electron_events,
            view_cropped=view_cropped,
            get_real=get_real,
            normalize=normalize,
        )

    def sample(
        self,
        key: PRNGKeyArray,
        *,
        view_cropped: bool = True,
        get_real: bool = True,
        normalize: bool = False,
    ) -> Image:
        """Sample the assembly from the stochastic parts of the model."""
        idx = 0  # Keep track of number of stochastic models
        if not isinstance(self.solvent, NullIce) and not isinstance(
            self.instrument.detector, NullDetector
        ):
            keys = jax.random.split(key)
        else:
            keys = jnp.expand_dims(key, axis=0)
        if not isinstance(self.solvent, NullIce):
            # Compute the scattering potential in the exit plane, including
            # potential of the solvent
            fourier_potential_at_exit_plane = (
                self.specimen.scatter_to_exit_plane_with_solvent(
                    keys[idx], self.solvent, self.config
                )
            )
            idx += 1
        else:
            # ... otherwise, scatter just compute the potential of the specimen
            fourier_potential_at_exit_plane = self.specimen.scatter_to_exit_plane(
                self.config
            )

        # ... propagate the potential to the contrast at the detector plane
        fourier_contrast_or_wavefunction_at_detector_plane = (
            self.instrument.propagate_to_detector_plane(
                fourier_potential_at_exit_plane,
                self.config,
                defocus_offset=self.specimen.pose.offset_z_in_angstroms,
            )
        )
        # ... compute the squared wavefunction
        fourier_squared_wavefunction_at_detector_plane = (
            self.instrument.compute_fourier_squared_wavefunction(
                fourier_contrast_or_wavefunction_at_detector_plane,
                self.config,
            )
        )
        # ... now measure the detector readout
        fourier_detector_readout = self.instrument.measure_detector_readout(
            keys[idx],
            fourier_squared_wavefunction_at_detector_plane,
            self.config,
        )

        return self._get_final_image(
            fourier_detector_readout,
            view_cropped=view_cropped,
            get_real=get_real,
            normalize=normalize,
        )


class AssemblyPipeline(AbstractPipeline, strict=True):
    """Compute an image from a superposition of subunits in
    the `AbstractAssembly`.

    **Attributes:**

    - `config`: The image configuration.

    - `assembly`: The assembly from which to render images.

    - `instrument`: The abstraction of the electron microscope.

    - `solvent: `The solvent around the specimen.

    - `filter: `A filter to apply to the image.

    - `mask`: A mask to apply to the image.
    """

    config: ImageConfig
    assembly: AbstractAssembly
    instrument: Instrument
    solvent: AbstractIce

    filter: Optional[AbstractFilter]
    mask: Optional[AbstractMask]

    def __init__(
        self,
        config: ImageConfig,
        assembly: AbstractAssembly,
        instrument: Optional[Instrument] = None,
        solvent: Optional[AbstractIce] = None,
        *,
        filter: Optional[AbstractFilter] = None,
        mask: Optional[AbstractMask] = None,
    ):
        self.config = config
        self.assembly = assembly
        self.instrument = instrument or Instrument()
        self.solvent = solvent or NullIce()
        self.filter = filter
        self.mask = mask

    @override
    def sample(
        self,
        key: PRNGKeyArray,
        *,
        view_cropped: bool = True,
        get_real: bool = True,
        normalize: bool = False,
    ) -> Image:
        """Sample the superposition of `AbstractAssembly.subunits` from
        stochastic models.
        """
        idx = 0  # Keep track of number of stochastic models
        if not isinstance(self.solvent, NullIce) and not isinstance(
            self.instrument.detector, NullDetector
        ):
            keys = jax.random.split(key)
        else:
            keys = jnp.expand_dims(key, axis=0)
        # Compute the contrast or wavefunction in the detector plane
        fourier_contrast_or_wavefunction_at_detector_plane = (
            self._compute_subunit_superposition()
        )
        if not isinstance(self.solvent, NullIce):
            # Compute the solvent contrast or wavefunction in the detector plane
            # and add to that of the specimen
            fourier_solvent_potential_at_exit_plane = self.solvent.sample(
                keys[idx], self.config
            )
            fourier_contrast_or_wavefunction_at_detector_plane += (
                self.instrument.propagate_to_detector_plane(
                    fourier_solvent_potential_at_exit_plane, self.config
                )
            )
            idx += 1
        # ... compute the squared wavefunction
        fourier_squared_wavefunction_at_detector_plane = (
            self.instrument.compute_fourier_squared_wavefunction(
                fourier_contrast_or_wavefunction_at_detector_plane,
                self.config,
            )
        )
        # ... measure the detector readout
        fourier_detector_readout = self.instrument.measure_detector_readout(
            keys[idx],
            fourier_squared_wavefunction_at_detector_plane,
            self.config,
        )

        return self._get_final_image(
            fourier_detector_readout,
            view_cropped=view_cropped,
            get_real=get_real,
            normalize=normalize,
        )

    @override
    def render(
        self,
        *,
        view_cropped: bool = True,
        get_real: bool = True,
        normalize: bool = False,
    ) -> Image:
        """Render the superposition of images from the
        `AbstractAssembly.subunits`.
        """
        # Compute the contrast in the detector plane
        fourier_contrast_or_wavefunction_at_detector_plane = (
            self._compute_subunit_superposition()
        )
        # ... compute the squared wavefunction
        fourier_squared_wavefunction_at_detector_plane = (
            self.instrument.compute_fourier_squared_wavefunction(
                fourier_contrast_or_wavefunction_at_detector_plane,
                self.config,
            )
        )
        # ... compute the expected number of electron events
        fourier_expected_electron_events = (
            self.instrument.compute_expected_electron_events(
                fourier_squared_wavefunction_at_detector_plane,
                self.config,
            )
        )

        return self._get_final_image(
            fourier_expected_electron_events,
            view_cropped=view_cropped,
            get_real=get_real,
            normalize=normalize,
        )

    def _compute_subunit_superposition(self):
        # Get the assembly subunits
        subunits = self.assembly.subunits
        # Setup vmap over the pose and conformation
        is_vmap = lambda x: isinstance(x, (AbstractPose, AbstractConformation))
        to_vmap = jax.tree_util.tree_map(is_vmap, subunits, is_leaf=is_vmap)
        vmap, novmap = eqx.partition(subunits, to_vmap)
        # Compute all images and sum
        compute_contrast_or_wavefunction = (
            lambda spec, conf, ins: ins.propagate_to_detector_plane(
                spec.scatter_to_exit_plane(conf),
                conf,
                defocus_offset=spec.pose.offset_z_in_angstroms,
            )
        )
        # ... vmap to compute a stack of images to superimpose
        compute_stack = jax.vmap(
            lambda vmap, novmap, conf, ins: compute_contrast_or_wavefunction(
                eqx.combine(vmap, novmap), conf, ins
            ),
            in_axes=(0, None, None, None),
        )
        # ... sum over the stack of images and jit
        compute_stack_and_sum = jax.jit(
            lambda vmap, novmap, conf, ins: jnp.sum(
                compute_stack(vmap, novmap, conf, ins),
                axis=0,
            )
        )
        # ... compute the superposition
        fourier_contrast_or_wavefunction_at_detector_plane = (
            (compute_stack_and_sum(vmap, novmap, self.config, self.instrument))
            .at[0, 0]
            .divide(self.assembly.n_subunits)
        )

        return fourier_contrast_or_wavefunction_at_detector_plane
