from __future__ import annotations

import datetime
import functools
import json
import logging
from collections.abc import Container, Iterable, Mapping
from typing import Any, Literal, TypeVar

import cv2
import npc_io
import npc_sync
import numpy as np
import numpy.typing as npt
import upath
from typing_extensions import TypeAlias

logger = logging.getLogger(__name__)


MVRInfoData: TypeAlias = Mapping[str, Any]
"""Contents of `RecordingReport` from a camera's info.json for an MVR
recording."""

CameraName: TypeAlias = Literal["eye", "face", "behavior"]


class MVRDataset:
    """A collection of paths + data for processing the output from MVR for one
    session.

    Expectations:

    - 3 .mp4/.avi video file paths (eye, face, behavior)
    - 3 .json info file paths (eye, face, behavior)
    - the associated data as Python objects for each of the above (e.g mp3 -> CV2,
    json -> dict)

    - 1 sync file path (h5)
    - sync data as a SyncDataset object

    Assumptions:
    - all files live in the same directory (so we can initialize with a single path)
    - MVR was started after sync
    - MVR may have been stopped before sync

    >>> import npc_mvr

    >>> d = npc_mvr.MVRDataset('s3://aind-ephys-data/ecephys_670248_2023-08-03_12-04-15')

    # get paths
    >>> d.video_paths['behavior']
    S3Path('s3://aind-ephys-data/ecephys_670248_2023-08-03_12-04-15/behavior_videos/Behavior_20230803T120430.mp4')
    >>> d.info_paths['behavior']
    S3Path('s3://aind-ephys-data/ecephys_670248_2023-08-03_12-04-15/behavior_videos/Behavior_20230803T120430.json')
    >>> d.sync_path
    S3Path('s3://aind-ephys-data/ecephys_670248_2023-08-03_12-04-15/behavior/20230803T120415.h5')

    # get data
    >>> type(d.video_data['behavior'])
    <class 'cv2.VideoCapture'>
    >>> type(d.info_data['behavior'])
    <class 'dict'>
    >>> type(d.sync_data)
    <class 'npc_sync.sync.SyncDataset'>

    # get frame times for each camera on sync clock
    # - nans correspond to frames not recorded on sync
    # - first nan is metadata frame
    >>> d.frame_times['behavior']
    array([     nan, 14.08409, 14.10075, ...,      nan,      nan,      nan])
    >>> d.validate()
    """

    def __init__(
        self, session_dir: npc_io.PathLike, sync_path: npc_io.PathLike | None = None
    ) -> None:
        self.session_dir = npc_io.from_pathlike(session_dir)
        if sync_path is not None:
            self.sync_path = npc_io.from_pathlike(sync_path)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.session_dir})"

    @property
    def session_dir(self) -> upath.UPath:
        return self._session_dir

    @session_dir.setter
    def session_dir(self, value: npc_io.PathLike) -> None:
        path = npc_io.from_pathlike(value)
        if path.name in ("behavior", "behavior_videos", "behavior-videos"):
            path = path.parent
            logger.debug(
                f"Setting session directory as {path}: after March 2024 video and sync no longer stored together"
            )
        self._session_dir = path

    @npc_io.cached_property
    def is_cloud(self) -> bool:
        return self.session_dir.protocol not in ("file", "")

    @npc_io.cached_property
    def sync_dir(self) -> upath.UPath:
        if (path := self.session_dir / "behavior").exists():
            return path
        return self.session_dir

    @npc_io.cached_property
    def video_dir(self) -> upath.UPath:
        if not self.is_cloud:
            return self.session_dir
        for name in ("behavior_videos", "behavior-videos", "behavior"):
            if (path := self.session_dir / name).exists():
                return path
        return self.session_dir

    @npc_io.cached_property
    def frame_times(self) -> dict[CameraName, npt.NDArray[np.float64]]:
        """Returns frametimes (in seconds) as measured on sync clock for each
        camera.

        - see `get_video_frame_times` for more details
        """
        return {
            get_camera_name(p.stem): times
            for p, times in get_video_frame_times(
                self.sync_data, *self.video_paths.values()
            ).items()
        }

    @npc_io.cached_property
    def video_paths(self) -> dict[CameraName, upath.UPath]:
        return {
            get_camera_name(p.stem): p for p in get_video_file_paths(self.video_dir)
        }

    @npc_io.cached_property
    def video_data(self) -> npc_io.LazyDict[str, cv2.VideoCapture]:
        return npc_io.LazyDict(
            (camera_name, (get_video_data, (path,), {}))
            for camera_name, path in self.video_paths.items()
        )

    @npc_io.cached_property
    def info_paths(self) -> dict[CameraName, upath.UPath]:
        return {
            get_camera_name(p.stem): p
            for p in get_video_info_file_paths(self.video_dir)
        }

    @npc_io.cached_property
    def info_data(self) -> dict[CameraName, MVRInfoData]:
        return {
            camera_name: get_video_info_data(path)
            for camera_name, path in self.info_paths.items()
        }

    @npc_io.cached_property
    def sync_path(self) -> upath.UPath:
        return npc_sync.get_single_sync_path(self.sync_dir)

    @npc_io.cached_property
    def sync_data(self) -> npc_sync.SyncDataset:
        return npc_sync.get_sync_data(self.sync_path)

    @npc_io.cached_property
    def video_start_times(self) -> dict[CameraName, datetime.datetime]:
        """Naive datetime of when the video recording started.
        - can be compared to `sync_data.start_time` to check if MVR was started
          after sync.
        """
        return {
            camera_name: datetime.datetime.fromisoformat(
                self.info_data[camera_name]["TimeStart"][:-1]
            )  # discard 'Z'
            for camera_name in self.info_data
        }

    @npc_io.cached_property
    def augmented_camera_info(self) -> dict[CameraName, dict[str, Any]]:
        cam_exposing_times = get_cam_exposing_times_on_sync(self.sync_data)
        cam_transfer_times = get_cam_transfer_times_on_sync(self.sync_data)
        cam_exposing_falling_edge_times = get_cam_exposing_falling_edge_times_on_sync(
            self.sync_data
        )
        augmented_camera_info = {}
        for camera_name, video_path in self.video_paths.items():
            camera_info = dict(self.info_data[camera_name])  # copy
            frames_lost = camera_info["FramesLostCount"]

            num_exposures = cam_exposing_times[camera_name].size
            num_transfers = cam_transfer_times[camera_name].size

            num_frames_in_video = get_total_frames_in_video(video_path)
            num_expected_from_sync = num_transfers - frames_lost + 1
            signature_exposures = (
                cam_exposing_falling_edge_times[camera_name][:10]
                - cam_exposing_times[camera_name][:10]
            )

            camera_info["num_frames_exposed"] = num_exposures
            camera_info["num_frames_transfered"] = num_transfers
            camera_info["num_frames_in_video"] = num_frames_in_video
            camera_info["num_frames_expected_from_sync"] = num_expected_from_sync
            camera_info["expected_minus_actual"] = (
                num_expected_from_sync - num_frames_in_video
            )
            camera_info["num_frames_from_sync"] = len(
                get_video_frame_times(
                    self.sync_path,
                    self.video_paths[camera_name],
                    apply_correction=False,
                )[self.video_paths[camera_name]]
            )
            camera_info["signature_exposure_duration"] = np.round(
                np.median(signature_exposures), 3
            )
            camera_info["lost_frame_percentage"] = (
                100 * camera_info["FramesLostCount"] / camera_info["FramesRecorded"]
            )
            augmented_camera_info[camera_name] = camera_info
        return augmented_camera_info

    def validate(self) -> None:
        """Check all data required for processing is present and consistent. Check dropped frames
        count."""
        for camera in self.video_paths:
            video = self.video_data[camera]
            info_json = self.info_data[camera]
            augmented_info = self.augmented_camera_info[camera]
            times = self.frame_times[camera]

            if not times.any() or np.isnan(times).all():
                raise AssertionError(f"No frames recorded on sync for {camera}")
            if (a := video.get(cv2.CAP_PROP_FRAME_COUNT)) - (
                b := info_json["FramesRecorded"]
            ) > 1:
                # metadata frame is added to the video file, so the difference should be 1
                raise AssertionError(
                    f"Frame count from {camera} video file ({a}) does not match info.json ({b})"
                )
            if self.video_start_times[camera] < self.sync_data.start_time:
                raise AssertionError(
                    f"Video start time is before sync start time for {camera}"
                )

            if not is_acceptable_frame_rate(info_json["FPS"]):
                raise AssertionError(f"Invalid frame rate: {info_json['FPS']=}")

            if not is_acceptable_lost_frame_percentage(
                augmented_info["lost_frame_percentage"]
            ):
                raise AssertionError(
                    f"Lost frame percentage too high: {augmented_info['lost_frame_percentage']=}"
                )

            if not is_acceptable_expected_minus_actual_frame_count(
                augmented_info["expected_minus_actual"]
            ):
                # if number of frame times on sync matches the number expected, this isn't a hard failure
                if (
                    augmented_info["num_frames_expected_from_sync"]
                    != augmented_info["num_frames_from_sync"]
                ):
                    raise AssertionError(
                        f"Expected minus actual frame count too high: {augmented_info['expected_minus_actual']=}"
                    )


def is_acceptable_frame_rate(frame_rate: float) -> bool:
    return abs(frame_rate - 60) <= 0.05


def is_acceptable_lost_frame_percentage(lost_frame_percentage: float) -> bool:
    return lost_frame_percentage < 0.05


def is_acceptable_expected_minus_actual_frame_count(
    expected_minus_actual: int | float,
) -> bool:
    return abs(expected_minus_actual) < 20


def get_camera_name(path: str) -> CameraName:
    names: dict[str, CameraName] = {
        "eye": "eye",
        "face": "face",
        "beh": "behavior",
    }
    try:
        return names[next(n for n in names if n in str(path).lower())]
    except StopIteration as exc:
        raise ValueError(f"Could not extract camera name from {path}") from exc


def get_video_frame_times(
    sync_path_or_dataset: npc_io.PathLike | npc_sync.SyncDataset,
    *video_paths: npc_io.PathLike,
    apply_correction: bool = True,
) -> dict[upath.UPath, npt.NDArray[np.float64]]:
    """Returns frametimes as measured on sync clock for each video file.

    If a single directory is passed, video files in that directory will be
    found. If multiple paths are passed, the video files will be filtered out.

    - keys are video file paths
    - values are arrays of frame times in seconds
    - the first frametime will be a nan value (corresponding to a metadata frame)
    - frames at the end may also be nan values:
        MVR previously ceased all TTL pulses before the recording was
        stopped, resulting in frames in the video that weren't registered
        in sync. MVR was fixed July 2023 after Corbett discovered the issue.

        (only applied if `apply_correction` is True)

    - frametimes from sync may be cut to match the number of frames in the video:
        after July 2023, we started seeing video files that had fewer frames than
        timestamps in sync file.

        (only applied if `apply_correction` is True)

    >>> sync_path = 's3://aind-private-data-prod-o5171v/ecephys_708019_2024-03-22_15-33-01/behavior/20240322T153301.h5'
    >>> video_path = 's3://aind-private-data-prod-o5171v/ecephys_708019_2024-03-22_15-33-01/behavior-videos'
    >>> frame_times = get_video_frame_times(sync_path, video_path)
    >>> [len(frames) for frames in frame_times.values()]
    [103418, 103396, 103406]
    >>> sync_path = 's3://aind-ephys-data/ecephys_670248_2023-08-03_12-04-15/behavior/20230803T120415.h5'
    >>> video_path = 's3://aind-ephys-data/ecephys_670248_2023-08-03_12-04-15/behavior_videos'
    >>> frame_times = get_video_frame_times(sync_path, video_path)
    >>> [len(frames) for frames in frame_times.values()]
    [304233, 304240, 304236]
    """
    videos = get_video_file_paths(*video_paths)
    jsons = get_video_info_file_paths(*video_paths)
    camera_to_video_path = {get_camera_name(path.stem): path for path in videos}
    camera_to_json_data = {
        get_camera_name(path.stem): get_video_info_data(path) for path in jsons
    }
    camera_exposing_times = get_cam_exposing_times_on_sync(sync_path_or_dataset)
    frame_times: dict[upath.UPath, npt.NDArray[np.floating]] = {}
    for camera in camera_exposing_times:
        if camera in camera_to_video_path:
            num_frames_in_video = get_total_frames_in_video(
                camera_to_video_path[camera]
            )
            camera_frame_times = remove_lost_frame_times(
                camera_exposing_times[camera],
                get_lost_frames_from_camera_info(camera_to_json_data[camera]),
            )
            # Insert a nan frame time at the beginning to account for metadata frame
            camera_frame_times = np.insert(camera_frame_times, 0, np.nan)
            # append nan frametimes for frames in the video file but are
            # unnaccounted for on sync:
            if (
                apply_correction
                and (
                    frames_missing_from_sync := num_frames_in_video
                    - len(camera_frame_times)
                )
                > 0
            ):
                camera_frame_times = np.append(
                    camera_frame_times,
                    np.full(frames_missing_from_sync, np.nan),
                )
            # cut times of sync events that don't correspond to frames in the video:
            elif apply_correction and (len(camera_frame_times) > num_frames_in_video):
                camera_frame_times = camera_frame_times[:num_frames_in_video]
            if apply_correction:
                assert len(camera_frame_times) == num_frames_in_video, (
                    f"Expected {num_frames_in_video} frame times, got {len(camera_frame_times)} "
                    f"for {camera_to_video_path[camera]}"
                    f"{'' if apply_correction else ' (try getting frametimes with `apply_correction=True`)'}"
                )
            frame_times[camera_to_video_path[camera]] = camera_frame_times
    return frame_times


def get_cam_line_times_on_sync(
    sync_path_or_dataset: npc_io.PathLike | npc_sync.SyncDataset,
    sync_line_suffix: str,
    edge_type: Literal["rising", "falling"] = "rising",
) -> dict[Literal["behavior", "eye", "face"], npt.NDArray[np.float64]]:
    sync_data = npc_sync.get_sync_data(sync_path_or_dataset)

    edge_getter = (
        sync_data.get_rising_edges
        if edge_type == "rising"
        else sync_data.get_falling_edges
    )

    line_times = {}
    for line in (line for line in sync_data.line_labels if sync_line_suffix in line):
        camera_name = get_camera_name(line)
        line_times[camera_name] = edge_getter(line, units="seconds")
    return line_times


def get_cam_exposing_times_on_sync(
    sync_path_or_dataset: npc_io.PathLike | npc_sync.SyncDataset,
) -> dict[Literal["behavior", "eye", "face"], npt.NDArray[np.float64]]:
    return get_cam_line_times_on_sync(sync_path_or_dataset, "_cam_exposing")


def get_cam_exposing_falling_edge_times_on_sync(
    sync_path_or_dataset: npc_io.PathLike | npc_sync.SyncDataset,
) -> dict[Literal["behavior", "eye", "face"], npt.NDArray[np.float64]]:
    return get_cam_line_times_on_sync(sync_path_or_dataset, "_cam_exposing", "falling")


def get_cam_transfer_times_on_sync(
    sync_path_or_dataset: npc_io.PathLike | npc_sync.SyncDataset,
) -> dict[Literal["behavior", "eye", "face"], npt.NDArray[np.float64]]:
    return get_cam_line_times_on_sync(sync_path_or_dataset, "_cam_frame_readout")


def get_lost_frames_from_camera_info(
    info_path_or_data: MVRInfoData | npc_io.PathLike,
) -> npt.NDArray[np.int32]:
    """
    >>> get_lost_frames_from_camera_info({'LostFrames': ['1-2,4-5,7']})
    array([0, 1, 3, 4, 6])
    """
    info = get_video_info_data(info_path_or_data)

    if info.get("FramesLostCount") == 0:
        return np.array([])

    assert isinstance(_lost_frames := info["LostFrames"], list)
    lost_frame_spans: list[str] = _lost_frames[0].split(",")

    lost_frames: list[int] = []
    for span in lost_frame_spans:
        start_end = span.split("-")
        if len(start_end) == 1:
            lost_frames.append(int(start_end[0]))
        else:
            lost_frames.extend(np.arange(int(start_end[0]), int(start_end[1]) + 1))

    return np.subtract(lost_frames, 1)  # lost frames in info are 1-indexed


def get_total_frames_from_camera_info(
    info_path_or_data: MVRInfoData | npc_io.PathLike,
) -> int:
    """`FramesRecorded` in info.json plus 1 (for metadata frame)."""
    info = get_video_info_data(info_path_or_data)
    assert isinstance((reported := info.get("FramesRecorded")), int)
    return reported + 1


NumericT = TypeVar("NumericT", bound=np.generic, covariant=True)


def remove_lost_frame_times(
    frame_times: Iterable[NumericT], lost_frame_idx: Container[int]
) -> npt.NDArray[NumericT]:
    """
    >>> remove_lost_frame_times([1., 2., 3., 4., 5.], [1, 3])
    array([1., 3., 5.])
    """
    return np.array(
        [t for idx, t in enumerate(frame_times) if idx not in lost_frame_idx]
    )


def get_video_file_paths(*paths: npc_io.PathLike) -> tuple[upath.UPath, ...]:
    if len(paths) == 1 and npc_io.from_pathlike(paths[0]).is_dir():
        upaths = tuple(npc_io.from_pathlike(paths[0]).glob("*"))
    else:
        upaths = tuple(npc_io.from_pathlike(p) for p in paths)
    return tuple(
        p
        for p in upaths
        if p.suffix in (".avi", ".mp4")
        and any(label in p.stem.lower() for label in ("eye", "face", "beh"))
    )


def get_video_info_file_paths(*paths: npc_io.PathLike) -> tuple[upath.UPath, ...]:
    return tuple(
        p.with_suffix(".json").with_stem(p.stem.replace(".mp4", "").replace(".avi", ""))
        for p in get_video_file_paths(*paths)
    )


def get_video_info_data(path_or_info_data: npc_io.PathLike | Mapping) -> MVRInfoData:
    if isinstance(path_or_info_data, Mapping):
        if "RecordingReport" in path_or_info_data:
            return path_or_info_data["RecordingReport"]
        return path_or_info_data
    return json.loads(npc_io.from_pathlike(path_or_info_data).read_bytes())[
        "RecordingReport"
    ]


def get_video_data(
    video_or_video_path: cv2.VideoCapture | npc_io.PathLike,
) -> cv2.VideoCapture:
    """
    >>> path = 's3://aind-ephys-data/ecephys_660023_2023-08-08_07-58-13/behavior_videos/Behavior_20230808T130057.mp4'
    >>> v = get_video_data(path)
    >>> assert isinstance(v, cv2.VideoCapture)
    >>> assert v.get(cv2.CAP_PROP_FRAME_COUNT) != 0
    """
    if isinstance(video_or_video_path, cv2.VideoCapture):
        return video_or_video_path

    video_path = npc_io.from_pathlike(video_or_video_path)
    # check if this is a local or cloud path
    is_local = video_path.protocol in ("file", "")
    if is_local:
        path = video_path.as_posix()
    else:
        path = npc_io.get_presigned_url(video_path)
    return cv2.VideoCapture(path)


@functools.cache
def get_total_frames_in_video(
    video_path: npc_io.PathLike,
) -> int:
    v = get_video_data(video_path)
    num_frames = v.get(cv2.CAP_PROP_FRAME_COUNT)

    return int(num_frames)


if __name__ == "__main__":
    from npc_mvr import testmod

    testmod()
