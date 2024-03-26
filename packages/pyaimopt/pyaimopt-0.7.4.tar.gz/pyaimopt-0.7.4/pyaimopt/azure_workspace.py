# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""
azure_workspace.py

Implements a workspace to run jobs on the online AIM service
"""
# pylint: disable=invalid-name

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from math import ceil
from typing import Dict, List, Tuple, NamedTuple, Optional
import io
import logging
import os
import base64  # Enable https transport to web server.
import random
import re
import time
import sys
import importlib.metadata  # PyAimOpt version check
import requests  # Enable https transport to web server.
from json5 import loads

from anyio import Lock, sleep
from dotenv import dotenv_values
from azure.core.exceptions import ResourceExistsError
from azure.identity import InteractiveBrowserCredential
from azure.storage.blob import ContainerClient
from packaging.version import Version
from .constants import has_data_file, create_empty_data_file, get_terms_of_usage_file
from .description import ProblemDescription
from .serialization import serialize, read_solution_from_stream
from .workspace import (
    Workspace,
    JobID,
    JobStatus,
    JobResult,
    Ok,
    Failed,
    Pending,
    create_job_id,
    jobid_as_short_string,
    jobid_from_short_string,
)
from .aim_credentials import AimCredentials
from .platform import (
    is_default_target_cpu,
    is_default_target_gpu,
    get_target_hardware_for_solver,
)


_logger = logging.getLogger(__name__)
_PACKAGE_FIRST_USE_FILE: str = "aim_past_first_use.txt"

PRIVACY_STATEMENT_URI: str = "https://go.microsoft.com/fwlink/?LinkId=521839"
__AZURE_STORAGE_ACCOUNT_RELEASE__: str = "https://aimdemorsa.blob.core.windows.net/"
__AZURE_STORAGE_ACCOUNT_DEBUG__: str = "https://mscamaimdsa.blob.core.windows.net"
__AZURE_STORAGE_ACCOUNT__: str = __AZURE_STORAGE_ACCOUNT_RELEASE__
__AZURE_SERVICE_ACCOUNT__: str = "https://aimdemorfunc.azurewebsites.net/api/Function4/"
# __AZURE_SERVICE_ACCOUNT__: str = "http://localhost:443/api/Function4/"
GREGOSLIVECO_ONMICROSOFT: str = "791cf287-d56f-4591-97a1-dbca68a63415"
FILE_NAME_FIRST_USE: str = "aim_on_first_use.txt"
TIMEOUT_SECONDS_DEFAULT: int = int(30)
TIMEOUT_SECONDS_MIN: int = int(1)
TIMEOUT_SECONDS_MAX: int = int(9999)  # Fit to 4-character suffix of upload name.
HTTP_TIMEOUT_SECS: int = int(30)
_HTTP_SSL_CERTIFICATE_VERIFY = bool(True)


__SIZEOF_MAX_BLOB_CONTAINER_NAME__: int = 17


def _make_blob_name(job_id: JobID, time_limit: int) -> str:
    """
    Create a blob name from the job id

    :param job_id: The job id
    :param time_limit: The time limit
    :returns: The blob name
    """
    assert time_limit > 0
    assert job_id is not None

    timestamp = datetime.now(tz=timezone.utc).strftime("%y%m%d%H%M%S")

    if time_limit > TIMEOUT_SECONDS_MAX:
        _logger.error(
            "time_limit %d exceeds maximum %d", time_limit, TIMEOUT_SECONDS_MAX
        )
        raise ValueError(
            f"time_limit {time_limit} exceeds maximum {TIMEOUT_SECONDS_MAX}"
        )

    # In case the user passes a float, then round up to the next integer.
    time_limit_orig = time_limit
    time_limit = ceil(time_limit)
    if time_limit != time_limit_orig:
        _logger.warning("time limit %d rounded up to %d", time_limit_orig, time_limit)

    tag = jobid_as_short_string(job_id)
    seconds = str(time_limit)
    pad = "0000"
    suffix = pad[len(seconds) :] + seconds

    if is_default_target_cpu():
        prefix = "c"
    elif is_default_target_gpu():
        prefix = "g"
    else:
        raise ValueError(f"Unknown target hardware {get_target_hardware_for_solver()}")

    return f"{prefix}{timestamp}_{tag}_{suffix}"


def _job_id_from_blob_name(blob_name: str) -> JobID:
    """
    Extract the job id from the blob name

    :param blob_name: The blob name
    :returns: The job id
    """
    left = blob_name.index("_")
    right = blob_name.rindex("_")
    tag = blob_name[(left + 1) : right]
    return jobid_from_short_string(tag)


def _time_limit_from_blob_name(blob_name: str) -> int:
    """
    Extract the time limit from the blob name

    :param blob_name: The blob name
    :returns: The time limit
    """
    right = blob_name.rindex("_")
    suffix = blob_name[(right + 1) :]
    return int(suffix)


def _submitted_time_from_blob_name(blob_name: str) -> datetime:
    """
    Extract the submitted time from the blob name

    :param blob_name: The blob name
    :returns: The submitted time
    """
    # left = blob_name.index("_")
    # timestamp = blob_name[1:left]
    timestamp = re.match(r"^.*?([0-9]+)_.*$", blob_name).group(1)
    return datetime.strptime(timestamp, "%y%m%d%H%M%S")


def _is_completed_successfully(blob_name: str) -> bool:
    """
    Check if the blob name indicates that the job is completed

    :param blob_name: The blob name
    :returns: True if the job is completed
    """
    return blob_name.startswith("G")


def _is_submission(blob_name: str) -> bool:
    """
    Check if the blob name indicates a job submission

    :param blob_name: The blob name
    :returns: True if the job is completed
    """
    return blob_name.startswith("g")


def _is_failed(blob_name: str) -> bool:
    """
    Check if the blob name indicates that the job failed

    :param blob_name: The blob name
    :returns: True if the job failed
    """
    return blob_name.startswith("E")


def _is_completed(blob_name: str) -> bool:
    """
    Check if the blob name indicates that the job is completed

    :param blob_name: The blob name
    :returns: True if the job is completed
    """
    return (
        _is_completed_successfully(blob_name)
        or _is_failed(blob_name)
        or _is_cancelled(blob_name)
    )


def _is_cancelled(blob_name: str) -> bool:
    """
    Check if the blob name indicates that the job was cancelled

    :param blob_name: The blob name
    :returns: True if the job was cancelled
    """
    return blob_name.startswith("C")


def _click_thru():
    """On first use: click-thru to accept use.txt T&C, and show Privacy Statement."""
    if has_data_file(_PACKAGE_FIRST_USE_FILE):
        _logger.debug("Not first use; not showing click-thru.")
        return
    _logger.debug("First use; showing click-thru.")

    txt = "You must accept the use terms before you can install or use the software."
    print(txt)
    print("If you do not accept the use terms, do not install or use the software.")
    print("\n\n")

    with open(get_terms_of_usage_file(), encoding="utf-8") as f_use_txt:
        for line in f_use_txt:
            print(line.rstrip())

    print("Press 'y' to accept the terms, or any other character to exit.")
    sys.stdin.flush()
    key_press = sys.stdin.read(1)
    if not key_press == "y" and not key_press == "Y":
        print("Exiting because terms were not accepted.")
        sys.exit(0)

    sys.stdin.flush()
    print("Please read our Privacy Statement, available at:")
    print(f"    {PRIVACY_STATEMENT_URI}")
    print("Press any key to continue.")
    sys.stdin.flush()
    sys.stdin.read(1)

    create_empty_data_file(_PACKAGE_FIRST_USE_FILE)


class JobInfo(NamedTuple):
    """Information about a job."""

    #: Current status of the job.
    status: JobStatus

    #: The result of the job, if it is completed.
    result: Optional[str]

    #: Input name of the job
    input: str

    #: The time the job was submitted.
    time_submitted: datetime

    #: The time the job was completed, if it is completed.
    time_completed: Optional[datetime]

    #: The time limit for the job.
    time_limit: int


class AzureWorkspaceException(Exception):
    """Exception type thrown by AzureWorkspace class."""

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.message = message


class ServiceConnection(ABC):
    """
    Abstract class to represent a connection to a service
    from which we can submit, query, and cancel jobs,
    and download job results.
    """

    @abstractmethod
    def upload(self, bio: io.BytesIO, blob_name: str):
        """
        Upload a blob to the service

        :param bio: The blob to upload
        :param blob_name: The name of the blob
        """

    @abstractmethod
    def download(self, bio: io.BytesIO, blob_name: str) -> int:
        """
        Download a blob from the service

        :param bio: The buffer to download the blob into
        :param blob_name: The name of the blob
        :returns: The bytes received
        """

    @abstractmethod
    def download_as_text(self, blob_name: str) -> str:
        """
        Download a blob from the service as text

        :param blob_name: The name of the blob
        :returns: The text received
        """

    @abstractmethod
    def list_blobs(self) -> List[str]:
        """
        List the blobs in the service

        :returns: A list of blob names
        """

    @abstractmethod
    def delete(self, blob_name: str):
        """
        Delete a blob from the service

        :param blob_name: The name of the blob
        """

    @abstractmethod
    def get_blob_creation_time(self, blob_name: str) -> datetime:
        """
        Get the creation time of a blob

        :param blob_name: The name of the blob
        :returns: The creation time
        """

    @property
    @abstractmethod
    def endpoint_name(self) -> str:
        """
        Get a unique name for the endpoint
        """

    @abstractmethod
    def test(self) -> bool:
        """
        Test the connection to the service
        """


class ContainerConnection(ServiceConnection):
    """
    A connection to an Azure blob storage container
    """

    __slots__ = (
        "__container",
        "__container_name",
    )

    def __init__(self, container):
        """
        Create a connection to an Azure blob storage container

        :param container: The name of the container
        """

        assert container is not None

        self.__container: ContainerClient = container
        self.__container_name: str = container.container_name

    def upload(self, bio: io.BytesIO, blob_name: str):
        blob = self.__container.get_blob_client(blob=blob_name)
        blob.upload_blob(bio)

    def download(self, bio: io.BytesIO, blob_name: str) -> int:
        blob = self.__container.get_blob_client(blob=blob_name)
        return blob.download_blob().readinto(bio)

    def download_as_text(self, blob_name: str) -> str:
        blob = self.__container.get_blob_client(blob=blob_name)
        return blob.download_blob().readall().decode("utf-8")

    def list_blobs(self) -> List[str]:
        return self.__container.list_blob_names()

    def delete(self, blob_name: str):
        blob = self.__container.get_blob_client(blob=blob_name)
        blob.delete_blob()

    def get_blob_creation_time(self, blob_name: str) -> str:
        blob = self.__container.get_blob_client(blob=blob_name)
        properties = blob.get_blob_properties()
        return properties.creation_time

    @property
    def endpoint_name(self) -> str:
        return self.__container_name

    def test(self) -> bool:
        return self.__container.exists()


class AzureServiceConnection(ServiceConnection):
    """
    A connection to the Azure service
    """

    __slots__ = (
        "__endpoint_storage",
        "__endpoint_service",
        "__credential",
        "__headers",
    )

    def __init__(self, endpoint_storage, endpoint_service, credential):
        self.__endpoint_storage = endpoint_storage
        self.__endpoint_service = endpoint_service
        self.__credential = credential

        access_token = self.__credential.get_token(f"{self.__endpoint_storage}.default")
        self.__headers = {"Authorization": f"Bearer {access_token.token}"}
        self.is_latest_pyaimopt_package()
        web_token_lifetime = self.token_valid_seconds()
        sec_per_day = float(24 * 60 * 60)
        valid_days = int(float(web_token_lifetime) / sec_per_day)

        if valid_days < 1:
            raise AzureWorkspaceException("AimCredentials expiring today.")

        if valid_days < 5:
            print(f"Warning: AimCredentials expire in {valid_days} days")

    def upload(self, bio: io.BytesIO, blob_name: str):
        dict_blob_count = self.web_count_blobs()
        if dict_blob_count["current"] > dict_blob_count["max"]:  # if gregos
            mess = "Upload would exceed max permitted blobs"
            raise AzureWorkspaceException(f"{mess} {dict_blob_count['max']}.")

        is_uploaded = bool(False)
        retry_limit = int(8)
        retry_count = int(0)
        while not is_uploaded and retry_count < retry_limit:
            payload = {"op_code": "upload_blob", "blobName": blob_name}
            files = {"file": (blob_name, bio, "application/octet-stream")}
            res = requests.post(
                self.__endpoint_service,
                headers=self.__headers,
                params=payload,
                files=files,
                timeout=HTTP_TIMEOUT_SECS,
                verify=_HTTP_SSL_CERTIFICATE_VERIFY,
            )
            res.raise_for_status()
            if "Return-Value" not in res.headers:
                raise AzureWorkspaceException("error: no data in downloaded.")

            results_code = res.headers["Return-Value"]
            if results_code == "1":  # Failure
                print(f"_WebUpload attempt {retry_count} failed: try again")
                delay = float(random.randint(1000, 2000)) / 1000.0
                time.sleep(delay)
                retry_count = retry_count + 1
            else:
                is_uploaded = True

        if not is_uploaded:
            raise AzureWorkspaceException(
                f"_WebUpload {retry_limit} successive failures: giving up."
            )

    def download(self, bio: io.BytesIO, blob_name: str) -> int:
        payload = {"op_code": "download_blob", "blobName": blob_name}
        res = requests.get(
            self.__endpoint_service,
            headers=self.__headers,
            params=payload,
            timeout=HTTP_TIMEOUT_SECS,
            verify=_HTTP_SSL_CERTIFICATE_VERIFY,
        )
        res.raise_for_status()
        res.encoding = "utf-8"
        result_string = res.text
        if result_string is None:  # Failure
            raise AzureWorkspaceException("error: no data in downloaded.")
        result_string = res.headers["Return-Value"]
        if result_string is None:  # Failure
            raise AzureWorkspaceException("error: no data in downloaded.")
        received = base64.b64decode(result_string)
        bio.seek(0)
        bytes_copied = bio.write(received)
        if bytes_copied != len(received):
            _logger.error(
                "error: only %d bytes copied of %d; aborting",
                bytes_copied,
                len(received),
            )
            raise AzureWorkspaceException(
                f"error: only {bytes_copied} bytes copied of {len(received)}"
            )

        return bytes_copied

    def download_as_text(self, blob_name: str) -> str:
        bio = io.BytesIO()
        self.download(bio, blob_name)
        return bio.getvalue().decode("utf-8")

    def list_blobs(self) -> List[str]:
        payload = {"op_code": "list_blobs"}
        res = requests.get(
            self.__endpoint_service,
            headers=self.__headers,
            params=payload,
            timeout=HTTP_TIMEOUT_SECS,
            verify=_HTTP_SSL_CERTIFICATE_VERIFY,
        )
        res.raise_for_status()
        res.encoding = "utf-8"
        if len(res.text) > 0:
            return res.text.split(",")
        return []

    def delete(self, blob_name: str):
        """
        Delete upload and download data from storage.

        :param blob_name: The name of the blob to delete.
        """
        payload = {"op_code": "delete_blob", "blobName": blob_name}
        res = requests.get(
            self.__endpoint_service,
            headers=self.__headers,
            params=payload,
            timeout=HTTP_TIMEOUT_SECS,
            verify=_HTTP_SSL_CERTIFICATE_VERIFY,
        )
        res.raise_for_status()

    def get_blob_creation_time(self, blob_name: str) -> datetime:
        payload = {"op_code": "get_blob_properties", "blobName": blob_name}
        res = requests.get(
            self.__endpoint_service,
            headers=self.__headers,
            params=payload,
            timeout=HTTP_TIMEOUT_SECS,
            verify=_HTTP_SSL_CERTIFICATE_VERIFY,
        )

        response = loads(res.text)
        if "created" not in response:
            _logger.warning("Blob creation time not found in response: %s", response)
            return datetime.utcnow()

        created = response["created"]
        return datetime.strptime(created, "%Y%m%dT%H%M%S%z")

    def web_count_blobs(self) -> dict[str, int]:
        """
        Count of blobs in user's demo tenant blob container
        """
        payload = {"op_code": "count_blobs"}
        res = requests.get(
            self.__endpoint_service,
            headers=self.__headers,
            params=payload,
            timeout=HTTP_TIMEOUT_SECS,
            verify=_HTTP_SSL_CERTIFICATE_VERIFY,
        )
        res.raise_for_status()
        res.encoding = "utf-8"
        dict_out = {"current": int(0), "max": int(0)}
        if "Return-Value" in res.headers and "," in res.headers["Return-Value"]:
            list_out = res.headers["Return-Value"].split(",")
            dict_out = {"current": int(list_out[0]), "max": int(list_out[1])}
        return dict_out

    def web_server_api_version(self) -> str:
        """
        Get web server's API version.
        """
        payload = {"op_code": "server_api_version"}
        res = requests.get(
            self.__endpoint_service,
            headers=self.__headers,
            params=payload,
            timeout=HTTP_TIMEOUT_SECS,
            verify=_HTTP_SSL_CERTIFICATE_VERIFY,
        )
        res.raise_for_status()
        res.encoding = "utf-8"
        if "Return-Value" in res.headers:
            return res.headers["Return-Value"]
        return "unknown"

    def token_valid_seconds(self) -> int:
        """
        Get the remaining timetime seconds of current access token

        :return: remaining time in seconds
        """
        payload = {"op_code": "token_valid_seconds"}
        res = requests.get(
            self.__endpoint_service,
            headers=self.__headers,
            params=payload,
            timeout=HTTP_TIMEOUT_SECS,
            verify=_HTTP_SSL_CERTIFICATE_VERIFY,
        )
        res.raise_for_status()
        if "Return-Value" in res.headers and not res.headers["Return-Value"] is None:
            return int(res.headers["Return-Value"])
        return int(0)

    def is_latest_pyaimopt_package(self) -> bool:
        """Check local pyaimopt version against latest advertised by service."""
        payload = {"op_code": "pyaimopt_version"}
        res = requests.get(
            self.__endpoint_service,
            headers=self.__headers,
            params=payload,
            timeout=HTTP_TIMEOUT_SECS,
            verify=_HTTP_SSL_CERTIFICATE_VERIFY,
        )
        res.raise_for_status()

        if "Return-Value" in res.headers:
            web_version = res.headers["Return-Value"]
        else:
            _logger.warning("pyaimopt_version not found in response: %s", res.text)
            web_version = None

        try:
            local_version = importlib.metadata.version("pyaimopt")
        except importlib.metadata.PackageNotFoundError:
            _logger.warning("pyaimopt package version not found")
            local_version = None

        if local_version is None or web_version is None:
            _logger.warning("Cannot determine whether package is updated")
            return False

        if Version(local_version) < Version(web_version):
            mess = f"Warning: pyaimopt package {local_version} deprecated"
            print(f"{mess} - please upgrade to {web_version}")
            return False

        return False

    @property
    def endpoint_name(self) -> str:
        return self.__endpoint_storage

    def test(self) -> bool:
        return True


class AzureWorkspace(Workspace):
    """
    Workspace to run jobs on the online AIM service
    """

    __slots__ = (
        "__jobs",
        "__lock",
        "__busy",
        "__jobs_read_lock",
        "__connection",
    )

    def __init__(self, connection: ServiceConnection):
        """
        Create a new workspace

        :param connection: Connection to the Azure service
        """
        super().__init__()

        assert connection is not None

        _click_thru()  # Accept T&C and show privacy statement on first use.
        self.__jobs: Dict[JobID, JobInfo] = {}
        self.__lock: Lock = Lock()
        self.__busy: bool = False
        self.__jobs_read_lock: Lock = Lock()
        self.__connection: ServiceConnection = connection

    def test_connection(self) -> bool:
        """Tests whether the connection to the service is working"""
        return self.__connection.test()

    async def submit_async(self, problem: ProblemDescription, time_limit: int) -> JobID:
        """
        Submit a job to the service using the async API

        :param problem: The problem to solve
        :param time_limit: The time limit in seconds
        :returns: The job id
        """
        pid = create_job_id()
        problem.configuration["guid"] = str(pid)

        bio = io.BytesIO()
        serialize(bio, problem)
        bio.seek(0)

        done = False
        blob_name = ""
        while not done:
            try:
                blob_name = _make_blob_name(pid, time_limit)
                _logger.info("Submitting job %s with name %s", str(pid), str(blob_name))
                self.__connection.upload(bio, blob_name)
                done = True
            except ResourceExistsError:
                _logger.warning("Blob name %s already exists; trying again", blob_name)
                await sleep(1.0)

        return pid

    async def _update_status(self):
        should_update = True
        while self.__busy:
            should_update = False
            await sleep(1.0)

        if not should_update:
            # Another thread updated the status
            return

        async with self.__lock:
            if self.__busy:
                # Another thread updated the status before we got the lock
                return

            _logger.info(
                "Updating job status for container %s", self.__connection.endpoint_name
            )

            self.__busy = True
            blobs = self.__connection.list_blobs()

            jobs: Dict[JobID, JobInfo] = {}
            for blob in blobs:
                job_id = _job_id_from_blob_name(blob)

                if job_id in self.__jobs and self.__jobs[job_id].status in (
                    JobStatus.COMPLETED,
                    JobStatus.FAILED,
                    JobStatus.CANCELED,
                ):
                    # Job has already been completed
                    # no need to check properties again
                    jobs[job_id] = self.__jobs[job_id]
                    continue

                info = await self._update_info_for_job(blob, job_id, jobs)

                jobs[job_id] = info

            async with self.__jobs_read_lock:
                self.__jobs = jobs

        self.__busy = False

    async def _update_info_for_job(self, blob, job_id, jobs):
        if job_id not in jobs:
            info = JobInfo(
                status=JobStatus.SUBMITTED,
                result=None,
                input=blob,
                time_submitted=_submitted_time_from_blob_name(blob),
                time_completed=None,
                time_limit=_time_limit_from_blob_name(blob),
            )
        else:
            info = jobs[job_id]

        # pylint disable=protected_access,W0212

        if not _is_submission(blob):
            creation_time = self.__connection.get_blob_creation_time(blob)
            info = info._replace(time_completed=creation_time)

            if _is_completed_successfully(blob):
                info = info._replace(status=JobStatus.COMPLETED, result=blob)
            elif _is_failed(blob):
                info = info._replace(status=JobStatus.FAILED, result=blob)
            elif _is_cancelled(blob):
                info = info._replace(status=JobStatus.CANCELED)
            else:
                info = info._replace(status=JobStatus.UNKNOWN)
        else:
            info = info._replace(input=blob)

        # pylint enable=protected_access,W0212

        return info

    async def get_status_async(self, job_id: JobID) -> JobStatus:
        _logger.debug(
            "Inside get_status_async for job %s in container %s in AIM service",
            job_id,
            self.__connection.endpoint_name,
        )
        await self._update_status()
        async with self.__jobs_read_lock:
            info = self.__jobs.get(job_id, None)
            if info is None:
                return JobStatus.UNKNOWN
            return info.status

    async def get_result_async(self, job_id: JobID) -> JobResult:
        _logger.debug(
            "Inside get_result_async for job %s in container %s in AIM service",
            job_id,
            self.__connection.endpoint_name,
        )
        await self._update_status()
        async with self.__jobs_read_lock:
            if job_id not in self.__jobs:
                return Failed(f"Job {job_id} not found")

            if self.__jobs[job_id].status in (JobStatus.SUBMITTED, JobStatus.RUNNING):
                return Pending()

            _logger.debug("Job %s is completed; downloading result", job_id)

            blob_name = self.__jobs[job_id].result

            if self.__jobs[job_id].status == JobStatus.COMPLETED:
                bio = io.BytesIO()
                bytes_read = self.__connection.download(bio, blob_name)

                _logger.debug(
                    "Read %d bytes from blob %s for job %s",
                    bytes_read,
                    blob_name,
                    job_id,
                )
                bio.seek(0)
                solution = read_solution_from_stream(bio)

                result = Ok(solution)
            else:
                message = self.__connection.download_as_text(blob_name)
                result = Failed(message)

            # Remove blobs from demo tenant storage once result downloaded.
        await self.delete_job_async(job_id)

        return result

    async def get_completed_jobs_async(self) -> List[JobID]:
        _logger.debug(
            "Inside get_completed_jobs_async for container %s in AIM service",
            self.__connection.endpoint_name,
        )
        await self._update_status()
        async with self.__jobs_read_lock:
            return [
                job_id
                for job_id, info in self.__jobs.items()
                if info.status == JobStatus.COMPLETED
            ]

    async def get_all_jobs_async(self) -> List[Tuple[JobID, JobStatus]]:
        _logger.debug(
            "Inside get_all_jobs_async for container %s in AIM service",
            self.__connection.endpoint_name,
        )
        await self._update_status()
        async with self.__jobs_read_lock:
            return [(job_id, info.status) for job_id, info in self.__jobs.items()]

    async def cancel_job_async(self, _job_id: JobID) -> bool:
        _logger.debug(
            "Inside cancel_job_async for job %s in container %s in AIM service",
            _job_id,
            self.__connection.endpoint_name,
        )

        raise NotImplementedError("Canceling jobs is not supported in the AIM service")

    async def delete_job_async(self, job_id: JobID) -> bool:
        _logger.debug(
            "Inside delete_job_async for job %s in container %s in AIM service",
            job_id,
            self.__connection.endpoint_name,
        )
        await self._update_status()

        async with self.__jobs_read_lock:
            if job_id not in self.__jobs:
                _logger.warning("Job %s not found; ignoring", job_id)
                return False

            info = self.__jobs[job_id]

            if info.status == JobStatus.RUNNING:
                _logger.error("Job %s is running; cannot delete; will continue", job_id)
                return False

            blob_name = info.input
            self.__connection.delete(blob_name)

            if info.result is not None:
                blob_name = info.result
                if not blob_name[:1] == "E":  # retain Error files for debugging
                    self.__connection.delete(blob_name)

        await self._update_status()
        return True

    async def print_detailed_async(self) -> None:
        await self._update_status()

        async with self.__jobs_read_lock:
            for job_id, info in self.__jobs.items():
                print(f"Job {job_id} (time limit: {info.time_limit}): {info.status}")
                print(f"\tInput: {info.input}")

                if info.status in (
                    JobStatus.COMPLETED,
                    JobStatus.FAILED,
                    JobStatus.CANCELED,
                ):
                    print(f"\t{info.time_submitted} - {info.time_completed})")
                    print(f"\tResult: {info.result}")
                else:
                    print(f"\t{info.time_submitted} - (not completed)")


def _container_name_from_username(username: str) -> str:
    """
    Create the container name from the username
    """
    username = username.replace(".", "")
    username = username.replace("-", "")
    username = username.replace("_", "")
    username = username.replace("&", "")
    username = username.replace("@", "-")

    if len(username) > __SIZEOF_MAX_BLOB_CONTAINER_NAME__:
        username = username[0:__SIZEOF_MAX_BLOB_CONTAINER_NAME__]

    return username


def __ask_for_username():
    """
    Ask the user for their username

    :return: The username
    """

    _logger.debug("Invoking interactive authentication")
    user_credential = InteractiveBrowserCredential(tenant_id=GREGOSLIVECO_ONMICROSOFT)
    auth = user_credential.authenticate()
    return user_credential, auth.username


def create_azure_workspace(
    username: str = None, container: str = None
) -> AzureWorkspace:
    """
    Create a workspace to run jobs on the online AIM service

    :param username: The username to use to get access to the service
    :param container: The storage container
    :return: The Azure workspace which can be used to submit jobs and check their status
    """

    # Load environment variables from .env file
    if "AIM_SETTINGS_ENV" in os.environ:
        env_file = os.environ["AIM_SETTINGS_ENV"]
        if not os.path.exists(env_file):
            _logger.error(
                "Environment file %s does not exist; will try alternative authentication methods",
                env_file,
            )
        _logger.info("Loading environment variables from %s", env_file)
        config = {**dotenv_values(env_file), **os.environ}
    else:
        config = os.environ

    storage_account = config.get("AIM_STORAGE_ACCOUNT", __AZURE_STORAGE_ACCOUNT__)

    if container is None:
        container = config.get("AIM_CONTAINER", None)

    service_endpoint = config.get("AIM_SERVICE_ENDPOINT", __AZURE_SERVICE_ACCOUNT__)

    aim_creds = AimCredentials(username=username, tenant_id=GREGOSLIVECO_ONMICROSOFT)
    _logger.info("Creating Azure workspace for account %s', aim_creds.Username")

    connection = AzureServiceConnection(
        storage_account, service_endpoint, credential=aim_creds.Credentials
    )
    return AzureWorkspace(connection)
