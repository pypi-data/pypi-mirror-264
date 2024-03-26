import os
from unittest.mock import MagicMock, patch

import pytest

from nrdtech_aws_utils.dynamodb_table import (
    deserialize_dynamodb_image,
    DynamodbTable,
)


# Mocking AWS DynamoDB
@pytest.fixture
def mock_dynamodb_resource():
    with patch("boto3.resource") as mock_resource:
        mock_table = MagicMock()
        mock_resource.Table.return_value = mock_table
        yield mock_resource, mock_table


@pytest.fixture
def dynamodb_table(mock_dynamodb_resource):
    mock_resource, _ = mock_dynamodb_resource
    os.environ["ENVIRONMENT"] = "test"
    return DynamodbTable(mock_resource, "test_table")


@pytest.fixture
def dynamodb_table_env_mod(mock_dynamodb_resource):
    mock_resource, _ = mock_dynamodb_resource
    os.environ["ENVIRONMENT"] = "test"
    return DynamodbTable(
        mock_resource, "test_table", automatically_append_env_to_table_name=True
    )


class TestDynamodbTable:
    def test_init(self, dynamodb_table):
        assert dynamodb_table._primary_key == "id"
        assert dynamodb_table._secondary_key == "sub_id"

    def test_get_full_table_name(self, dynamodb_table, dynamodb_table_env_mod):
        assert dynamodb_table._get_full_table_name("my_table") == "my_table"
        assert (
            dynamodb_table_env_mod._get_full_table_name("my_table") == "my_table-test"
        )

    def test_put_item(self, dynamodb_table, mock_dynamodb_resource):
        _, mock_table = mock_dynamodb_resource
        item = {"id": "123", "data": "test"}
        dynamodb_table.put_item(item)
        mock_table.put_item.assert_called_with(Item=item)

    def test_put_items(self, dynamodb_table, mock_dynamodb_resource):
        _, mock_table = mock_dynamodb_resource
        items = [{"id": str(i), "data": "test"} for i in range(30)]
        dynamodb_table.put_items(items)
        assert mock_table.batch_writer.call_count == 2  # Assuming 25 items per batch

    def test_get_item_with_id_and_sub_id(self, dynamodb_table, mock_dynamodb_resource):
        _, mock_table = mock_dynamodb_resource
        mock_table.query.return_value = {"Items": [{"id": "123", "sub_id": "456"}]}
        result = dynamodb_table.get_item_with_id_and_sub_id("123", "456")
        assert result == {"id": "123", "sub_id": "456"}

    def test_get_items_with_id_and_sub_id_prefix(
        self, dynamodb_table, mock_dynamodb_resource
    ):
        _, mock_table = mock_dynamodb_resource
        mock_table.query.return_value = {"Items": [{"id": "123", "sub_id": "45"}]}
        result = dynamodb_table.get_items_with_id_and_sub_id_prefix("123", "45")
        assert result == [{"id": "123", "sub_id": "45"}]

    def test_get_items_with_id(self, dynamodb_table, mock_dynamodb_resource):
        _, mock_table = mock_dynamodb_resource
        mock_table.query.return_value = {"Items": [{"id": "123"}]}
        result = dynamodb_table.get_items_with_id("123")
        assert result == [{"id": "123"}]


def test_deserialize_dynamodb_image():
    image = {"key": {"S": "value"}}
    assert deserialize_dynamodb_image(image) == {"key": "value"}

    assert deserialize_dynamodb_image(None) is None
