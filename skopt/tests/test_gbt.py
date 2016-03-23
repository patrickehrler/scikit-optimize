import numpy as np
from scipy import stats

from sklearn.utils import check_random_state
from sklearn.utils.testing import assert_equal, assert_almost_equal

from skopt.gbt import GBTQuantiles


def truth(X):
    return 0.5 * np.sin(1.75*X[:, 0])

def constant_noise(X):
    return np.ones_like(X)

def sample_noise(X, std=0.2, noise=constant_noise,
                 random_state=None):
    """Uncertainty inherent to the process

    The regressor should try and model this.
    """
    rng = check_random_state(random_state)
    return np.array([rng.normal(0, std*noise(x)) for x in X])

def test_gbt_gaussian():
    # estiamte quantiles of the normal distribution
    rng = np.random.RandomState(1)
    N = 10000
    X = np.ones((N, 1))
    y = rng.normal(size=N)

    rgr = GBTQuantiles()
    rgr.fit(X, y)

    estimates = rgr.predict(X)
    assert_almost_equal(stats.norm.ppf(rgr.quantiles),
                        np.mean(estimates, axis=1),
                        decimal=2)

def test_gbt_with_std():
    # simple test of the interface
    rng = np.random.RandomState(1)
    X = rng.uniform(0, 5, 500)[:, np.newaxis]

    noise_level = 0.5
    y = truth(X) + sample_noise(X, noise_level, random_state=rng)

    X_ = np.linspace(0, 5, 1000)[:, np.newaxis]

    model = GBTQuantiles()
    model.fit(X, y)

    l, c, h = model.predict(X_)
    assert_equal(l.shape, c.shape, h.shape)
    assert_equal(l.shape[0], X_.shape[0])
