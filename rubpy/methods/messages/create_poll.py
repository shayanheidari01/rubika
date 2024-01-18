from typing import Union
from random import random


class CreatePoll:
    async def create_poll(
            self,
            object_guid: str,
            question: str,
            options: list,
            type: str = 'Regular',
            is_anonymous: bool = True,
            allows_multiple_answers: bool = True,
            correct_option_index: Union[int, str] = None,
            explanation: str = None,
            reply_to_message_id: Union[str, int] = 0,
    ):
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