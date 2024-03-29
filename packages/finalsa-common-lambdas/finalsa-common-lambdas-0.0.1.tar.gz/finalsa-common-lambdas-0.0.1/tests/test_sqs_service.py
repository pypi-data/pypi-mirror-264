from finalsa.common.lambdas.sqs import SqsHandler, SqsEvent
from logging import getLogger
from json import dumps
from finalsa.sqs.client import SqsServiceTest


def test_sqs_event_parsing():
    event = {
        "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
        "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
        "body": "test",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
        "messageAttributes": {},
        "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
        "eventSource": "aws:sqs",
        "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
        "awsRegion": "us-west-2",
    }

    event = SqsEvent.from_sqs_lambda_event(event)

    assert event.message_id == "c80e8021-a70a-42c7-a470-796e1186f753"
    assert event.receipt_handle == "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a..."
    assert event.body == "test"
    assert event.attributes["ApproximateReceiveCount"] == "1"
    assert event.attributes["SentTimestamp"] == "1523232000000"
    assert event.attributes["SenderId"] == "123456789012"
    assert event.attributes["ApproximateFirstReceiveTimestamp"] == "1523232000001"
    assert event.message_attributes == {}
    assert event.md5_of_body == "098f6bcd4621d373cade4e832627b4f6"
    assert event.event_source == "aws:sqs"
    assert event.event_source_arn == "arn:aws:sqs:us-west-2:123456789012:MyQueue"
    assert event.aws_region == "us-west-2"


def test_sqs_event_parsing_with_sns_message():
    body = {
        "topic": "queue"
    }

    event = {
        "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
        "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
        "body": dumps(body),
        "attributes": {
            "ApproximateReceiveCount": "1",
            "SentTimestamp": "1523232000000",
            "SenderId": "123456789012",
            "ApproximateFirstReceiveTimestamp": "1523232000001",
        },
        "messageAttributes": {},
        "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
        "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
        "eventSource": "aws:sqs",
        "awsRegion": "us-west-2",
    }

    event = SqsEvent.from_sqs_lambda_event(event)

    assert event.message_id == "c80e8021-a70a-42c7-a470-796e1186f753"
    assert event.receipt_handle == "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a..."
    assert event.body == dumps(body)
    assert event.attributes["ApproximateReceiveCount"] == "1"
    assert event.attributes["SentTimestamp"] == "1523232000000"
    assert event.attributes["SenderId"] == "123456789012"
    assert event.attributes["ApproximateFirstReceiveTimestamp"] == "1523232000001"
    assert event.message_attributes == {}
    assert event.md5_of_body == "098f6bcd4621d373cade4e832627b4f6"
    assert event.event_source == "aws:sqs"
    assert event.event_source_arn == "arn:aws:sqs:us-west-2:123456789012:MyQueue"
    assert event.aws_region == "us-west-2"

    parsed_body = event.try_parse()

    assert parsed_body == body

    
def test_sqs_handler():

    app = SqsHandler(getLogger("test"))

    @app.handler("queue")
    def test_handler():
        return "test"

    @app.default()
    def default_handler():
        return "default"

    assert app.handlers["queue"] == test_handler
    assert app.handlers["default"] == default_handler


def test_process_default():

    app = SqsHandler(getLogger("test"))
    app.sqs_client = SqsServiceTest()

    @app.default()
    def default_handler():
        return "default"

    response = app.process({
        "eventSource": "aws:sqs",
        "Records": [
            {
                "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": "test",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
                "messageAttributes": {},
                "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
                "awsRegion": "us-west-2",
            }
        ]

    }, {})

    assert response == ["default"]

    response = app.process({
        "eventSource": "aws:sqs",
        "Records": [
            {
                "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": dumps({
                    "topic": "queue"
                }),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
                "messageAttributes": {},
                "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-west-2:123456789012:MyQueue",
                "awsRegion": "us-west-2",
            }
        ]

    }, {})

    assert response == ["default"]
