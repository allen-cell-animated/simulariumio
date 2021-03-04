#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from simulariumio import FileConverter
from simulariumio.filters import TransformSpatialAxesFilter


@pytest.mark.parametrize(
    "input_path, _filter, expected_data",
    [
        (
            "simulariumio/tests/data/cytosim/aster_pull3D_couples_actin_solid_3_frames"
            "/aster_pull3D_couples_actin_solid_3_frames_small.json",
            TransformSpatialAxesFilter(axes_mapping=["+X", "-Z", "+Y"]),
            {
                "trajectoryInfo": {
                    "version": 2,
                    "timeUnits": {
                        "magnitude": 1.0,
                        "name": "s",
                    },
                    "timeStepSize": 0.05,
                    "totalSteps": 3,
                    "spatialUnits": {
                        "magnitude": 1.0,
                        "name": "µm",
                    },
                    "size": {"x": 200.0, "y": 200.0, "z": 200.0},
                    "typeMapping": {
                        "1": {"name": "microtubule"},
                        "7": {"name": "motor complex"},
                    },
                },
                "spatialData": {
                    "version": 1,
                    "msgType": 1,
                    "bundleStart": 0,
                    "bundleSize": 3,
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
                                -16.78,
                                36.8,
                                30.55,
                                -19.84,
                                43.87,
                                24.169999999999998,
                                -22.900000000000002,
                                50.93,
                                17.78,
                                -25.95,
                                57.99999999999999,
                                11.4,
                                -29.01,
                                65.07,
                                1000.0,
                                12.0,
                                7.0,
                                -73.8,
                                43.89,
                                -25.2,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                            ],
                        },
                        {
                            "frameNumber": 1,
                            "time": 0.05,
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
                                18.0,
                                44.55,
                                -8.86,
                                33.97,
                                36.63,
                                -4.51,
                                38.269999999999996,
                                28.96,
                                -0.5,
                                43.28,
                                21.83,
                                2.52,
                                49.61,
                                16.0,
                                3.58,
                                57.66,
                                12.85,
                                1.47,
                                66.92,
                                1000.0,
                                12.0,
                                7.0,
                                -72.52,
                                43.59,
                                -21.9,
                                0.0,
                                0.0,
                                0.0,
                                2.0,
                                0.0,
                            ],
                        },
                        {
                            "frameNumber": 2,
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
                                -8.86,
                                33.97,
                                36.63,
                                -4.51,
                                38.269999999999996,
                                28.96,
                                -0.5,
                                43.28,
                                21.83,
                                2.52,
                                49.61,
                                16.0,
                                3.58,
                                57.66,
                                1000.0,
                                12.0,
                                7.0,
                                -72.52,
                                43.59,
                                -21.9,
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
def test_transform_spatial_axes_filter(input_path, _filter, expected_data):
    converter = FileConverter(input_path)
    filtered_data = converter.filter_data([_filter])
    buffer_data = converter._read_custom_data(filtered_data)
    assert expected_data == buffer_data
