import json
import time
from typing import List
import requests
from pipebio.models.entity_types import EntityTypes
from pipebio.models.job_status import JobStatus
from pipebio.models.job_type import JobType
from pipebio.models.output_link import OutputLink
from pipebio.models.upload_detail import UploadDetail
from pipebio.util import Util


class Jobs:
    session: requests.sessions
    status: str

    def __init__(self, url, session: requests.sessions, job_id=None):
        self.base_url = url
        self.url = url + '/api/v2/jobs'
        self.session = Util.mount_standard_session(session)
        self.job_id = job_id
        self.status = JobStatus.RUNNING.value

    def create(self,
               owner_id: str,
               shareable_id: str,
               job_type: JobType,
               name: str,
               input_entity_ids: List[int],
               params=None) -> str:
        """

        :param owner_id: - organization id owning this job
        :param shareable_id: - project in which the docuemnts are
        :param job_type:
        :param name: - helpful user facing name
        :param input_entity_ids: - document ids
        :param params: - specific to this job_type
        :return:
        """

        if params is None:
            params = {}

        response = self.session.post(self.url,
                                     headers={
                                         'content-type': 'application/json'
                                     },
                                     data=json.dumps({
                                         'name': name,
                                         'params': params,
                                         'shareableId': shareable_id,
                                         'ownerId': owner_id,
                                         'inputEntities': input_entity_ids,
                                         'type': job_type.value
                                     }))

        Util.raise_detailed_error(response)

        data = response.json()
        job_id = data['id']
        self.job_id = job_id
        return job_id

    def list(self):
        response = self.session.get(self.url + '?filter=',
                                    headers={
                                        'content-type': 'application/json'
                                    })
        Util.raise_detailed_error(response)
        return response

    def get(self, job_id=None):
        if job_id is None:
            job_id = self.job_id
        url = '{}/{}'.format(self.url, job_id)
        response = self.session.get(url, headers={'content-type': 'application/json'})
        Util.raise_detailed_error(response)
        return response.json()

    def start_import_job(self):
        """
        Enable the cloud-function to trigger a job run via the kubernetes job processing engine.
        :return:
        """
        response = self.session.patch(
            '{}/{}/import'.format(self.url, self.job_id),
            headers={'content-type': 'application/json'}
        )
        Util.raise_detailed_error(response)
        return response

    def poll_job(self, job_id=None, timeout_seconds=None):

        if job_id is None:
            job_id = self.job_id

        done = False
        job_status = None
        job = None

        # 5mins
        timeout = time.time() + (timeout_seconds if timeout_seconds is not None else 60 * 5)

        while not done:
            time.sleep(5)
            print('Polling job: {}'.format(job_id))
            job = self.get(job_id)
            job_status = job['status']
            print('     status: {}'.format(job_status))
            done = job_status in [JobStatus.RUNNING.value, JobStatus.FAILED.value]

            if time.time() > timeout:
                raise Exception('Timeout waiting for job {} to finish.'.format(job_id))

        print('Job {} is: {}'.format(self.job_id, job_status))
        return job

    def create_signed_upload(self,
                             file_name: str,
                             parent_id: int,
                             project_id: str,
                             organization_id: str,
                             details: List[UploadDetail],
                             file_name_id: str) -> dict:
        data = {
            'name': file_name,
            'type': EntityTypes.SEQUENCE_DOCUMENT.value,
            'targetFolderId': parent_id,
            'shareableId': project_id,
            'ownerId': organization_id,
        }

        data['details'] = []

        if details is not None:
            # Details should be an
            for detail in details:
                data['details'].append(detail.to_json())

        if file_name_id is not None:
            data['details'].append({
                'name': 'fileNameId',
                'type': 'fileNameId',
                'value': file_name_id
            })

        response = self.session.post('{}/api/v2/signed-url'.format(self.base_url), json=data)

        Util.raise_detailed_error(response)

        return response.json()

    def upload_data_to_signed_url(self, absolute_file_location: str, signed_url: str, signed_headers):

        # 1. Start the signed-upload.
        # NOTE: Url and headers cannot be modified or the upload will fail.
        create_upload_response = self.session.post(signed_url, headers=signed_headers)
        Util.raise_detailed_error(create_upload_response)
        response_headers = create_upload_response.headers
        location = response_headers['Location']

        # 2. Upload bytes.
        with open(absolute_file_location, 'rb') as file:
            upload_response = self.session.put(location, data=file)
            Util.raise_detailed_error(upload_response)
            print('Upload response: ', upload_response.status_code)
            print('Upload response:', upload_response.text)

    def update(self,
               status: JobStatus,
               progress=None,
               messages: List[str] = None,
               output_entity_ids: List[int] = None,
               output_links: List[OutputLink] = None):
        """
        Update a jobs status.
        :param status:
        :param progress:
        :param messages:
        :param output_entity_ids:
        :param output_links:
        :return:
        """

        body = {
            'status': status.value,
        }

        if progress is not None:
            # Clamp the progress between 0 and 100.
            body['progress'] = max(0, min(100, progress))

        if messages is not None:
            body['messages'] = messages

        if output_entity_ids is not None:
            body['outputEntities'] = output_entity_ids

        if output_links is not None:
            body['outputLinks'] = list(map(lambda link: link.to_json(), output_links))

        response = self.session.patch('{}/{}'.format(self.url, self.job_id),
                                      headers={'content-type': 'application/json'},
                                      data=json.dumps(body))
        Util.raise_detailed_error(response)
        return response

    def set_complete(self,
                     messages: List[str] = None,
                     output_entity_ids: List[int] = None,
                     output_links: List[OutputLink] = None):
        """
        Complete a job.
        :param messages:
        :param output_entity_ids:
        :param output_links:
        :return:
        """
        return self.update(JobStatus.COMPLETE,
                           100,
                           messages=messages,
                           output_entity_ids=output_entity_ids,
                           output_links=output_links)
