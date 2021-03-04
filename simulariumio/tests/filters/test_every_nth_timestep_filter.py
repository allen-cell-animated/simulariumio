#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from simulariumio import FileConverter
from simulariumio.filters import EveryNthTimestepFilter


@pytest.mark.parametrize(
    "input_path, _filter, expected_data",
    [
        (
            "simulariumio/tests/data/cytosim/aster_pull3D_couples_actin_solid_3_frames"
            "/aster_pull3D_couples_actin_solid_3_frames.json",
            EveryNthTimestepFilter(n=2),
            {
                "trajectoryInfo": {
                    "version": 2,
                    "timeUnits": {
                        "magnitude": 1.0,
                        "name": "s",
                    },
                    "timeStepSize": 0.1,
                    "totalSteps": 2,
                    "spatialUnits": {
                        "magnitude": 1.0,
                        "name": "µm",
                    },
                    "size": {"x": 200.0, "y": 200.0, "z": 200.0},
                    "typeMapping": {
                        "1": {"name": "microtubule"},
                        "2": {"name": "actin"},
                        "3": {"name": "aster"},
                        "4": {"name": "vesicle"},
                        "5": {"name": "kinesin"},
                        "6": {"name": "dynein"},
                        "7": {"name": "motor complex"},
                    },
                },
                "spatialData": {
                    "version": 1,
                    "msgType": 1,
                    "bundleStart": 0,
                    "bundleSize": 2,
                    "bundleData": [
                        {
                            "frameNumber": 0,
                            "time": 0.0,
                            "data": [
                                1001.0,
                                1.0,
                                1.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                15.0,
                                36.93,
                                36.8,
                                16.78,
                                30.55,
                                43.87,
                                19.84,
                                24.169999999999998,
                                50.93,
                                22.900000000000002,
                                17.78,
                                57.99999999999999,
                                25.95,
                                11.4,
                                65.07,
                                29.01,
                                1001.0,
                                2.0,
                                1.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                12.0,
                                36.93,
                                36.8,
                                16.78,
                                37.2,
                                27.11,
                                19.220000000000002,
                                37.46,
                                17.41,
                                21.66,
                                37.730000000000004,
                                7.720000000000001,
                                24.099999999999998,
                                1001.0,
                                3.0,
                                1.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                15.0,
                                36.93,
                                36.8,
                                16.78,
                                40.71,
                                30.86,
                                23.880000000000003,
                                44.5,
                                24.92,
                                30.98,
                                48.28,
                                18.970000000000002,
                                38.07,
                                52.07000000000001,
                                13.03,
                                45.17,
                                1001.0,
                                13.0,
                                2.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                12.0,
                                46.08,
                                -104.85,
                                -2.1,
                                45.67,
                                -104.54,
                                -1.9,
                                45.26,
                                -104.23,
                                -1.7000000000000002,
                                44.85,
                                -103.91999999999999,
                                -1.5,
                                1001.0,
                                14.0,
                                2.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                9.0,
                                53.690000000000005,
                                79.28,
                                -3.09,
                                53.6,
                                78.83,
                                -3.39,
                                53.5,
                                78.39,
                                -3.6999999999999997,
                                1000.0,
                                4.0,
                                3.0,
                                36.93,
                                36.8,
                                16.78,
                                0.0,
                                0.0,
                                0.0,
                                10.0,
                                0.0,
                                1000.0,
                                5.0,
                                4.0,
                                78.60000000000001,
                                -28.799999999999997,
                                18.04,
                                0.0,
                                0.0,
                                0.0,
                                10.0,
                                0.0,
                                1000.0,
                                6.0,
                                4.0,
                                -55.089999999999996,
                                -33.42,
                                -61.85000000000001,
                                0.0,
                                0.0,
                                0.0,
                                10.0,
                                0.0,
                                1000.0,
                                7.0,
                                5.0,
                                20.61,
                                -39.910000000000004,
                                89.35,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                8.0,
                                5.0,
                                92.82000000000001,
                                32.269999999999996,
                                18.55,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                9.0,
                                5.0,
                                37.56,
                                -80.46,
                                -46.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                101.0,
                                6.0,
                                -74.11999999999999,
                                30.31,
                                -59.89,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                102.0,
                                6.0,
                                -61.739999999999995,
                                -55.269999999999996,
                                -55.98,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                103.0,
                                6.0,
                                -19.37,
                                -9.379999999999999,
                                97.66,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                10.0,
                                7.0,
                                32.629999999999995,
                                38.550000000000004,
                                57.120000000000005,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                11.0,
                                7.0,
                                4.42,
                                20.200000000000003,
                                -62.88,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                12.0,
                                7.0,
                                -73.8,
                                -25.2,
                                -43.89,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                            ],
                        },
                        {
                            "frameNumber": 1,
                            "time": 0.1,
                            "data": [
                                1001.0,
                                1.0,
                                1.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                15.0,
                                44.55,
                                33.97,
                                8.86,
                                36.63,
                                38.269999999999996,
                                4.51,
                                28.96,
                                43.28,
                                0.5,
                                21.83,
                                49.61,
                                -2.52,
                                16.0,
                                57.66,
                                -3.58,
                                1001.0,
                                2.0,
                                1.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                6.0,
                                44.230000000000004,
                                33.56,
                                9.04,
                                42.02,
                                24.04,
                                6.92,
                                1001.0,
                                3.0,
                                1.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                12.0,
                                44.22,
                                33.18,
                                8.89,
                                40.660000000000004,
                                24.060000000000002,
                                10.94,
                                37.22,
                                15.1,
                                13.750000000000002,
                                34.0,
                                6.74,
                                18.2,
                                1001.0,
                                13.0,
                                2.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                6.0,
                                51.480000000000004,
                                -85.75,
                                5.3100000000000005,
                                51.0,
                                -85.78,
                                5.59,
                                1001.0,
                                14.0,
                                2.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                12.0,
                                47.0,
                                81.69999999999999,
                                -9.139999999999999,
                                47.099999999999994,
                                81.22,
                                -9.39,
                                47.21,
                                80.74,
                                -9.64,
                                47.31,
                                80.25999999999999,
                                -9.89,
                                1000.0,
                                4.0,
                                3.0,
                                44.86,
                                34.239999999999995,
                                9.36,
                                0.0,
                                0.0,
                                0.0,
                                10.0,
                                0.0,
                                1000.0,
                                5.0,
                                4.0,
                                77.18,
                                -36.65,
                                21.9,
                                0.0,
                                0.0,
                                0.0,
                                10.0,
                                0.0,
                                1000.0,
                                6.0,
                                4.0,
                                -59.67,
                                -29.659999999999997,
                                -65.88000000000001,
                                0.0,
                                0.0,
                                0.0,
                                10.0,
                                0.0,
                                1000.0,
                                7.0,
                                5.0,
                                20.61,
                                -39.910000000000004,
                                89.35,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                8.0,
                                5.0,
                                92.82000000000001,
                                32.269999999999996,
                                18.55,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                9.0,
                                5.0,
                                37.56,
                                -80.46,
                                -46.0,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                101.0,
                                6.0,
                                -74.11999999999999,
                                30.31,
                                -59.89,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                102.0,
                                6.0,
                                -61.739999999999995,
                                -55.269999999999996,
                                -55.98,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                103.0,
                                6.0,
                                -19.37,
                                -9.379999999999999,
                                97.66,
                                0.0,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                1000.0,
                                10.0,
                                7.0,
                                33.96,
                                13.309999999999999,
                                50.29,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                11.0,
                                7.0,
                                19.189999999999998,
                                17.69,
                                -76.94,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                                1000.0,
                                12.0,
                                7.0,
                                -72.52,
                                -21.9,
                                -43.59,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                            ],
                        },
                    ],
                },
                "plotData": {"version": 1, "data": []},
            },
        ),
    ],
)
def test_every_nth_timestep_filter(input_path, _filter, expected_data):
    converter = FileConverter(input_path)
    filtered_data = converter.filter_data([_filter])
    buffer_data = converter._read_custom_data(filtered_data)
    assert expected_data == buffer_data
