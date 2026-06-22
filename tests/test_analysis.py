import numpy as np
import pytest

from rf_sentinel.analysis.demodulator import Demodulator
from rf_sentinel.analysis.spectrum import SpectrumAnalyzer
from rf_sentinel.analysis.waterfall import Waterfall
from rf_sentinel.classification.rule_based import SignalClassifier
from rf_sentinel.detection.energy import EnergyDetector
from rf_sentinel.detection.threshold import SignalDetector


def test_spectrum_analyzer():
    analyzer = SpectrumAnalyzer()
    samples = np.random.randn(1024) + 1j * np.random.randn(1024)
    psd, freqs = analyzer.analyze(samples)
    assert len(psd) == 512
    assert len(freqs) == 512


def test_waterfall():
    wf = Waterfall(width=100, height=50)
    spectrum = np.random.rand(100) * 100 - 60
    wf.add_spectrum(spectrum)
    img = wf.get_image()
    assert img.shape == (50, 100)


def test_demodulator_am():
    demod = Demodulator()
    samples = np.random.randn(1000) + 1j * np.random.randn(1000)
    result = demod.demodulate(samples, "am")
    assert len(result) == len(samples)


def test_signal_detector():
    detector = SignalDetector()
    spectrum = np.random.rand(1000) * 40 - 100
    frequencies = np.linspace(100e6, 110e6, 1000)
    peaks = detector.detect(spectrum, frequencies)
    assert isinstance(peaks, list)


def test_energy_detector():
    ed = EnergyDetector()
    samples = np.random.randn(2048) + 1j * np.random.randn(2048)
    detections = ed.detect(samples)
    assert isinstance(detections, list)


def test_signal_classifier():
    clf = SignalClassifier()
    signal = {"bandwidth": 100e3, "power": -45.0}
    result = clf.classify(signal)
    assert "modulation" in result
    assert "confidence" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
