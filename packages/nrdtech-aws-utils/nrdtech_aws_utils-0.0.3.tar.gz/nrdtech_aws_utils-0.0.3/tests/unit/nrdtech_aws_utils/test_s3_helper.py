from unittest import mock

import pytest
from unittest.mock import Mock, patch, mock_open

from nrdtech_aws_utils.s3_helper import S3Helper


@pytest.fixture
def s3_client_mock():
    return Mock()


@pytest.fixture
def s3_helper(s3_client_mock):
    return S3Helper(s3_client_mock)


def test_upload_file_success(s3_helper, s3_client_mock):
    # Setup
    filename = "test.txt"
    bucket_name = "mybucket"
    key = "test/test.txt"

    # Act
    s3_helper.upload_file(filename, bucket_name, key)

    # Assert
    s3_client_mock.upload_file.assert_called_once_with(
        filename, bucket_name, key, ExtraArgs={"ContentType": "text/plain"}
    )


def test_upload_data_success(s3_helper, s3_client_mock):
    # Setup
    data = "Hello, World!"
    bucket_name = "mybucket"
    key = "test/data.txt"

    # Act
    s3_helper.upload_data(data, bucket_name, key)

    # Assert
    # You should check that a file was created, data written to it, and uploaded
    # Asserts will depend on how you mock tempfile.NamedTemporaryFile


def test_download_file_success(s3_helper, s3_client_mock):
    # Setup
    bucket_name = "mybucket"
    key = "test/test.txt"
    expected_content = "File content"

    # Act
    with patch("builtins.open", mock_open(read_data=expected_content)) as mock_file:
        content = s3_helper.download_file(bucket_name, key)

    # Assert
    s3_client_mock.download_file.assert_called_once_with(bucket_name, key, mock.ANY)
    assert content == expected_content


def test_download_file_from_s3_path_success(s3_helper, s3_client_mock):
    # Setup
    s3_path = "s3://mybucket/test/test.txt"
    expected_content = "File content"

    # Act
    with patch("builtins.open", mock_open(read_data=expected_content)) as mock_file:
        content = s3_helper.download_file_from_s3_path(s3_path)

    # Assert
    assert content == expected_content


def test_guess_mime_type_from_filename():
    # Test with known file extensions
    assert S3Helper._guess_mime_type_from_filename("file.txt") == "text/plain"
    assert S3Helper._guess_mime_type_from_filename("image.jpg") == "image/jpeg"
    assert S3Helper._guess_mime_type_from_filename("document.pdf") == "application/pdf"
    assert S3Helper._guess_mime_type_from_filename("archive.zip") == "application/zip"
