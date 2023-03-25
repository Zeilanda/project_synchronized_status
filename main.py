"""
code for parsing command output 'chronyc tracking'
"""

import datetime
from typing import Union

status_synchronized_time = '''Reference ID    : 0A0A1B32 (10.10.27.50)
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

status_synchronized_time_with_errors = '''Reference ID    : 0000000 ()
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


def get_parced_status_synchronized_time(status__server_synchronized_time: str) -> dict:

    status_server_data_to_values = {}

    for line in status__server_synchronized_time.split('\n'):
        if line:
            key, value = line.split(': ')
            stripped_key = key.strip()
            stripped_value = value.strip()
            status_server_data_to_values[stripped_key] = stripped_value

    return status_server_data_to_values


def get_reference_id(ref_id: str) -> Union[str, None]:
    id_second_part = ref_id.split()[1][1:-1]
    return id_second_part if id_second_part else None


def get_reference_time(ref_time_utc: str) -> datetime:
    ref_time_datetime = datetime.datetime.strptime(ref_time_utc, '%a %b %d %H:%M:%S %Y')
    try:
        ref_time_timestamp = ref_time_datetime.timestamp()
    except OSError:
        result = None
        return result
    return ref_time_timestamp


def get_next_synchronize_time(reference_time_utc: str, time_interval: str) -> datetime:
    reference_time = get_reference_time(reference_time_utc)
    if not reference_time:
        return None

    ref_time_datetime = datetime.datetime.strptime(reference_time_utc, '%a %b %d %H:%M:%S %Y')
    update_interval = float(time_interval.split()[0])
    synchronize_timestamp = float(ref_time_datetime.timestamp()) + update_interval
    return synchronize_timestamp


status_synchronized_time_dict = get_parced_status_synchronized_time(status_synchronized_time)

ref_time = get_reference_time(status_synchronized_time_dict['Ref time (UTC)'])
reference_id = get_reference_id(status_synchronized_time_dict['Reference ID'])
next_synchronize_time = get_next_synchronize_time(status_synchronized_time_dict['Ref time (UTC)'],
                                                  status_synchronized_time_dict['Update interval'])


def main():
    print(reference_id)
    print(ref_time)
    print(next_synchronize_time)


if __name__ == "__main__":
    main()
