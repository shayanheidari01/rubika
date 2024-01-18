import rubpy


class GetPollStatus:
    async def get_poll_status(
            self: "rubpy.Client",
            poll_id: str,
    ):
        return self.builder(name='getPollStatus',
                            input={
                                'poll_id': poll_id,
                            })