"""
code for parsing command output 'chronic tracking'
"""

import datetime
from typing import Optional

_REF_TIME_UTC = 'Ref time (UTC)'
_REFERENCE_ID = 'Reference ID'
_UPDATE_INTERVAL = 'Update interval'


def _parse_time_synchronization_status(status__server_synchronized_time: str) -> dict[str, str]:
    status_server_data_to_values = {}

    for line in status__server_synchronized_time.split('\n'):
        if line:
            key, value = line.split(': ')
            stripped_key = key.strip()
            stripped_value = value.strip()
            status_server_data_to_values[stripped_key] = stripped_value

    return status_server_data_to_values


def _get_reference_id(ref_id: str) -> Optional[str]:
    id_second_part = ref_id.split()[1][1:-1]
    return id_second_part if id_second_part else None


def _get_reference_time(ref_time_utc: str) -> datetime:
    ref_time_datetime = datetime.datetime.strptime(ref_time_utc, '%a %b %d %H:%M:%S %Y')
    try:
        result = ref_time_datetime.timestamp()
    except OSError:
        result = None
    return result


def _get_next_synchronize_time(reference_time_utc: str, time_interval: str) -> Optional[float]:
    reference_time = _get_reference_time(reference_time_utc)
    if not reference_time:
        return None

    ref_time_datetime = datetime.datetime.strptime(reference_time_utc, '%a %b %d %H:%M:%S %Y')
    update_interval_float = float(time_interval.split()[0])
    synchronize_timestamp = float(ref_time_datetime.timestamp()) + update_interval_float
    return synchronize_timestamp


def get_status_parameters(chronic_tracking_output: str) -> tuple[str, float, float]:
    status_synchronized_time_dict = _parse_time_synchronization_status(chronic_tracking_output)
    reference_time = _get_reference_time(status_synchronized_time_dict[_REF_TIME_UTC])
    reference_id = _get_reference_id(status_synchronized_time_dict[_REFERENCE_ID])
    next_synchronize_time = _get_next_synchronize_time(status_synchronized_time_dict[_REF_TIME_UTC],
                                                       status_synchronized_time_dict[_UPDATE_INTERVAL])
    return reference_id, reference_time, next_synchronize_time


def main():
    pass


if __name__ == "__main__":
    main()
