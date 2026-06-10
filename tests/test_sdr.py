import pytest

from rf_sentinel.sdr.hackrf import HackRFSource
from rf_sentinel.sdr.rtl_sdr import RTLSDRSource


def test_hackrf_device():
    device = HackRFSource()
    assert device.name == "HackRF One (device 0)"
    assert device.frequency_range == (0.0, 6.0e9)


def test_hackrf_open_close():
    device = HackRFSource()
    device.open()
    assert device.is_open
    device.close()
    assert not device.is_open


def test_hackrf_invalid_frequency():
    device = HackRFSource()
    with pytest.raises(ValueError):
        device.set_frequency(7e9)


def test_rtlsdr_device():
    device = RTLSDRSource()
    assert device.name == "RTL-SDR (device 0)"
    assert device.frequency_range == (24.0e6, 1.7e9)


def test_rtlsdr_open_close():
    device = RTLSDRSource()
    device.open()
    assert device.is_open
    device.close()
    assert not device.is_open


def test_rtlsdr_invalid_frequency():
    device = RTLSDRSource()
    with pytest.raises(ValueError):
        device.set_frequency(1e6)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
