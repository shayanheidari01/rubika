from typing import Optional
import rubpy

class UpdateProfile:
    async def update_profile(
            self: "rubpy.Client",
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            bio: Optional[str] = None,
    ):
        if first_name and last_name and bio is None:
            raise ValueError('All parameters are None.')

        input = {'updated_parameters': []}

        if first_name is not None:
            input['updated_parameters'].append('first_name')
            input['first_name'] = first_name

        if last_name is not None:
            input['updated_parameters'].append('last_name')
            input['last_name'] = last_name

        if bio is not None:
            input['updated_parameters'].append('bio')
            input['bio'] = bio

        return await self.builder(name='updateProfile', input=input)