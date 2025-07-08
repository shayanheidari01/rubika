from typing import Union
from random import random
import rubpy

class CreatePoll:
    """
    Provides a method to create a poll message.

    Methods:
    - create_poll: Create a poll message with the specified parameters.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def create_poll(
            self: "rubpy.Client",
            object_guid: str,
            question: str,
            options: list,
            type: str = 'Regular',
            is_anonymous: bool = True,
            allows_multiple_answers: bool = True,
            correct_option_index: Union[int, str] = None,
            explanation: str = None,
            reply_to_message_id: Union[str, int] = 0,
    ) -> rubpy.types.Update:
        """
        Create a poll message with the specified parameters.

        Parameters:
        - object_guid (str): The GUID of the object associated with the poll (e.g., user, group, channel).
        - question (str): The question for the poll.
        - options (list): A list of string values representing the poll options.
        - type (str): The type of the poll, can be 'Regular' or 'Quiz'.
        - is_anonymous (bool): Whether the poll is anonymous or not.
        - allows_multiple_answers (bool): Whether the poll allows multiple answers or not.
        - correct_option_index (Union[int, str]): The index or ID of the correct option for quiz-type polls.
        - explanation (str): An explanation for the correct answer in quiz-type polls.
        - reply_to_message_id (Union[str, int]): The ID of the message to reply to.

        Returns:
        - rubpy.types.Update: The updated information after creating the poll.
        """
        if len(options) <= 1:
            raise ValueError('The `options` argument must have more than two string values.')

        if type not in ('Quiz', 'Regular'):
            raise ValueError('The `type` argument can only be in `["Quiz", "Regular"]`.')

        input = {
            'object_guid': object_guid,
            'question': question,
            'options': options,
            'allows_multiple_answers': allows_multiple_answers,
            'is_anonymous': is_anonymous,
            'reply_to_message_id': reply_to_message_id,
            'type': type,
            'rnd': int(random() * 1e6 + 1),
        }

        if type == 'Quiz':
            input['correct_option_index'] = correct_option_index
            input['explanation'] =  explanation

        return await self.builder('createPoll', input=input)
