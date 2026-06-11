import pytest
import numpy as np

@pytest.fixture
def sample_complex():
    return np.random.randn(1024) + 1j * np.random.randn(1024)

@pytest.fixture
def sample_spectrum():
    return np.random.rand(1000) * 40 - 100