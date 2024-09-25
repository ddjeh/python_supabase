import os

from supabase_service.config import SupabaseClient
from supabase_service.types import GenericResponse


class SupabaseStorage(SupabaseClient):

    def __init__(self):
        super().__init__()
        self.__client_storage = self._get_client

    def list_buckets(self) -> GenericResponse:
        """
        :return: list[SyncBucket]
        """
        try:
            buckets = self.__client_storage.list_buckets()
            return GenericResponse(status=200, message="Buckets retrieved successfully", data=buckets)
        except Exception as e:
            return GenericResponse(status=500, message=str(e))

    def create_bucket(self, bucket_id: str, bucket_name: str, public: bool = False) -> GenericResponse:
        """
        :param bucket_id: str
        :param bucket_name: str
        :return: dict[str,str] | str
        """
        if not bucket_id or not bucket_id.strip():
            return GenericResponse(status=400, message="Bucket ID is required")

        if not bucket_name or not bucket_name.strip():
            return GenericResponse(status=400, message="Bucket name is required")

        buckets = self.list_buckets()

        if buckets.status not in [200]:
            return GenericResponse(status=400, message="Buckets not found")

        if bucket_id in [bucket.id for bucket in buckets.data]:
            return GenericResponse(status=400, message="Bucket already exists")

        try:
            bucket_created = self.__client_storage.create_bucket(id=bucket_id, name=bucket_name,
                                                                 options={"public": public})
        except Exception as e:
            return str(e)

        return GenericResponse(status=201, message="Bucket created successfully", data=bucket_created)

    def delete_bucket(self, bucket_id: str) -> GenericResponse:
        """
        :param bucket_id: str
        :return: dict[str, str] | None
        """
        if not bucket_id or not bucket_id.strip():
            return GenericResponse(status=400, message="Bucket ID is required")

        try:
            bucket = self.get_bucket(bucket_id=bucket_id)

            if bucket.status not in [200]:
                return GenericResponse(status=400, message="Bucket not found")

        except Exception as e:
            return GenericResponse(status=400, message="Bucket not found")

        bucket_removed = self.__client_storage.delete_bucket(id=bucket_id)

        return GenericResponse(status=200, message="Bucket removed!", data=bucket_removed)

    def get_bucket(self, bucket_id: str) -> GenericResponse:
        """
        :param bucket_id: str
        :return: SyncBucket | None
        """
        if not bucket_id or not bucket_id.strip():
            return None

        try:
            bucket = self.__client_storage.get_bucket(id=bucket_id)

            return GenericResponse(status=200, message="Bucket retrieved successfully", data=bucket)
        except Exception as e:
            return GenericResponse(status=400, message=str(e))

    def list_files(self, bucket_id: str) -> GenericResponse:
        """
        :param bucket_id: str
        :return: list
        """
        if not bucket_id or not bucket_id.strip():
            return GenericResponse(status=400, message="Bucket ID is required")

        bucket = self.get_bucket(bucket_id=bucket_id)

        if bucket.status not in [200]:
            return GenericResponse(status=400, message="Bucket not found")

        return GenericResponse(status=200, message="Files retrieved successfully", data=bucket.data.list())

    def upload_file(self, bucket_id: str, bucket_path: str, local_file_path: str, file_name: str) -> GenericResponse:
        """
        :param bucket_id: str
        :param bucket_path: str | None
        :param local_file_path: str
        :param file_name: str
        :return: Response | str
        """
        global path

        if not bucket_id or not bucket_id.strip():
            return GenericResponse(status=400, message="Bucket ID is required")

        if not local_file_path or not local_file_path.strip():
            return GenericResponse(status=400, message="Local file path is required")

        if not file_name or not file_name.strip():
            return GenericResponse(status=400, message="File name is required")

        if os.path.exists(local_file_path) and not os.path.isfile(local_file_path):
            return GenericResponse(status=400, message="Local file path is not a file")

        if bucket_path > 0 and not bucket_path.endswith("/"):
            bucket_path += "/"

        if bucket_path:
            path = bucket_path + file_name
        else:
            path = file_name

        bucket = self.get_bucket(bucket_id=bucket_id)

        if bucket.status not in [200]:
            return GenericResponse(status=400, message="Bucket not found")

        try:
            file_uploaded = bucket.upload(path=path, file=local_file_path, file_options=None)

            return GenericResponse(status=201, message="File uploaded successfully", data=file_uploaded)
        except Exception as e:
            return GenericResponse(status=400, message=str(e))

    def download_file(self, bucket_id: str, bucket_path: str, file_name: str) -> GenericResponse:
        """
        :param bucket_id: str
        :param bucket_path: str | None
        :param file_name: str
        :return: Response | str
        """
        global path

        if not bucket_id or not bucket_id.strip():
            return GenericResponse(status=400, message="Bucket ID is required")

        if not file_name or not file_name.strip():
            return GenericResponse(status=400, message="File name is required")

        if bucket_path and not bucket_path.endswith("/"):
            bucket_path += "/"

        if bucket_path:
            path = bucket_path + file_name
        else:
            path = file_name

        bucket = self.get_bucket(bucket_id=bucket_id)

        if bucket.status not in [200]:
            return GenericResponse(status=400, message="Bucket not found")

        try:
            file_downloader = bucket.download(path=path)

            return GenericResponse(status=200, message="File downloaded successfully", data=file_downloader)
        except Exception as e:
            return GenericResponse(status=400, message=str(e))

    def update_file(self, bucket_id: str, bucket_path: str, local_file_path: str, file_name: str) -> GenericResponse:
        """
        :param bucket_id: str
        :param bucket_path: str | None
        :param local_file_path: str
        :param file_name: str
        :return: Response | str
        """
        global path

        if not bucket_id or not bucket_id.strip():
            return GenericResponse(status=400, message="Bucket ID is required")

        if not local_file_path or not local_file_path.strip():
            return GenericResponse(status=400, message="Local file path is required")

        if not file_name or not file_name.strip():
            return GenericResponse(status=400, message="File name is required")

        if os.path.exists(local_file_path) and not os.path.isfile(local_file_path):
            return GenericResponse(status=400, message="Local file path is not a file")

        if bucket_path and not bucket_path.endswith("/"):
            bucket_path += "/"

        if bucket_path:
            path = bucket_path + file_name
        else:
            path = file_name

        bucket = self.get_bucket(bucket_id=bucket_id)

        if bucket.status not in [200]:
            return None

        try:
            file_updated = bucket.update(path=path, file=local_file_path, file_options=None)

            return GenericResponse(status=200, message="File updated successfully", data=file_updated)
        except Exception as e:
            return GenericResponse(status=400, message=str(e))

    def copy_file(self, bucket_id: str, from_path: str, to_path: str) -> GenericResponse:
        """
        :param bucket_id: str
        :param from_path: str
        :param to_path: str
        :return: dict[str, str] | str
        """
        global path

        if not bucket_id or not bucket_id.strip():
            return GenericResponse(status=400, message="Bucket ID is required")

        if not from_path or not from_path.strip():
            return GenericResponse(status=400, message="From path is required")

        if not to_path or not to_path.strip():
            return GenericResponse(status=400, message="To path is required")

        bucket = self.get_bucket(bucket_id=bucket_id)

        if bucket.status not in [200]:
            return GenericResponse(status=400, message="Bucket not found")

        try:
            file_copied = bucket.copy(from_path=from_path, to_path=to_path)

            return GenericResponse(status=200, message="File copied successfully", data=file_copied)
        except Exception as e:
            return GenericResponse(status=400, message=str(e))

    def move_file(self, bucket_id: str, from_path: str, to_path: str) -> GenericResponse:
        """
        :param bucket_id: str
        :param from_path: str
        :param to_path: str
        :return: dict[str, str] | str
        """
        global path

        if not bucket_id or not bucket_id.strip():
            return GenericResponse(status=400, message="Bucket ID is required")

        if not from_path or not from_path.strip():
            return GenericResponse(status=400, message="From path is required")

        if not to_path or not to_path.strip():
            return GenericResponse(status=400, message="To path is required")

        bucket = self.get_bucket(bucket_id=bucket_id)

        if bucket.status not in [200]:
            return GenericResponse(status=400, message="Bucket not found")

        try:
            file_moved = bucket.move(from_path=from_path, to_path=to_path)

            return GenericResponse(status=200, message="File moved successfully", data=file_moved)
        except Exception as e:
            return GenericResponse(status=400, message=str(e))
