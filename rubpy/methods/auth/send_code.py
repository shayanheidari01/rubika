from typing import Optional
import rubpy

class SendCode:
    async def send_code(self: "rubpy.Client",
                        phone_number: str,
                        pass_key: Optional[str] = None,
                        send_type: Optional[str] = 'SMS',
    ):
        # Validate send_type
        if send_type not in ('SMS', 'Internal'):
            raise ValueError('send_type can only be `SMS` or `Internal`.')

        # Prepare data for sending the code
        data = {
            'phone_number': phone_number,
            'pass_key': pass_key,
            'send_type': send_type
        }

        # Use builder to send the code
        return await self.builder(
            name='sendCode',
            input=data,
            tmp_session=True,
        )
