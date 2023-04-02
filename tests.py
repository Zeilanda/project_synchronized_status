
from main import get_status_parameters

synchronised_time = '''Reference ID    : 0A0A1B32 (10.10.27.50)
Stratum         : 3
Ref time (UTC)  : Sun Mar 12 20:22:02 2023
System time     : 0.000072261 seconds fast of NTP time
Last offset     : +0.000203388 seconds
RMS offset      : 0.000159382 seconds
Frequency       : 20.877 ppm slow
Residual freq   : +0.027 ppm
Skew            : 0.583 ppm
Root delay      : 0.001047121 seconds
Root dispersion : 0.020145597 seconds
Update interval : 521.0 seconds
Leap status     : Normal
'''

non_synchronised_time = '''Reference ID    : 0000000 ()
Stratum         : 3
Ref time (UTC)  : Thu Jan 01 00:00:00 1970
System time     : 0.000000000 seconds slow of NTP time
Last offset     : +0.000062649 seconds
RMS offset      : 0.000152495 seconds
Frequency       : 20.837 ppm slow
Residual freq   : +0.003 ppm
Skew            : 0.311 ppm
Root delay      : 0.001047121 seconds
Root dispersion : 0.019596824 seconds
Update interval : 65.2 seconds
Leap status     : Not synchronised
'''


def test_get_correct_status_parameters():
    assert get_status_parameters(synchronised_time) == ('10.10.27.50', 1678641722.0, 1678642243.0)


def test_get_incorrect_status_parameters():
    assert get_status_parameters(non_synchronised_time) == (None, None, None)
