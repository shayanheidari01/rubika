import tempfile
import warnings
import base64
import typing
import io
import os
from pathlib import Path

DEFAULT_TEMP_PATH = r'./temps'
path = Path(DEFAULT_TEMP_PATH)

if not path.exists():
    path.mkdir(parents=True)

try:
    from moviepy.editor import VideoFileClip

except ImportError:
    VideoFileClip = None

try:
    import cv2
    import numpy as np

except ImportError:
    cv2 = None
    numpy = None

try:
    import PIL.Image

except ImportError:
    PIL = None


class ResultMedia:
    def __repr__(self) -> str:
        return repr(vars(self))

    def __init__(self,
                 image: bytes,
                 width: typing.Optional[int] = 200,
                 height: typing.Optional[int] = 200,
                 seconds: typing.Optional[int] = 1) -> None:
        self.image = image
        self.width = width
        self.height = height
        self.seconds = seconds

        if hasattr(cv2, 'imdecode'):
            if not isinstance(image, np.ndarray):
                image = np.frombuffer(image, dtype=np.uint8)
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

    def to_base64(self):
        return base64.b64encode(self.image).decode('utf-8')


class MediaThumbnail:
    @classmethod
    def from_image(cls, image: bytes) -> ResultMedia:
        # Check if PIL is avaliable
        if PIL is not None:
            image, output = PIL.Image.open(io.BytesIO(image)), io.BytesIO()
            width, height = image.size
            image.save(output, format='PNG')
            return ResultMedia(output.getvalue(), width=width, height=height)

        # Check if OpenCV and NumPy are available
        if cv2 is None or np is None:
            warnings.warn('OpenCV or NumPy not found, image processing disabled')
            return None

        # If image is not a NumPy array, convert it
        if not isinstance(image, np.ndarray):
            image = np.frombuffer(image, dtype=np.uint8)
            image = cv2.imdecode(image, flags=1)

        # Resize the image
        height, width = image.shape[0], image.shape[1]
        image = cv2.resize(image, (round(width / 10), round(height / 10)), interpolation=cv2.INTER_CUBIC)

        # Encode the image to PNG format
        status, buffer = cv2.imencode('.png', image)
        if status:
            return ResultMedia(bytes(buffer), width=width, height=height)

    @classmethod
    def from_video(cls, video: bytes) -> typing.Optional[ResultMedia]:
        if VideoFileClip and PIL is not None:
            file = tempfile.NamedTemporaryFile(mode='wb+', suffix='.rp-temp', dir=DEFAULT_TEMP_PATH, delete=False)
            file.write(video)
            file_name = file.name
            file.close()
            os.chmod(file_name, 0o777)
            capture = VideoFileClip(file_name)
            width, height = capture.size
            seconds = capture.duration * 1000
            image = capture.get_frame(0)
            capture.close()
            os.remove(file_name)
            return ResultMedia(image, width, height, seconds)

        # Check if OpenCV is available
        if cv2 is None:
            warnings.warn('OpenCV not found, video processing disabled')
            return None

        # Write video content to a temporary file
        with tempfile.NamedTemporaryFile(mode='wb+', suffix='.rp-temp', dir=DEFAULT_TEMP_PATH) as file:
            file.write(video)

            # Read the video using OpenCV
            capture = cv2.VideoCapture(file.name)
            status, image = capture.read()

            # If successful, calculate video duration and create ResultMedia object
            if status is True:
                fps = capture.get(cv2.CAP_PROP_FPS)
                frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
                seconds = int(frames / fps) * 1000
                width = image.shape[1]
                height = image.shape[0]

                return ResultMedia(image, width, height, seconds)