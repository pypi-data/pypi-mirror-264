import logging
import shutil
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, Dict, Union, Type
from zipfile import ZipFile

import botocore
from boto3_type_annotations.s3 import Client as S3Client

from cvd.datasets.exporter.xml import import_from_xml, exporter_to_xml
from cvd.datasets.interfaces.idataset import IDataset
from cvd.datasets.meta import DatasetMeta
from cvd.datasets.zoo.internal_representation import _InternalFileMeta, _InternalDataset, _InternalMeta, \
    _InternalFilesMeta, _InternalDatasetMeta, _InternalDatasetsMeta
from cvd.tools.hash import md5

from tqdm.auto import tqdm


class Datasets:
    def __init__(
        self,
        s3client: Optional[S3Client] = None,
        s3_datasets_bucket: Optional[str] = None,
        s3_datasets_folder: Optional[str] = None,
        data_folder: Optional[Path] = None
    ):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._s3 = s3client
        if self._s3 is not None:
            assert s3_datasets_bucket, "Please set datasets_bucket"
            assert s3_datasets_folder, "Please set datasets_folder"
            self._s3_datasets_bucket = s3_datasets_bucket
            self._s3_datasets_folder = s3_datasets_folder

        if data_folder is None:
            self._data_folder = Path.home() / "Datasets"
            self._data_folder.mkdir(exist_ok=True)
        else:
            self._data_folder = data_folder
            if not self._data_folder.is_dir():
                self._logger.info(f"The data folder `{self._data_folder}` doesn't exist and will be created")
                self._data_folder.mkdir(parents=True)

        self._data_folder_annotations = self._data_folder / "annotations"
        self._data_folder_images = self._data_folder / "images"
        self._data_folder_annotations.mkdir(exist_ok=True)
        self._data_folder_images.mkdir(exist_ok=True)

        self._datasets_meta_file_path = self._data_folder / "datasets_meta.xml"
        self._data_files_meta_path = self._data_folder / "data_files_meta.xml"
        self._datasets_meta: Optional[_InternalDatasetsMeta] = None
        self._data_files_meta: Optional[_InternalFilesMeta] = None
        self._read_meta_information()

    def _read_meta_information(self, force: bool = False):
        _datasets_meta = self.read_meta_file(
            meta_file=self._datasets_meta_file_path,
            class_loaded=_InternalDatasetsMeta,
            force=force
        )
        _data_files_meta = self.read_meta_file(
            meta_file=self._data_files_meta_path,
            class_loaded=_InternalFilesMeta,
            force=force
        )
        if _datasets_meta is None or _data_files_meta is None:
            raise Exception("The local version library is great then remote library.")
        self._datasets_meta = _datasets_meta
        self._data_files_meta = _data_files_meta

    def read_meta_file(
            self,
            meta_file: Path,
            class_loaded: Type[Union[_InternalDatasetsMeta, _InternalFilesMeta]],
            force: bool = False
    ) -> Optional[Union[_InternalDatasetsMeta, _InternalFilesMeta]]:
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            tmp_meta_file = tmp_path/"tmp.xml"
            try:
                local_meta = import_from_xml(meta_file)
            except IOError:
                local_meta = class_loaded()
            if force or (not meta_file.is_file() and self._s3 is not None):
                self._download_file(
                    src_file=self._s3_datasets_folder + f"/{meta_file.name}",
                    dst_file=tmp_meta_file
                )
                try:
                    s3_meta = import_from_xml(tmp_meta_file)
                except IOError:
                    s3_meta = class_loaded()
                if local_meta.version <= s3_meta.version:
                    if s3_meta.version > 0:
                        shutil.copy(tmp_meta_file, meta_file)
                    return s3_meta
                return None
            else:
                return local_meta

    def _upload_file(self, src_file: Path, dst_file: Union[Path, str]) -> bool:
        try:
            pbar = tqdm(total=src_file.stat().st_size, unit='B', unit_scale=True, unit_divisor=1024)
            self._s3.upload_file(str(src_file), self._s3_datasets_bucket, str(dst_file), Callback=pbar.update)
            pbar.close()
            self._logger.info(f"{src_file} are uploaded to remote library.")
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                self._logger.info(f"File `{src_file}` not uploaded on S3")
            else:
                self._logger.warning("Couldn't connect to s3.")
        return False

    def _download_file(self, src_file: Union[Path, str], dst_file: Path) -> bool:
        try:
            meta_data = self._s3.head_object(Bucket=self._s3_datasets_bucket, Key=str(src_file))
            pbar = tqdm(total=int(meta_data.get('ContentLength', 0)), unit='B', unit_scale=True, unit_divisor=1024)
            self._s3.download_file(self._s3_datasets_bucket, str(src_file), str(dst_file), Callback=pbar.update)
            pbar.close()
            self._logger.info(f"{Path(src_file).name} was downloaded from remote library.")
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                self._logger.info(f"File `{src_file}` not found on S3")
            else:
                self._logger.warning("Couldn't connect to s3.")
        return False

    def datasets(self) -> Dict[str, DatasetMeta]:
        return self._datasets_meta

    def _ds_meta_to_id(self, dataset_meta: DatasetMeta):
        return f"{dataset_meta.name}_{dataset_meta.part.value}_{dataset_meta.version}"

    def add(self, dataset: IDataset):
        _dataset_id = self._ds_meta_to_id(dataset.dataset_meta)
        if _dataset_id not in self._datasets_meta:
            _dataset_folder = self._data_folder_images / _dataset_id
            _dataset_folder.mkdir(exist_ok=True)
            _files, _annotations, _required_datasets = [], [], set()
            _datasets_info = _InternalDatasetMeta(deepcopy(dataset.dataset_meta))
            for ds_item in dataset:
                # TODO: cache md5 checksum in file_info
                file_md5 = md5(ds_item.file_info.abs_path)
                if file_md5 not in self._data_files_meta:
                    file_path = Path(ds_item.file_info.unique_id)
                    if not file_path.suffix:
                        file_path = file_path.parent / f"{file_path.name}{ds_item.file_info.abs_path.suffix}"
                    full_path_to_dst = _dataset_folder / file_path
                    full_path_to_dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(ds_item.file_info.abs_path, full_path_to_dst)
                    partial_path = Path(_dataset_id) / file_path
                    _tmp_file_indo = deepcopy(ds_item.file_info)
                    _tmp_file_indo.abs_path = None
                    _ifi = _InternalFileMeta(
                        file_info=_tmp_file_indo,
                        partial_path=partial_path,
                        dataset_id=_dataset_id,
                        duplicate=False
                    )
                    self._data_files_meta[file_md5] = _ifi
                    if ds_item.file_info.unique_id == 'MW-18Mar-21_000451.png':
                        print("file_md5 not in ", ds_item)
                else:
                    duplicated_ifi = self._data_files_meta[file_md5]
                    _tmp_file_indo = deepcopy(ds_item.file_info)
                    _ifi = _InternalFileMeta(
                        file_info=_tmp_file_indo,
                        partial_path=duplicated_ifi.partial_path,
                        dataset_id=duplicated_ifi.dataset_id,
                        duplicate=False
                    )
                    if _ifi.dataset_id != _dataset_id:
                        _datasets_info.add_dependency(_ifi.dataset_id)
                    else:
                        _ifi.duplicate = True
                        self._logger.warning(f"The added dataset contains duplicate data files. "
                                             f"`{_ifi.file_info.unique_id} and `{ds_item.file_info.unique_id}``")
                _files.append(_ifi)
                _annotations.append(ds_item.annotations)
            _empty_ds = dataset.__class__.__new__(dataset.__class__)
            _empty_ds.__init__()
            _dataset = _InternalDataset(
                files=_files,
                annotations=_annotations,
                dataset=_empty_ds,
            )
            self._datasets_meta[_dataset_id] = _datasets_info
            self._datasets_meta.inc_version()
            self._save_meta(self._datasets_meta, self._datasets_meta_file_path)
            self._data_files_meta.inc_version()
            self._save_meta(self._data_files_meta, self._data_files_meta_path)
            exporter_to_xml(_dataset, self._data_folder_annotations/f"{_dataset_id}.xml")
        else:
            self._logger.info("The dataset is already in the library. "
                              "If it is a modified dataset change its version.")

    def _save_meta(self, meta_object: _InternalMeta, output_file: Path):
        if output_file.is_file():
            file_meta: _InternalFilesMeta = import_from_xml(output_file)
            if file_meta.version > meta_object.version:
                raise Exception(f"The version of meta information in {output_file.name} file"
                                f"is great then your meta information`. Downgrade isn't possible")
        exporter_to_xml(meta_object, output_file)

    def datasets_ids(self):
        return self._datasets_meta.keys()

    def get_by_id(self, dataset_id: str):
        if dataset_id in self._datasets_meta:
            annotation_file = self._data_folder_annotations/f"{dataset_id}.xml"
            ds_image_path = self._data_folder_images/dataset_id
            if not annotation_file.is_file() or not ds_image_path.is_dir():
                self._logger.info(f"Downloading dataset `{dataset_id}`")
                self._download(dataset_id)
                self._logger.info(f"{dataset_id} dataset was downloaded")
            internal_dataset_meta = self._datasets_meta[dataset_id]
            internal_dataset: _InternalDataset = import_from_xml(annotation_file)
            new_dataset = internal_dataset.dataset
            new_dataset.dataset_meta = internal_dataset_meta.dataset_meta

            for _internal_file_info, ann in zip(internal_dataset.files, internal_dataset.annotations):
                file_info = _internal_file_info.file_info
                file_info.abs_path = self._data_folder_images / _internal_file_info.partial_path
                new_dataset.add_item(file_info, ann)
            return new_dataset
        else:
            self._logger.warning(f"Datasets with `{dataset_id}` id not found")

            print(f"Datasets with `{dataset_id}` id not found. You should get pull. But be careful, it will overwrite all your local datasets files!")
            return None

    def _download_to_tmp(self, tmpdirname: Path, dataset_id: str):
        annotation_file = self._data_folder_annotations / f"{dataset_id}.xml"
        ds_image_path = self._data_folder_images / dataset_id
        if not annotation_file.is_file() or not ds_image_path.is_dir():
            self._logger.info(f"Downloading dataset `{dataset_id}`")
            ds_zip_name = f"{dataset_id}.zip"
            tmp_file_path = Path(tmpdirname) / ds_zip_name
            self._download_file(Path(self._s3_datasets_folder) / ds_zip_name, tmp_file_path)
            with ZipFile(tmp_file_path, 'r') as zf:
                zf.extractall(self._data_folder)
            self._logger.debug(f"{dataset_id} dataset was downloaded")

    def pull(self):
        self._read_meta_information(force=True)

    def _download(self, dataset_id: str):
        with TemporaryDirectory() as tmpdirname:
            self._download_to_tmp(tmpdirname, dataset_id)
            ds_meta = self._datasets_meta[dataset_id]
            for _dataset_id in ds_meta.dataset_dependences:
                self._download(_dataset_id)

    def uploads(self):
        with TemporaryDirectory() as tmpdirname:
            tmp_path = Path(tmpdirname)
            # print('tmp_path=', tmp_path)
            s3_meta_file = tmp_path / "s3_meta_file.xml"
            status = self._download_file(
                src_file=self._s3_datasets_folder + f"/{self._datasets_meta_file_path.name}",
                dst_file=s3_meta_file
            )
            if status:
                s3_ds_meta = import_from_xml(s3_meta_file)
            else:
                s3_ds_meta = _InternalDatasetsMeta()

            # TODO: 1) Log information about uploaded dataset 2)  Handling of exceptional situations when loading
            #  multiple datasets (not enough space on disk, break of connection),
            #  you need to download or adjust meta files after loading each dataset.
            #  3) Deleting dataset zip files after downloading
            for dataset_id, _ds_meta in self._datasets_meta.items():
                if dataset_id not in s3_ds_meta:
                    zip_file_path = tmp_path / f'{dataset_id}.zip'
                    zf = ZipFile(zip_file_path, mode='w')
                    internal_image_dataset = import_from_xml(self._data_folder_annotations / f"{dataset_id}.xml")
                    for file_info in internal_image_dataset.files:
                        if not file_info.duplicate and file_info.dataset_id == dataset_id:
                            zf.write(
                                filename=self._data_folder_images / file_info.partial_path,
                                arcname=f"{self._data_folder_images.name}/{str(file_info.partial_path)}"
                            )
                    zf.write(
                        filename=self._data_folder_annotations / f"{dataset_id}.xml",
                        arcname=f"{self._data_folder_annotations.name}/{dataset_id}.xml"
                    )
                    zf.close()
                    status = self._upload_file(zip_file_path, self._s3_datasets_folder + f"/{zip_file_path.name}")
                    if status:
                        self._logger.info(f"{dataset_id} datasets uploaded to library")

            self._upload_file(
                src_file=self._data_files_meta_path,
                dst_file=self._s3_datasets_folder + f"/{self._data_files_meta_path.name}"
            )

            self._upload_file(
                src_file=self._datasets_meta_file_path,
                dst_file=self._s3_datasets_folder + f"/{self._datasets_meta_file_path.name}"
            )


