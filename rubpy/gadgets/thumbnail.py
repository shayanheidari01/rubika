import io
import base64
import tempfile


try:
    import cv2
    import numpy

except ImportError:
    cv2 = None
    numpy = None

DEFAULT_IMAGE_THUMB = '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'

class Thumbnail:
    def __init__(self,
                 image: bytes,
                 width: int = 200,
                 height: int = 200,
                 seconds: int = 1, *args, **kwargs) -> None:

        self.image = image
        self.width = width
        self.height = height
        self.seconds = seconds

        if isinstance(self.image, str):
            with open(image, 'rb') as file:
                self.image = file.read()

    def to_base64(self, *args, **kwargs) -> str:
        if self.image is not None:
            return base64.b64encode(self.image).decode('utf-8')

        return DEFAULT_IMAGE_THUMB


class MakeThumbnail(Thumbnail):
    def __init__(self,
                 image,
                 width: int = 200,
                 height: int = 200,
                 seconds: int = 1, *args, **kwargs) -> None:
        self.image = None
        self.width = width
        self.height = height
        self.seconds = seconds

        if hasattr(cv2, 'imdecode'):
            if not isinstance(image, numpy.ndarray):
                image = numpy.frombuffer(image, dtype=numpy.uint8)
                image = cv2.imdecode(image, flags=1)

            self.image = self.ndarray_to_bytes(image)

    def ndarray_to_bytes(self, image, *args, **kwargs) -> str:
        if hasattr(cv2, 'resize'):
            self.width = image.shape[1]
            self.height = image.shape[0]
            image = cv2.resize(image,
                               (round(self.width / 10), round(self.height / 10)),
                               interpolation=cv2.INTER_CUBIC)

            status, buffer = cv2.imencode('.png', image)
            if status is True:
                return io.BytesIO(buffer).read()

    @classmethod
    def from_video(cls, video: bytes, *args, **kwargs):
        if hasattr(cv2, 'VideoCapture'):
            with tempfile.TemporaryFile(mode='wb+') as file:
                file.write(video)
                capture = cv2.VideoCapture(file.name)
                status, image = capture.read()

                if status is True:
                    fps = capture.get(cv2.CAP_PROP_FPS)
                    frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
                    return MakeThumbnail(
                        image=image,
                        seconds=int(frames / fps) * 1000, *args, **kwargs)

        return MakeThumbnail(image=DEFAULT_IMAGE_THUMB, *args, **kwargs)