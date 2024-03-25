import os
from datetime import datetime, timezone
from typing import Optional
from jfrog_ml._artifactory_api import ArtifactoryApi
from jfrog_ml._log_config import logger
from jfrog_ml.model_info import ModelInfo, Checksums
from jfrog_ml.storage import Storage
from jfrog_ml._utils import BearerAuth, join_url, extract_uri_and_repo_name


class Artifactory(Storage):
    """
    Repository implementation to download or store model artifacts, and metrics in Artifactory repository.
    """

    def __init__(self):
        self.uri = None
        self.uri = extract_uri_and_repo_name(os.getenv("JFML_URL"))
        self.auth = BearerAuth(os.getenv("JFML_TOKEN"))
        self.artifactory_api = ArtifactoryApi(self.uri, self.auth)

    def upload_model_version(
            self,
            repository: str,
            model_name: str,
            source_path: str,
            namespace: Optional[str] = None,
            version: Optional[str] = None,
            tags: Optional[dict[str, str]] = None):
        namespace_and_name = self.__union_model_name_with_namespace(namespace, model_name)
        location_to_upload, transaction_id = self.artifactory_api.start_transaction(repository=repository,
                                                                                    model_name=namespace_and_name,
                                                                                    version=version)
        transaction_date = self.__milliseconds_to_iso_instant(transaction_id)
        model_info = ModelInfo(model_name=namespace_and_name, created_date=transaction_date, artifacts=[])
        self.__upload_by_source(source_path, repository, location_to_upload, model_info)

        if version is None:
            version = location_to_upload.replace(f'models/{namespace_and_name}/tmp/', "").split('/')[0]

        self.artifactory_api.end_transaction(repository=repository, model_name=namespace_and_name,
                                             model_info=model_info, transaction_id=transaction_id, version=version,
                                             tags=tags)
        return version

    def download_model_version(
            self,
            repository: str,
            model_name: str,
            version: str,
            target_path: str,
            namespace: Optional[str] = None):
        model_info = self.artifactory_api.get_model_info(repository, namespace, model_name, version)
        search_under_repo = f"/{repository}/"

        for artifact in model_info["artifacts"]:
            download_url = artifact["download_url"]
            artifact_path = artifact["artifact_path"]
            position_under_repo = download_url.find(search_under_repo)
            if position_under_repo != -1:
                repo_rel_path = download_url[position_under_repo + len(search_under_repo):]
                if not os.path.exists(target_path + "/" + artifact_path):
                    self.__create_dirs_if_needed(target_path, artifact_path)
                    self.artifactory_api.download_file(repository, repo_rel_path, target_path + "/" + artifact_path)

    def associate_artifacts_to_model_version(
            self,
            repository: str,
            model_name: str,
            version: str,
            source_path: str,
            namespace: Optional[str] = None):
        namespace_and_name = self.__union_model_name_with_namespace(namespace, model_name)
        mode_info = self.artifactory_api.get_model_info(repository, namespace, model_name, version)
        if mode_info is not None:
            location_to_upload = f"models/{namespace_and_name}/{version}/artifacts/"
            self.__upload_by_source(source_path, repository, location_to_upload, None)
        else:
            logger.error(
                f'Could not find model info for {namespace_and_name} version {version} in repository {repository}')


    def get_model_info(self, repository: str, namespace: Optional[str], model_name: str, version: Optional[str]):
        return self.artifactory_api.get_model_info(repository, namespace, model_name, version)

    def __upload_by_source(self, source_path: str, repository: str, location_to_upload: str,
                           model_info: Optional[ModelInfo]):
        if os.path.isfile(source_path):
            rel_path = os.path.basename(source_path)
            self.__upload_single_file(repository, source_path, rel_path, location_to_upload, model_info)
        else:
            for dir_path, dir_names, file_names in os.walk(source_path):
                for filename in file_names:
                    full_path = os.path.join(dir_path, filename)
                    rel_path = os.path.relpath(full_path, source_path)
                    self.__upload_single_file(repository, full_path, rel_path, location_to_upload, model_info)

    def __upload_single_file(self, repository, full_path, rel_path, location_to_upload,
                             model_info: Optional[ModelInfo]):
        checksums = Checksums.calc_checksums(full_path)
        if model_info is not None:
            model_info.add_file(full_path, checksums, rel_path)
        url = join_url(self.uri, repository, location_to_upload, rel_path)
        is_checksum_deploy_success = self.artifactory_api.checksum_deployment(url=url, checksum=checksums,
                                                                              stream=True)
        if is_checksum_deploy_success is False:
            self.artifactory_api.upload_file(url=url, file_path=full_path)
        else:
            logger.info(f'Uploaded by checksum deploy: {full_path}')

    @staticmethod
    def __union_model_name_with_namespace(namespace: str, model_name: str):
        if namespace is None:
            return model_name
        else:
            return namespace + "/" + model_name

    @staticmethod
    def __create_dirs_if_needed(base_dir, file_uri):
        full_path = os.path.join(base_dir, file_uri.strip("/"))
        dest_path = os.path.dirname(full_path)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        return dest_path

    @staticmethod
    def __milliseconds_to_iso_instant(milliseconds):
        instant = datetime.utcfromtimestamp(int(milliseconds) / 1000.0).replace(tzinfo=timezone.utc)
        x = instant.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]
        return x
