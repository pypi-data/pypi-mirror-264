from logging import getLogger

from cumplo_common.database.firestore.subcollections import UserSubcollection
from cumplo_common.models.channel import CHANNEL_CONFIGURATION_BY_TYPE, ChannelConfiguration, ChannelType
from cumplo_common.utils.constants import CHANNELS_COLLECTION

logger = getLogger(__name__)


class ChannelCollection(UserSubcollection):
    __id__ = CHANNELS_COLLECTION

    def get(self, id_user: str, id_document: str) -> ChannelConfiguration:
        """
        Gets a specific Channel of a given user

        Args:
            id_user (str): The user ID which owns the channel
            id_document (str): The channel type to be retrieved

        Raises:
            KeyError: When the channel does not exist

        Returns:
            ChannelConfiguration: The channel configuration data
        """
        logger.info(f"Getting user {id_user} configurations from Firestore")
        document = self._collection(id_user).document(id_document).get()
        if document.exists and (data := document.to_dict()):
            return CHANNEL_CONFIGURATION_BY_TYPE[ChannelType(document.id)](**data)

        raise KeyError(f"CHannel with ID {id_document} does not exist")

    def get_all(self, id_user: str) -> dict[ChannelType, ChannelConfiguration]:
        """
        Gets the user channels data

        Args:
            id_user (str): The user ID which owns the channels

        Returns:
            dict[ChannelType, ChannelConfiguration]: A dictionary containing the user channels
        """
        logger.info(f"Getting user {id_user} channels from Firestore")
        stream = self._collection(id_user).stream()
        return {
            ChannelType(document.id): CHANNEL_CONFIGURATION_BY_TYPE[ChannelType(document.id)](**data)
            for document in stream
            if (data := document.to_dict())
        }

    def put(self, id_user: str, data: ChannelConfiguration) -> None:
        """
        Creates or updates a channel of a given user

        Args:
            id_user (str): The user ID which owns the channel
            data (ChannelConfiguration): The new channel data to be upserted
        """
        logger.info(f"Upserting channel {data.type_} of user {id_user} into Firestore")
        document = self._collection(id_user).document(str(data.type_))
        document.set(data.json(exclude={"type_"}))

    def delete(self, id_user: str, id_document: str) -> None:
        """
        Deletes a channel for a given user and channel ID

        Args:
            id_user (str): The user ID which owns the configuration
            id_document (int): The channel type to be deleted
        """
        channel_type = ChannelType(id_document)
        logger.info(f"Deleting channel {channel_type} from Firestore")
        document = self._collection(id_user).document(channel_type)
        document.delete()
