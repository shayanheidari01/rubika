from typing import Optional
import rubpy

class UpdateProfile:
    """
    Provides a method to update user profile information.

    Methods:
    - update_profile: Update user profile information.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def update_profile(
            self: "rubpy.Client",
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            bio: Optional[str] = None,
            birth_date: Optional[str] = None,
    ) -> rubpy.types.Update:
        """
        Update user profile information.

        Parameters:
        - first_name (Optional[str]): The updated first name.
        - last_name (Optional[str]): The updated last name.
        - bio (Optional[str]): The updated biography.

        Returns:
        - rubpy.types.Update: The updated user information after the profile update.
        """
        if first_name is None and last_name is None and bio is None and birth_date is None:
            raise ValueError('At least one parameter (first_name, last_name, bio, birth_date) should be provided for update.')

        input_data = {'updated_parameters': []}

        if first_name is not None:
            input_data['updated_parameters'].append('first_name')
            input_data['first_name'] = first_name

        if last_name is not None:
            input_data['updated_parameters'].append('last_name')
            input_data['last_name'] = last_name

        if bio is not None:
            input_data['updated_parameters'].append('bio')
            input_data['bio'] = bio

        if birth_date is not None:
            input_data['updated_parameters'].append('birth_date')
            input_data['birth_date'] = birth_date

        return await self.builder(name='updateProfile', input=input_data)  # type: ignore
