import collections
import itertools
import logging
import os
import time
from datetime import timedelta

from pathlib import Path
from typing import List, Optional, Type

from benchmark.config import METRICS
from benchmark.quality.benchmark_pipeline import BenchmarkFactory, benchmark_pipeline_stream, PipelinePart, \
    BenchmarkPipeline
from benchmark.quality.calculate_metrics import filter_occluded, print_results
from benchmark.quality.local_metrics import calculate_metrics
from benchmark.quality.utils import cvat_xml_to_dataframe
from src.model_config_generator import generate_configs
from src.tracker import STracker
from src.utils import get_video_info
import pandas as pd


def detection_metrics(
        data_path: Path,
        detected_min_h: Optional[List[float]] = None,
        version="test",
        pipeline_part=PipelinePart.PERSON_DETECTION,
        label: str = "person",
        result_folder: Optional[Path] = None
):
    """ Metric calculation entrypoint. """
    logger = logging.getLogger("CalMetric")
    metrics = METRICS[pipeline_part]
    occlusion = []
    frame_step = 1
    if result_folder is None:
        result_folder = data_path
    if detected_min_h is None:
        detected_min_h = [0.0]
    if detected_min_h:
        min_h_list = [float(val) for val in detected_min_h]

    data_path = data_path.absolute()
    if not data_path.is_dir():
        raise AssertionError('Argument `data-path` should specify a folder.')

    fragment_collections = collections.defaultdict(list)
    files = [data_path.glob(f'**/*{e}') for e in ['.mp4', '.avi']]
    files = sorted(list(itertools.chain.from_iterable(files)))
    for vid_path in files:
        for min_h in min_h_list:
            logger.info(f'Calculating predictions for {min_h}.')
            gt_path = vid_path.with_suffix('.xml')
            preds_path = result_folder / f"{vid_path.stem}_{pipeline_part}_{version}_0.0.h5"
            if gt_path.exists() and preds_path.exists():
                fragment_collections[vid_path.parent.stem].append((
                    vid_path.stem,
                    min_h * get_video_info(vid_path)["height"],
                    cvat_xml_to_dataframe(gt_path, label),
                    pd.read_hdf(preds_path)
                ))
            else:
                logger.warning(
                    f'Skipping fragment {vid_path.stem}, '
                    f'GT found {gt_path.exists()}, predictions found {preds_path.exists()}'
                )

    if len(occlusion) > 0:
        fragment_collections = filter_occluded(occlusion, fragment_collections)

    results_csv_path = str(Path(data_path) / f'{pipeline_part}.csv')
    results = calculate_metrics(
        # flatten fragments dict to list
        [fragment for collection in fragment_collections.values() for fragment in collection],
        metrics=metrics,
        frame_step=frame_step
    )
    print_results(results, results_csv_path)

    results.to_csv(results_csv_path)
    return results


def predict_detection(
        data_path: Path,
        benchmark_pipeline_class: Type[BenchmarkPipeline],
        video_source: bool = True,
        detected_min_h: Optional[List[float]] = None,
        version: str = "test",
        save_frames: bool = False,
        save_result_to_df: bool = True,
        result_folder: Optional[Path] = None,
        pipeline_part: str = 'person-detection'
):  # pylint: disable=too-many-locals
    logger = logging.getLogger(__name__)
    if detected_min_h is None:
        detected_min_h = [0]

    if result_folder is None:
        result_folder = data_path

    version_suffix = str(pipeline_part)
    if version:
        version_suffix += f'_{version}'

    # set columns to parse data
    columns = benchmark_pipeline_class.get_result_columns()
    min_h_list = [0.0]
    if detected_min_h:
        min_h_list = [float(val) for val in detected_min_h]

    if video_source:
        # absolute path to video or folder
        data_path = Path(data_path).absolute()
        if data_path.is_dir():
            # get a list of fragments in collections directories for each possible file extension
            files = [data_path.glob(f'**/*{e}') for e in ['.mp4', '.avi']]
            # flatten list of fragment paths
            files = list(itertools.chain.from_iterable(files))
        else:
            files = [data_path]
        for filepath in files:
            predict_on_video(benchmark_pipeline_class, columns, filepath, logger, min_h_list, result_folder,
                             save_frames, save_result_to_df, version_suffix)
    else:
        predict_on_images(benchmark_pipeline_class, columns, data_path, logger, min_h_list, result_folder,
                          save_frames, save_result_to_df, version_suffix)


def predict_on_images(
        benchmark_pipeline_class,
        columns,
        filespath,
        logger,
        min_h_list,
        result_folder,
        save_frames,
        save_result_to_df,
        version_suffix
):
    print('filespath=', filespath)
    logger.info(f'Calculating predictions for {filespath}.')
    frames_dir_path = None
    print("result_folder===", result_folder)

    if save_frames:
        frames_dir_path = result_folder / f'{filespath.stem}_{version_suffix}_0.0'
        frames_dir_path.mkdir(parents=True, exist_ok=True)

    generate_configs(person_min_h=0)
    rows = []
    start_time = time.time()
    for det in benchmark_pipeline_stream(
            benchmark_pipeline_class,
            uri=str(filespath) + "/",
            width=702,
            height=702,
            frames_dir=frames_dir_path,
            image_source=True,
    ):
        if save_result_to_df:
            rows.append(det)

    exec_seconds = time.time() - start_time
    logger.info(f'Execution ended after {timedelta(seconds=exec_seconds)}')

    if save_result_to_df:
        print("result_folder===", result_folder)
        out_file = result_folder.parent / f'{filespath.stem}_{version_suffix}_0.0.h5'
        logger.info(f"Save result into {out_file}")
        results = pd.DataFrame(data=rows, columns=columns)
        results.insert(0, 'fragment_id', filespath.stem)
        results.to_hdf(str(out_file), 'data', 'w')
        logger.info(f'Predictions have been written to {out_file}.')


def predict_on_video(
        benchmark_pipeline_class,
        columns,
        filepath,
        logger,
        min_h_list,
        result_folder,
        save_frames,
        save_result_to_df,
        version_suffix
):
    logger.info(f'Calculating predictions for {filepath}.')
    info = get_video_info(filepath)
    width = int(info['width'])
    height = int(info['height'])
    # get a ref to tracker instance, width\height placeholder, will be set by person_tracker plugin
    tracker = STracker.get_instance(frame_width=width, frame_height=height)
    for min_h in min_h_list:
        logger.info(f'Calculating predictions for {min_h}.')

        frames_dir_path = None
        print("result_folder===", result_folder)

        if save_frames:
            frames_dir_path = result_folder / f'{filepath.stem}_{version_suffix}_{min_h}'
            frames_dir_path.mkdir(parents=True, exist_ok=True)

        generate_configs(person_min_h=int(min_h * height))
        rows = []
        # reset tracker state before processing next fragment
        # so that track numbers start from 1 again
        tracker.reset()
        logger.info(f"Start processing {filepath}")
        start_time = time.time()
        for det in benchmark_pipeline_stream(
                benchmark_pipeline_class,
                uri=filepath.as_uri(),
                width=width,
                height=height,
                frames_dir=frames_dir_path
        ):
            if save_result_to_df:
                rows.append(det)

        exec_seconds = time.time() - start_time
        logger.info(f'Execution ended after {timedelta(seconds=exec_seconds)}')
        logger.info(f'Processed {info["nb_frames"]} frames, {int(info["nb_frames"]) / exec_seconds:.2f} FPS')

        if save_result_to_df:
            print("result_folder===", result_folder)
            out_file = result_folder / f'{filepath.stem}_{version_suffix}_{min_h}.h5'
            logger.info(f"Save result into {out_file}")
            results = pd.DataFrame(data=rows, columns=columns)
            results.insert(0, 'fragment_id', filepath.stem)
            results.to_hdf(str(out_file), 'data', 'w')
            logger.info(f'Predictions have been written to {out_file}.')
