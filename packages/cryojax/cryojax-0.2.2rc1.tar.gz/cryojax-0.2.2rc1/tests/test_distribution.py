import equinox as eqx
import jax.random as jr
import numpy as np

import cryojax.simulator as cs
from cryojax.image import operators as op
from cryojax.inference import distributions as dist


def test_custom_variance(noisy_model, config, test_image):
    noisy_model = eqx.tree_at(
        lambda m: (m.solvent, m.instrument.detector),
        noisy_model,
        (cs.NullIce(), cs.GaussianDetector(cs.NullDQE())),
    )
    likelihood_model = dist.IndependentFourierGaussian(noisy_model)
    likelihood_model_with_custom_variance = dist.IndependentFourierGaussian(
        noisy_model, variance=op.Constant(1.0)
    )
    freqs = config.wrapped_frequency_grid_in_angstroms.get()
    assert eqx.tree_equal(
        likelihood_model.variance,
        likelihood_model_with_custom_variance.variance,
    )
    np.testing.assert_allclose(
        likelihood_model.variance(freqs),
        likelihood_model_with_custom_variance.variance(freqs),
    )
    np.testing.assert_allclose(
        likelihood_model.log_likelihood(test_image),
        likelihood_model_with_custom_variance.log_likelihood(test_image),
    )
    np.testing.assert_allclose(
        likelihood_model.sample(jr.PRNGKey(seed=0)),
        likelihood_model_with_custom_variance.sample(jr.PRNGKey(seed=0)),
    )
