import fnmatch
import logging
import os.path
import pathlib
import shutil
from dataclasses import dataclass
from typing import Union, Optional, Tuple, Iterator, List

import requests
from filelock import FileLock
from hbutils.collection import nested_map
from hbutils.string import format_tree
from hbutils.system import TemporaryDirectory

from ..client import get_session, ENDPOINT, find_resource, Resource, find_model, find_version, OFFLINE_MODE, \
    OfflineModeEnabled
from ..utils import download_file


class LocalPrimaryFileUnset(Exception):
    pass


class LocalFileNotFound(Exception):
    pass


class LocalFileDuplicated(Exception):
    pass


@dataclass
class LocalFile:
    """
    Data class of local managed file.
    """
    filename: str
    hash: str
    size: int
    is_primary: bool


class VersionManager:
    """
    Management of specific version of model.
    """

    def __init__(self, root_dir: str, model_name_or_id: Union[str, int], creator: Optional[str],
                 version: Union[str, int], model_data: Optional[dict] = None, offline: bool = False):
        """
        Manages the local model files downloaded from civitai.com for a specific model and version.

        :param root_dir: The root directory where the model files will be managed.
        :param model_name_or_id: The name or ID of the model to manage files for.
        :param creator: Name of creator. ``None`` means anyone.
        :param version: The version ID or name to manage files for.
        :param model_data: Optional dictionary containing model information to avoid fetching it from the API.
        :param offline: If True, the manager operates in offline mode, using locally downloaded resources.
        """
        self.root_dir = root_dir
        self.model_name_or_id = model_name_or_id
        self.creator = creator
        self._model_data = model_data
        self.version = version
        self._version_data = None

        os.makedirs(self.root_dir, exist_ok=True)
        self._f_lock = os.path.join(self.root_dir, '.filelock')
        self._f_primary = os.path.join(self.root_dir, 'primary')
        self._d_files = os.path.join(self.root_dir, 'files')
        self._d_hashes = os.path.join(self.root_dir, 'hashes')
        self.lock = FileLock(self._f_lock)
        self._offline = offline

    @property
    def _primary_file(self) -> Optional[str]:
        if os.path.exists(self._f_primary):
            pfile_val = pathlib.Path(self._f_primary).read_text(encoding='utf-8').splitlines(keepends=False)[0]
            return pfile_val if pfile_val else None
        else:
            return None

    def _get_model(self):
        if not self._model_data:
            self._model_data = find_model(self.model_name_or_id, self.creator)
        return self._model_data

    def _get_version(self):
        if not self._version_data:
            self._version_data = find_version(self._get_model(), self.version)
        return self._version_data

    def _get_resource(self, pattern: str = None) -> Resource:
        return find_resource(self._get_model(), self._get_version(), pattern)

    def _file_path(self, filename: str):
        return os.path.join(self._d_files, filename)

    def _get_file_size(self, filename: str) -> Optional[int]:
        f = self._file_path(filename)
        return os.path.getsize(f) if os.path.exists(f) else None

    def _hash_path(self, filename: str):
        return os.path.join(self._d_hashes, f'{filename}.hash')

    def _get_file_hash(self, filename: str) -> Optional[str]:
        f = self._hash_path(filename)
        return pathlib.Path(f).read_text(encoding='utf-8').strip() if os.path.exists(f) else None

    def _get_file_meta(self, filename: str) -> Tuple[Optional[str], Optional[int]]:
        return self._get_file_hash(filename), self._get_file_size(filename)

    def _need_download_check(self, resource: Resource):
        local_hash, local_size = self._get_file_meta(resource.filename)
        if not local_hash or local_size is None:
            return True
        else:
            return (resource.size != local_size) or (resource.sha256 != local_hash)

    def _iter_local_files(self) -> Iterator[Tuple[str, str, int]]:
        if os.path.exists(self._d_files):
            for f in os.listdir(self._d_files):
                _hash, _size = self._get_file_meta(f)
                if not _hash or _size is None:
                    continue

                yield f, _hash, _size

    def _download_resource(self, resource: Resource):
        with TemporaryDirectory() as td:
            file = os.path.join(td, resource.filename)
            download_file(
                resource.url, file,
                expected_size=resource.size,
                desc=resource.filename,
                session=get_session(),
            )

            os.makedirs(self._d_files, exist_ok=True)
            shutil.copyfile(file, self._file_path(resource.filename))
            os.makedirs(self._d_hashes, exist_ok=True)
            with open(self._hash_path(resource.filename), 'w', encoding='utf-8') as hf:
                hf.write(resource.sha256)

            if resource.is_primary:
                with open(self._f_primary, 'w', encoding='utf-8') as pf:
                    pf.write(resource.filename)

    def _try_sync_from_site(self, pattern: str = None):
        try:
            if OFFLINE_MODE or self._offline:
                raise OfflineModeEnabled

            resource = self._get_resource(pattern)
            logging.debug(f'Resource found from {ENDPOINT!r}: {resource!r}')
            if self._need_download_check(resource):
                logging.debug('The resource is not available locally or has been updated. '
                              'The download will commence shortly.')
                self._download_resource(resource)
        except (requests.exceptions.SSLError, requests.exceptions.ProxyError):
            # Actually raise for those subclasses of ConnectionError
            raise
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                OfflineModeEnabled,
        ):
            # ignore this, use the local models
            logging.debug('Offline environment detected, using locally downloaded resources.')

    def get_file(self, pattern: str = None):
        """
        Get the local file path of the specified model file.

        :param pattern: The pattern or name of the file to get. If None, the primary file will be returned.
        :type pattern: str
        :return: The local path of the specified model file.
        :rtype: str
        :raises LocalPrimaryFileUnset: If the primary file is not set and no specific pattern is provided.
        :raises LocalFileNotFound: If the specified file is not found locally.
        :raises LocalFileDuplicated: If multiple files matching the pattern are found locally.
        """
        with self.lock:
            self._try_sync_from_site(pattern)

            if pattern is None:
                pattern = self._primary_file
                fullmatch = True
                if pattern is None:
                    raise LocalPrimaryFileUnset(self.model_name_or_id, self.version)
            else:
                fullmatch = False

            matched_files = []
            if os.path.exists(self._d_files):
                for filename in os.listdir(self._d_files):
                    if (fullmatch and filename == pattern) or \
                            (not fullmatch and fnmatch.fnmatch(filename, pattern)):
                        matched_files.append(filename)

            if not matched_files:
                raise LocalFileNotFound(self.model_name_or_id, self.version)
            elif len(matched_files) > 1:
                raise LocalFileDuplicated(self.model_name_or_id, self.version, matched_files)
            else:
                local_file = self._file_path(matched_files[0])
                assert os.path.exists(local_file), \
                    f'The expected resource file {local_file!r} was not found, ' \
                    f'indicating a BUG. Please contact the developer.'
                return local_file

    def list_files(self) -> List[LocalFile]:
        """
        List all the local model files associated with this version manager.

        :return: A list of LocalFile objects containing information about each local model file.
        :rtype: List[LocalFile]
        """
        with self.lock:
            retval = []
            primary_file = self._primary_file
            for filename, hash_, size_ in self._iter_local_files():
                retval.append(LocalFile(filename, hash_, size_, filename == primary_file))

            return retval

    @property
    def total_size(self) -> int:
        """
        Get the total size of all the local model files associated with this version manager.

        :return: The total size in bytes.
        :rtype: int
        """
        with self.lock:
            return sum((file.size for file in self.list_files()))

    def delete_file(self, filename):
        """
        Delete the specified model file from the local storage.

        :param filename: The name of the file to delete.
        :type filename: str
        :raises LocalFileNotFound: If the specified file is not found locally.
        """
        with self.lock:
            fp = self._file_path(filename)
            hp = self._hash_path(filename)
            if not os.path.exists(fp) and not os.path.exists(hp):
                raise LocalFileNotFound(self.model_name_or_id, self.version, filename)
            else:
                if os.path.exists(fp):
                    os.remove(fp)
                if os.path.exists(hp):
                    os.remove(hp)

    def _repr(self):
        return f'<{self.__class__.__name__} model: {self.model_name_or_id!r}, version: {self.version!r}>'

    def _tree(self):
        return self, [(item, []) for item in sorted(self.list_files(), key=repr)]

    def __str__(self):
        return format_tree(
            nested_map(repr, self._tree()),
            lambda x: x[0],
            lambda x: x[1],
        )

    def __repr__(self):
        return self._repr()
