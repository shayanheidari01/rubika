import rubpy

class GetTime:
    async def get_time(self: "rubpy.Client"):
        return self.builder("getTime")