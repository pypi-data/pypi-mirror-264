import time
from functools import partial

import requests

from ploomber_cloud import client

# API_ROOT = "http://localhost:80"
API_ROOT = "https://serverless.ploomber.io"


class TimeoutError(Exception):
    pass


class JobError(Exception):
    pass


def call_with_timeout(func, timeout, delay=0.5):
    start_time = time.time()

    while True:
        try:
            return func()
        except Exception as e:

            if time.time() - start_time > timeout:
                raise TimeoutError from e

            time.sleep(delay)


class PloomberFunctionsClient(client.PloomberBaseClient):

    def pdf_to_text(self, path_to_pdf):
        with open(path_to_pdf, "rb") as file:
            response = requests.post(
                f"{API_ROOT}/functions/pdf-to-text",
                headers=self._get_headers(),
                files={"file": ("file.pdf", file, "application/pdf")},
            )

        response.raise_for_status()

        return response

    def image_to_text(self, path_to_image, question):
        question = requests.utils.quote(question)

        with open(path_to_image, "rb") as file:
            response = requests.post(
                f"{API_ROOT}/functions/image-to-text?question={question}",
                headers=self._get_headers(),
                files={"file": ("image", file, "image/*")},
            )

        response.raise_for_status()

        return response

    def get_result(self, job_id):
        response = requests.get(
            f"{API_ROOT}/status/{job_id}", headers=self._get_headers()
        )
        response.raise_for_status()

        response_ = response.json()

        if response_["status"] == "SUBMITTED":
            raise JobError("Job is still running")
        elif response_["status"] == "FAILED":
            raise JobError("Job failed")
        elif response_["status"] == "SUCCEEDED":
            response = requests.get(
                f"{API_ROOT}/result/{job_id}", headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        else:
            raise JobError(f"Unexpected status: {response_['status']}")


client = PloomberFunctionsClient()


def pdf_to_text(path_to_pdf, timeout=20, block=True):
    """Convert a PDF to text"""
    response = client.pdf_to_text(path_to_pdf)

    if block:
        get_result = partial(client.get_result, response.json()["job_id"])
        return call_with_timeout(get_result, timeout)["output"]
    else:
        return response.json()["job_id"]


def image_to_text(path_to_image, question, timeout=20, block=True):
    """Ask a question to an image"""
    response = client.image_to_text(path_to_image, question)

    if block:
        get_result = partial(client.get_result, response.json()["job_id"])
        return call_with_timeout(get_result, timeout)["output"]
    else:
        return response.json()["job_id"]


def get_result(job_id):
    """Get the result of a job"""
    return client.get_result(job_id)["output"]
