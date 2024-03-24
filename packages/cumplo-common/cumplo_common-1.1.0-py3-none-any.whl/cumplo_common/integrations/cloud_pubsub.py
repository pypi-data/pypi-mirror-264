import json

from google.cloud.pubsub import PublisherClient

from cumplo_common.utils.constants import PROJECT_ID


def publish_event(content: dict | list, topic: str, **attributes: str) -> str:
    """
    Publish an event to a topic with the given attributes.

    Args:
        content (dict): A dictionary containing the event data
        topic (str): The topic name to publish the event to
        **attributes (str): A sequence of key-value pairs to be used as event attributes

    Returns:
        str: The ID of the published event
    """
    publisher = PublisherClient()
    topic = f"projects/{PROJECT_ID}/topics/{topic}"
    data = json.dumps(content).encode()
    future = publisher.publish(topic, data, **attributes)
    return future.result()
