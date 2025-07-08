import rubpy


class UploadFile:
    """
    Provides a method to upload a file.

    Methods:
    - upload: Upload a file.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def upload(self: "rubpy.Client", file, *args, **kwargs) -> "rubpy.types.Update":
        """
        Upload a file.

        Args:
        - file: The file to be uploaded.
        - *args: Additional positional arguments.
        - **kwargs: Additional keyword arguments.

        Returns:
        - The result of the file upload operation.
        """
        return await self.connection.upload_file(file=file, *args, **kwargs, max_retries=self.max_retries)
