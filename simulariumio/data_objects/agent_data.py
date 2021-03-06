#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import copy
import logging
from typing import List, Tuple, Dict, Any
import math

import numpy as np
import pandas as pd

from ..constants import V1_SPATIAL_BUFFER_STRUCT, VIZ_TYPE
from ..exceptions import DataError

###############################################################################

log = logging.getLogger(__name__)

###############################################################################


class AgentData:
    times: np.ndarray
    n_agents: np.ndarray
    viz_types: np.ndarray
    unique_ids: np.ndarray
    types: List[List[str]]
    positions: np.ndarray
    rotations: np.ndarray
    radii: np.ndarray
    n_subpoints: np.ndarray = None
    subpoints: np.ndarray = None
    draw_fiber_points: bool = False
    type_ids: np.ndarray
    type_mapping: Dict[str, Any]

    def __init__(
        self,
        times: np.ndarray,
        n_agents: np.ndarray,
        viz_types: np.ndarray,
        unique_ids: np.ndarray,
        types: List[List[str]],
        positions: np.ndarray,
        radii: np.ndarray,
        rotations: np.ndarray = None,
        n_subpoints: np.ndarray = None,
        subpoints: np.ndarray = None,
        draw_fiber_points: bool = False,
        type_ids: np.ndarray = None,
    ):
        """
        This object contains spatial simulation data

        Parameters
        ----------
        times : np.ndarray (shape = [timesteps])
            A numpy ndarray containing the elapsed simulated time
            at each timestep (in the units specified by
            TrajectoryData.time_units)
        n_agents : np.ndarray (shape = [timesteps])
            A numpy ndarray containing the number of agents
            that exist at each timestep
        viz_types : np.ndarray (shape = [timesteps, agents])
            A numpy ndarray containing the viz type
            for each agent at each timestep. Current options:
                1000 : default,
                1001 : fiber (which will require subpoints)
        unique_ids : np.ndarray (shape = [timesteps, agents])
            A numpy ndarray containing the unique ID
            for each agent at each timestep
        types : List[List[str]] (list of shape [timesteps, agents])
            A list containing timesteps, for each a list of
            the string name for the type of each agent
        positions : np.ndarray (shape = [timesteps, agents, 3])
            A numpy ndarray containing the XYZ position
            for each agent at each timestep (in the units
            specified by TrajectoryData.spatial_units)
        radii : np.ndarray (shape = [timesteps, agents])
            A numpy ndarray containing the radius
            for each agent at each timestep
        rotations : np.ndarray (shape = [timesteps, agents, 3]) (optional)
            A numpy ndarray containing the XYZ euler angles representing
            the rotation for each agent at each timestep in degrees
            Default: [0, 0, 0] for each agent
        n_subpoints : np.ndarray (shape = [timesteps, agents]) (optional)
            A numpy ndarray containing the number of subpoints
            belonging to each agent at each timestep. Required if
            subpoints are provided
            Default: None
        subpoints : np.ndarray
        (shape = [timesteps, agents, subpoints, 3]) (optional)
            A numpy ndarray containing a list of subpoint position data
            for each agent at each timestep. These values are
            currently only used for fiber agents
            Default: None
        draw_fiber_points: bool (optional)
            Draw spheres at every other fiber point for fibers?
            Default: False
        """
        self.times = times
        self.n_agents = n_agents
        self.viz_types = viz_types
        self.unique_ids = unique_ids
        self.types = types
        self.positions = positions
        self.radii = radii
        self.rotations = (
            rotations if rotations is not None else np.zeros_like(positions)
        )
        self.n_subpoints = (
            n_subpoints if n_subpoints is not None else np.zeros_like(radii)
        )
        self.subpoints = subpoints if subpoints is not None else np.zeros_like(radii)
        self.draw_fiber_points = draw_fiber_points
        self.type_ids = type_ids
        self.type_mapping = None

    @staticmethod
    def _get_buffer_data_dimensions(buffer_data: Dict[str, Any]) -> Tuple[int]:
        """ """
        bundle_data = buffer_data["spatialData"]["bundleData"]
        total_steps = len(bundle_data)
        max_n_agents = 0
        max_n_subpoints = 0
        for t in range(total_steps):
            data = bundle_data[t]["data"]
            i = 0
            n_agents = 0
            while i < len(data):
                # a new agent should start at this index
                n_agents += 1
                i += V1_SPATIAL_BUFFER_STRUCT.NSP_INDEX
                # get the number of subpoints
                n_sp = math.floor(data[i] / 3.0)
                if n_sp > max_n_subpoints:
                    max_n_subpoints = n_sp
                i += int(
                    data[i]
                    + (
                        V1_SPATIAL_BUFFER_STRUCT.VALUES_PER_AGENT
                        - V1_SPATIAL_BUFFER_STRUCT.NSP_INDEX
                        - 1
                    )
                )
            if n_agents > max_n_agents:
                max_n_agents = n_agents
        return total_steps, max_n_agents, max_n_subpoints

    @staticmethod
    def get_type_ids_and_mapping(
        type_names: List[List[str]], type_ids: np.ndarray = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Generate the type_ids array from the type_names list
        """
        total_steps = len(type_names)
        max_agents = 0
        for t in range(len(type_names)):
            n = len(type_names[t])
            if n > max_agents:
                max_agents = n
        use_existing_ids = True
        if type_ids is None:
            type_ids = np.zeros((len(type_names), max_agents))
            use_existing_ids = False
        type_name_mapping = {}
        type_id_mapping = {}
        last_tid = 0
        for t in range(total_steps):
            for n in range(len(type_names[t])):
                tn = type_names[t][n]
                if len(tn) == 0:
                    continue
                if tn not in type_id_mapping:
                    if use_existing_ids:
                        tid = int(type_ids[t][n])
                    else:
                        tid = last_tid
                        last_tid += 1
                    type_id_mapping[tn] = tid
                    type_name_mapping[str(tid)] = {"name": tn}
                if not use_existing_ids:
                    type_ids[t][n] = type_id_mapping[tn]
        return type_ids, type_name_mapping

    @staticmethod
    def get_type_names(
        type_ids: np.ndarray, type_mapping: Dict[str, Any]
    ) -> List[List[str]]:
        """
        Generate the type_names list from the type_ids array
        """
        result = []
        for t in range(type_ids.shape[0]):
            result.append([])
            for n in range(int(len(type_ids[t]))):
                result[t].append(type_mapping[str(int(type_ids[t][n]))]["name"])
        return result

    @classmethod
    def from_buffer_data(cls, buffer_data: Dict[str, Any]):
        """
        Create AgentData from a simularium JSON dict containing buffers
        """
        bundle_data = buffer_data["spatialData"]["bundleData"]
        total_steps, max_agents, max_subpoints = AgentData._get_buffer_data_dimensions(
            buffer_data
        )
        print(
            f"original dim = {total_steps} timesteps X "
            f"{max_agents} agents X {max_subpoints} subpoints"
        )
        times = np.zeros(total_steps)
        n_agents = np.zeros(total_steps)
        viz_types = np.zeros((total_steps, max_agents))
        unique_ids = np.zeros((total_steps, max_agents))
        type_ids = np.zeros((total_steps, max_agents))
        positions = np.zeros((total_steps, max_agents, 3))
        rotations = np.zeros((total_steps, max_agents, 3))
        radii = np.ones((total_steps, max_agents))
        n_subpoints = np.zeros((total_steps, max_agents))
        subpoints = np.zeros((total_steps, max_agents, max_subpoints, 3))
        for t in range(total_steps):
            times[t] = bundle_data[t]["time"]
            frame_data = bundle_data[t]["data"]
            n = 0
            i = 0
            while i + V1_SPATIAL_BUFFER_STRUCT.NSP_INDEX < len(frame_data):
                # a new agent should start at this index
                viz_types[t][n] = frame_data[
                    i + V1_SPATIAL_BUFFER_STRUCT.VIZ_TYPE_INDEX
                ]
                unique_ids[t][n] = frame_data[i + V1_SPATIAL_BUFFER_STRUCT.UID_INDEX]
                type_ids[t][n] = frame_data[i + V1_SPATIAL_BUFFER_STRUCT.TID_INDEX]
                positions[t][n] = [
                    frame_data[i + V1_SPATIAL_BUFFER_STRUCT.POSX_INDEX],
                    frame_data[i + V1_SPATIAL_BUFFER_STRUCT.POSY_INDEX],
                    frame_data[i + V1_SPATIAL_BUFFER_STRUCT.POSZ_INDEX],
                ]
                rotations[t][n] = [
                    frame_data[i + V1_SPATIAL_BUFFER_STRUCT.ROTX_INDEX],
                    frame_data[i + V1_SPATIAL_BUFFER_STRUCT.ROTY_INDEX],
                    frame_data[i + V1_SPATIAL_BUFFER_STRUCT.ROTZ_INDEX],
                ]
                radii[t][n] = frame_data[i + V1_SPATIAL_BUFFER_STRUCT.R_INDEX]
                i += V1_SPATIAL_BUFFER_STRUCT.NSP_INDEX
                # get the subpoints
                if max_subpoints < 1:
                    i += int(
                        V1_SPATIAL_BUFFER_STRUCT.SP_INDEX
                        - V1_SPATIAL_BUFFER_STRUCT.NSP_INDEX
                    )
                    n += 1
                    continue
                n_subpoints[t][n] = int(frame_data[i] / 3.0)
                p = 0
                d = 0
                for j in range(int(frame_data[i])):
                    subpoints[t][n][p][d] = frame_data[i + 1 + j]
                    d += 1
                    if d > 2:
                        d = 0
                        p += 1
                i += int(
                    frame_data[i]
                    + (
                        V1_SPATIAL_BUFFER_STRUCT.SP_INDEX
                        - V1_SPATIAL_BUFFER_STRUCT.NSP_INDEX
                    )
                )
                n += 1
            n_agents[t] = n
        type_names = AgentData.get_type_names(
            type_ids, buffer_data["trajectoryInfo"]["typeMapping"]
        )
        return cls(
            times=times,
            n_agents=n_agents,
            viz_types=viz_types,
            unique_ids=unique_ids,
            types=type_names,
            positions=positions,
            radii=radii,
            rotations=rotations,
            n_subpoints=n_subpoints,
            subpoints=subpoints,
            draw_fiber_points=False,
            type_ids=type_ids,
        )

    @classmethod
    def from_dataframe(cls, traj: pd.DataFrame):
        """
        Create AgentData from a pandas DataFrame with columns:
        time, unique_id, type, positionX, positionY, positionZ, radius
        (only for default agents, no fibers)
        """
        times = np.unique(traj.loc[0, "time"].to_numpy())
        n_agents = np.squeeze(
            traj.groupby("time").agg(["count"])["unique_id"].to_numpy()
        )
        grouped_traj = (
            traj.set_index(["time", traj.groupby("time").cumcount()])
            .unstack(fill_value=0)
            .stack()
        )
        unique_ids = np.array(
            grouped_traj["unique_id"]
            .groupby(level=0)
            .apply(lambda x: x.values.tolist())
            .tolist()
        )
        positions = np.array(
            grouped_traj[["positionX", "positionY", "positionZ"]]
            .groupby(level=0)
            .apply(lambda x: x.values.tolist())
            .tolist()
        )
        rotations = np.array(
            grouped_traj[["rotationX", "rotationY", "rotationZ"]]
            .groupby(level=0)
            .apply(lambda x: x.values.tolist())
            .tolist()
        )
        radii = np.array(
            grouped_traj["radius"]
            .groupby(level=0)
            .apply(lambda x: x.values.tolist())
            .tolist()
        )
        grouped_traj = (
            traj.set_index(["time", traj.groupby("time").cumcount()])
            .unstack(fill_value="")
            .stack()
        )
        type_names = (
            grouped_traj["type"]
            .groupby(level=0)
            .apply(lambda x: x.values.tolist())
            .tolist()
        )
        return cls(
            times=times,
            n_agents=n_agents,
            viz_types=VIZ_TYPE.DEFAULT * np.ones_like(unique_ids),
            unique_ids=unique_ids,
            types=type_names,
            positions=positions,
            radii=radii,
            rotations=rotations,
        )

    def append_agents(self, new_agents: AgentData):
        """
        Concatenate the new AgentData with the current data,
        generate new unique IDs and type IDs as needed
        """
        # get dimensions
        total_steps = self.times.size
        new_total_steps = new_agents.times.size
        if new_total_steps != total_steps:
            raise DataError(
                "Timestep in data to add differs from existing: "
                f"new data has {new_total_steps} steps, while "
                f"existing data has {total_steps}"
            )
        max_agents = int(np.amax(self.n_agents)) + int(np.amax(new_agents.n_agents))
        # add agents
        n_agents = np.add(self.n_agents, new_agents.n_agents)
        self.viz_types = np.concatenate((self.viz_types, new_agents.viz_types), axis=1)
        unique_ids = np.zeros((total_steps, max_agents))
        types = []
        type_ids = np.zeros((total_steps, max_agents))
        self.positions = np.concatenate((self.positions, new_agents.positions), axis=1)
        self.rotations = np.concatenate((self.rotations, new_agents.rotations), axis=1)
        self.radii = np.concatenate((self.radii, new_agents.radii), axis=1)
        self.n_subpoints = np.concatenate(
            (self.n_subpoints, new_agents.n_subpoints), axis=1
        )
        self.subpoints = np.concatenate((self.subpoints, new_agents.subpoints), axis=1)
        # generate new unique IDs and type IDs so they don't overlap
        if self.type_ids is None:
            self.type_ids, tm = AgentData.get_type_ids_and_mapping(self.types)
        if new_agents.type_ids is None:
            new_agents.type_ids, tm = AgentData.get_type_ids_and_mapping(
                new_agents.types
            )
        self.type_mapping = None
        used_uids = list(np.unique(self.unique_ids))
        new_uids = {}
        for t in range(total_steps):
            i = 0
            types.append([])
            n_a = int(self.n_agents[t])
            for n in range(n_a):
                unique_ids[t][i] = self.unique_ids[t][n]
                type_ids[t][i] = self.type_ids[t][n]
                types[t].append(self.types[t][n])
                i += 1
            n_a = int(new_agents.n_agents[t])
            for n in range(n_a):
                raw_uid = new_agents.unique_ids[t][n]
                if raw_uid not in new_uids:
                    uid = raw_uid
                    while uid in used_uids:
                        uid += 1
                    new_uids[raw_uid] = uid
                    used_uids.append(uid)
                unique_ids[t][i] = new_uids[raw_uid]
                type_ids[t][i] = new_agents.type_ids[t][n]
                types[t].append(new_agents.types[t][n])
                i += 1
        self.unique_ids = unique_ids
        self.types = types
        self.type_ids = type_ids
        self.n_agents = n_agents

    def __deepcopy__(self, memo):
        if self.type_ids is None:
            type_ids = None
        else:
            type_ids = np.copy(self.type_ids)
        result = type(self)(
            times=np.copy(self.times),
            n_agents=np.copy(self.n_agents),
            viz_types=np.copy(self.viz_types),
            unique_ids=np.copy(self.unique_ids),
            types=copy.deepcopy(self.types, memo),
            positions=np.copy(self.positions),
            radii=np.copy(self.radii),
            rotations=np.copy(self.rotations),
            n_subpoints=np.copy(self.n_subpoints),
            subpoints=np.copy(self.subpoints),
            draw_fiber_points=self.draw_fiber_points,
            type_ids=type_ids,
        )
        return result
