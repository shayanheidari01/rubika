import tempfile
import warnings
import base64
import typing
import os
import io
from pathlib import Path

DEFAULT_TEMP_PATH = r'./temps'
path = Path(DEFAULT_TEMP_PATH)

if not path.exists():
    path.mkdir(parents=True)


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

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    VideoFileClip = None


class ResultMedia:
    """
    Represents media data along with its metadata.

    Attributes:
    - image (bytes): The raw image data.
    - width (int): The width of the media.
    - height (int): The height of the media.
    - seconds (int): The duration of the media in seconds.
    """

    def __repr__(self) -> str:
        return repr(vars(self))

    def __init__(self,
                 image: bytes,
                 width: typing.Optional[int] = 200,
                 height: typing.Optional[int] = 200,
                 seconds: typing.Optional[int] = 1) -> None:
        """
        Initialize ResultMedia with image data and metadata.

        Args:
        - image (bytes): The raw image data.
        - width (int): The width of the media.
        - height (int): The height of the media.
        - seconds (int): The duration of the media in seconds.
        """
        self.image = image
        self.width = width
        self.height = height
        self.seconds = seconds

        if hasattr(cv2, 'imdecode'):
            if not isinstance(image, np.ndarray):
                image = np.frombuffer(image, dtype=np.uint8)
                image = cv2.imdecode(image, flags=1)

            self.image = self.ndarray_to_bytes(image)

    def ndarray_to_bytes(self, image, *args, **kwargs) -> bytes:
        """
        Convert NumPy array to bytes.

        Args:
        - image: NumPy array representing the image.

        Returns:
        - bytes: The image data in bytes.
        """
        if hasattr(cv2, 'resize'):
            width = image.shape[1]
            height = image.shape[0]
            image = cv2.resize(image,
                            (width, height),
                            interpolation=cv2.INTER_CUBIC)

            status, buffer = cv2.imencode('.png', image)
            if status is True:
                return io.BytesIO(buffer).read()

        return self.image

    def to_base64(self):
        """
        Convert media data to base64.

        Returns:
        - str: Base64-encoded media data.
        """
        return base64.b64encode(self.image).decode('utf-8')

class MediaThumbnail:
    """
    Provides methods to generate media thumbnails.

    Methods:
    - from_image: Generate a thumbnail from image data.
    - from_video: Generate a thumbnail from video data.
    """

    @classmethod
    def from_image(cls, image: bytes) -> ResultMedia:
        """
        Generate a thumbnail from image data.

        Args:
        - image (bytes): The raw image data.

        Returns:
        - ResultMedia: ResultMedia object containing the thumbnail and metadata.
        """
        # Check if PIL is available
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
        # Calculate aspect ratio
        aspect_ratio = width / height
        new_width = 720
        new_height = int(new_width / aspect_ratio)
        # Resize the image to fit within 720x720
        if new_height > new_width:
            new_height = 720
            new_width = int(new_height * aspect_ratio)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

        # Encode the image to PNG format
        status, buffer = cv2.imencode('.png', image)
        if status:
            return ResultMedia(bytes(buffer), width=new_width, height=new_height)

    @classmethod
    def from_video(cls, video: bytes) -> typing.Optional[ResultMedia]:
        """
        Generate a thumbnail from video data.

        Args:
        - video (bytes): The raw video data.

        Returns:
        - ResultMedia: ResultMedia object containing the thumbnail and metadata.
        """
        if VideoFileClip is not None:
            return cls._from_video_moviepy(video)
        elif cv2 is not None:
            return cls._from_video_opencv(video)
        elif PIL is not None:
            return cls._from_video_moviepy(video)
        else:
            warnings.warn('OpenCV and MoviePy not found, video processing disabled')
            return None

    @classmethod
    def _from_video_opencv(cls, video: bytes) -> typing.Optional[ResultMedia]:
        """
        Generate a thumbnail from video data using OpenCV.

        Args:
        - video (bytes): The raw video data.

        Returns:
        - ResultMedia: ResultMedia object containing the thumbnail and metadata.
        """
        with tempfile.NamedTemporaryFile(mode='wb+', suffix='.mp4', dir=DEFAULT_TEMP_PATH) as file:
            file.write(video)

            # Read the video using OpenCV
            capture = cv2.VideoCapture(file.name)
            # Check if the video is opened successfully
            if not capture.isOpened():
                warnings.warn('Failed to open video file')
                return None

            # Read the first frame
            status, frame = capture.read()

            # If successful, create ResultMedia object
            if status:
                # Get video properties
                width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = capture.get(cv2.CAP_PROP_FPS)
                total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
                seconds = int(total_frames / fps)

                # Resize the frame to 720x720
                frame = cv2.resize(frame, (720, 720), interpolation=cv2.INTER_CUBIC)

                # Release the video capture object
                capture.release()

                return ResultMedia(frame, width=720, height=720, seconds=seconds)

        return None

    @classmethod
    def _from_video_moviepy(cls, video: bytes) -> typing.Optional[ResultMedia]:
        """
        Generate a thumbnail from video data using MoviePy.

        Args:
        - video (bytes): The raw video data.

        Returns:
        - ResultMedia: ResultMedia object containing the thumbnail and metadata.
        """
        try:
            # Save the video to a temporary file
            with tempfile.NamedTemporaryFile(mode='wb+', suffix='.mp4', dir=DEFAULT_TEMP_PATH, delete=False) as file:
                file.write(video)
                file_name = file.name

            # Read the video using MoviePy
            clip = VideoFileClip(file_name)

            # Extract the first frame
            frame = clip.get_frame(0)

            # Close the clip and remove the temporary file
            clip.close()
            os.remove(file_name)

            # Resize the frame to 720x720
            frame_resized = cv2.resize(frame, (720, 720), interpolation=cv2.INTER_CUBIC)

            # Convert frame to BGR (OpenCV uses BGR by default)
            frame_bgr = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2BGR)

            return ResultMedia(frame_bgr, width=720, height=720, seconds=int(clip.duration))

        except Exception as e:
            print(f"Error processing video with MoviePy: {e}")
            os.remove(file_name)
            return None
