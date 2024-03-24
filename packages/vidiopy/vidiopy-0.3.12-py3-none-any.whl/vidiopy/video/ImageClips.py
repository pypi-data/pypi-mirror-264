from pathlib import Path
from typing import Callable, Self
from PIL import Image, ImageFont, ImageDraw
from .ImageSequenceClip import ImageSequenceClip
import numpy as np
import numpy.typing as npt
from . import VideoClip
from ..decorators import *


class ImageClip(VideoClip.VideoClip):
    """
    A class representing a video clip generated from a single image.

    Attributes:
    - image (Image.Image | None): The image data used in the ImageClip.
    - fps (int | float | None): Frames per second of the video clip.
    - start (float): Start time of the video clip in seconds (always 0.0).
    - duration (int | float | None): Duration of the video clip in seconds.
    - end (int | float | None): End time of the video clip in seconds (equals duration).
    - size (Tuple[int, int] | None): Size of the image (width, height).

    Methods:
    - __init__(self, image: str | Path | Image.Image | np.ndarray | None = None, fps: int | float | None = None, duration: int | float | None = None):
        Initialize an ImageClip instance.
    - fl_frame_transform(self, func, *args, **kwargs) -> ImageClip:
        Apply a frame transformation function to the image.
    - fl_clip(self, func, *args, **kwargs) -> ImageClip:
        Raise a ValueError indicating that fl_clip is not applicable for ImageClip.
    - fx(self, func: Callable, *args, **kwargs) -> ImageClip:
        Apply a generic function to the ImageClip.
    - make_frame_any(self, t) -> Image.Image:
        Generate a frame for a given time.
    - make_frame_array(self, t) -> np.ndarray:
        Generate a frame array for a given time.
    - make_frame_pil(self, t) -> Image.Image:
        Generate a frame using PIL for a given time.

    Note:
    The ImageClip class extends the VideoClip class from the Vidiopy library and is designed
    for creating video clips from a single image. It provides methods for frame transformations,
    applying generic functions, and generating frames in different formats.

    Example Usage:
    ```python
    image_clip = ImageClip(image_path, fps=30, duration=5.0)
    transformed_clip = image_clip.fl_frame_transform(resize, width=640, height=480)
    final_video = transformed_clip.to_video_clip()
    ```
    """

    def __init__(
        self,
        image: str | Path | Image.Image | np.ndarray | None = None,
        fps: int | float | None = None,
        duration: int | float | None = None,
    ):
        """
        Initialize an ImageClip instance.

        Parameters:
        - image (str | Path | Image.Image | np.ndarray | None, optional):
            Input image path or image data. Defaults to None.
        - fps (int | float | None, optional): Frames per second of the video clip. Defaults to None.
        - duration (int | float | None, optional): Duration of the video clip in seconds. Defaults to None.

        Note: If image is provided, it will be imported and used as the source for the ImageClip.
              If not provided, the ImageClip will be initialized with default values.

        Attributes:
        - image (Image.Image | None): The image data used in the ImageClip.
        - fps (int | float | None): Frames per second of the video clip.
        - start (float): Start time of the video clip in seconds (always 0.0).
        - duration (int | float | None): Duration of the video clip in seconds.
        - end (int | float | None): End time of the video clip in seconds (equals duration).
        - size (Tuple[int, int] | None): Size of the image (width, height).

        Returns:
        - None
        """
        super().__init__()
        if isinstance(image, (str, Path)):
            self.imagepath = image
        else:
            self.imagepath = None
        # Import image if provided
        self.image: npt.NDArray[np.uint8] | None = (
            self._import_image(image) if image is not None else None
        )

        # Set properties
        self.fps = fps
        self.start = 0.0
        if duration is not None:
            self._dur = duration
        self.end = self.duration

        if self.image is not None:
            self.size = self.image.shape[:2][::-1]

    def _import_image(self, image) -> npt.NDArray[np.uint8]:
        """
        Import the image from various sources.

        Parameters:
        - image (str | Path | Image.Image | np.ndarray): Input image data.

        Returns:
        - Image.Image: The imported image data.
        """
        if isinstance(image, Image.Image):
            return np.array(image)
        elif isinstance(image, np.ndarray):
            return image
        elif isinstance(image, (str, Path, bytes)):
            return np.array(Image.open(image))
        return np.array(Image.open(image))

    def __repr__(self):
        return f"""{self.__class__.__name__}(fps={self.fps}, size={self.size}, start={self.start}, end={self.end}, duration={self.duration}, imagepath={self.imagepath}, id={hex(id(self))})"""

    def __str__(self):
        return f"""{self.__class__.__name__}(fps={self.fps}, size={self.size}, start={self.start}, end={self.end}, duration={self.duration})"""

    def __eq__(self, other):
        if not isinstance(other, ImageClip):
            return False
        return (
            self.fps == other.fps
            and self.size == other.size
            and self.start == other.start
            and self.end == other.end
            and self.duration == other.duration
            and np.array_equal(self.image, other.image)
        )

    @property
    def duration(self):
        return self._dur

    @duration.setter
    def duration(self, value: int | float | None):
        self._dur = value
        return self

    def set_duration(self, value) -> Self:
        self._dur = value
        return self

    def fl_frame_transform(self, func, *args, **kwargs) -> Self:
        """
        Apply a frame transformation function to the image.

        Parameters:
        - func (Callable): The frame transformation function.
        - *args: Additional positional arguments for the function.
        - **kwargs: Additional keyword arguments for the function.

        Returns:
        - ImageClip: A new ImageClip instance with the transformed image.

        Note: This method modifies the current ImageClip instance in-place.

        Example Usage:
        ```python
        image_clip = ImageClip(image_path, fps=30, duration=5.0)
        transformed_clip = image_clip.fl_frame_transform(resize, width=640, height=480)
        ```
        """
        self.image = func(self.image, *args, **kwargs)
        return self

    def fl_clip_transform(self, func, *args, **kwargs) -> Self:
        """
        Raise a ValueError indicating that fl_clip is not applicable for ImageClip.

        The Clip should be converted to VideoClip using `to_video_clip` method first.

        Parameters:
        - func: Unused.
        - *args: Unused.
        - **kwargs: Unused.

        Returns:
        - ImageClip: The current ImageClip instance.

        Raises:
        - ValueError: This method is not applicable for ImageClip.

        Example Usage:
        ```python
        image_clip = ImageClip(image_path, fps=30, duration=5.0)
        image_clip.fl_clip(some_function)  # Raises ValueError
        ```
        """
        raise ValueError(
            "Convert this Image Clip to Video Clip following is the function `to_video_clip`"
        )
        return self

    def sub_fx(
        self,
        func,
        *args,
        start_t: int | float | None = None,
        end_t: int | float | None = None,
        **kwargs,
    ) -> Self:
        """
        Apply a custom function to the Image Clip.

        Note: Before using the `sub_fx` method, you need to convert the image clip to a video clip using `to_video_clip()` function.

        Args:
            func: The custom function to apply to the Image Clip.
            *args: Additional positional arguments to pass to the custom function.
            start_t: The start time of the subclip in seconds. If None, the subclip starts from the beginning.
            end_t: The end time of the subclip in seconds. If None, the subclip ends at the last frame.
            **kwargs: Additional keyword arguments to pass to the custom function.

        Returns:
            Self: The modified ImageClips instance.

        Example:
            ```python
            # Convert the image clip to a video clip
            video_clip = image_clip.to_video_clip()

            # Apply a custom function to the video clip
            modified_clip = video_clip.sub_fx(custom_function, start_t=2, end_t=5)
            ```

        Raises:
            ValueError: If the method is called on an Image Clip instead of a Video Clip.
        """
        raise ValueError(
            "Convert this Image Clip to Video Clip following is the function `to_video_clip`"
        )
        return self

    def sub_clip_copy(
        self, start: int | float | None = None, end: int | float | None = None
    ) -> Self:
        """
        Create a copy of the current clip and apply sub-clip operation.
        Read more about sub-clip operation in the `sub_clip` method.

        Args:
            start (int | float | None): Start time of the sub-clip in seconds.
                If None, the sub-clip starts from the beginning of the original clip.
            end (int | float | None): End time of the sub-clip in seconds.
                If None, the sub-clip ends at the end of the original clip.

        Returns:
            Self: A new instance of the clip with the sub-clip applied.
        """
        clip = self.copy()
        clip.sub_clip(start, end)
        return clip

    def sub_clip(
        self, start: int | float | None = None, end: int | float | None = None
    ) -> Self:
        """
        Returns a sub-clip of the current clip.

        Args:
            start (int | float | None, optional): The start time of the sub-clip in seconds. Defaults to None.
            end (int | float | None, optional): The end time of the sub-clip in seconds. Defaults to None.

        Returns:
            Self: The sub-clip.

        Note:
            It modifies the current clip in-place.
            If both `start` and `end` are None, the original clip is returned.
            If `start` is None, it defaults to 0.
            If `end` is None, it defaults to the end time of the original clip.
        """
        if start is None and end is None:
            return self
        if start is None:
            start = 0.0
        if end is None:
            end = (
                self.end
                if self.end is not None
                else self.duration - start if self.duration is not None else None
            )
        self._st = 0
        self._dur = end - start if end is not None else None
        self.end = self._dur
        return self

    def make_frame_array(self, t) -> npt.NDArray[np.uint8]:
        """
        Gives the numpy array representation of the image at a given time.

        Args:
            t (float): The timestamp of the frame.

        Returns:
            numpy.ndarray: The numpy array representation of the image.

        Raises:
            ValueError: If the image is not set.
        """
        if self.image is None:
            raise ValueError("image is not set")
        return self.image

    def make_frame_pil(self, t) -> Image.Image:
        """
        Returns the image frame at a given time.

        Args:
            t (float): The time at which to retrieve the frame.

        Returns:
            PIL.Image.Image: The image frame at the given time.

        Raises:
            ValueError: If the image is not set.
        """
        if self.image is None:
            raise ValueError("image is not set")
        return Image.fromarray(self.image)

    def to_video_clip(self, fps=None, duration=None):
        """
        Convert `ImageClip` to `VideoClip`

        If fps or duration is not provided, it defaults to the corresponding attribute
        of the ImageClip instance. If those attributes are not available, a ValueError is raised.

        Parameters:
        - fps (float, optional): Frames per second of the resulting video clip.
            If not provided, it defaults to the fps attribute of the ImageClip instance.
            If that is also not available, a ValueError is raised.
        - duration (float, optional): Duration of the resulting video clip in seconds.
            If not provided, it defaults to the duration attribute of the ImageClip instance.
            If that is also not available, a ValueError is raised.
        - start (float, optional): Start time of the resulting video clip in seconds. Default is 0.0.
        - end (float, optional): End time of the resulting video clip in seconds.
            If not provided, it defaults to the end attribute of the ImageClip instance,
            or if that is not available, it is calculated based on start and duration.

        Returns:
        - ImageSequenceClip: A VideoClip subclass instance generated from the ImageClip frames.

        Raises:
        - ValueError: If fps or duration is not provided and the corresponding attribute is not available.

        Note:
        The `to_video_clip` method returns an instance of the `ImageSequenceClip` class,
        which is a subclass of the `VideoClip` Class.

        Example Usage:
        ```python
        # Example Usage
        image_clip = ImageClip()
        video_clip = image_clip.to_video_clip(fps=24, duration=10.0, start=2.0, end=12.0)
        video_clip.sub_fx(custom_function, start_t=2, end_t=5)
        ```
        """
        if fps is None:
            fps = self.fps
            if fps is None:
                raise ValueError("fps should be set of specify")
        if duration is None:
            duration = self.duration
            if duration is None:
                duration = self.end + self.start if self.end is not None else None
                if duration is None:
                    raise ValueError("duration should be set of specify")
        # Generate frames using make_frame_pil
        constant_frame = self.make_frame_pil(0)
        frames = (constant_frame,) * int((duration) * fps)

        # Create ImageSequenceClip from frames
        return (
            ImageSequenceClip(frames, fps=fps, duration=duration, audio=self.audio)
            .set_start(self.start)
            .set_end(self.end)
        )


class Data2ImageClip(ImageClip):
    """
    A class representing a video clip generated from raw data (numpy array or PIL Image).

    Parameters:
    - data (np.ndarray or PIL Image): The raw data to be converted into a video clip.
    - fps (int or float, optional): Frames per second of the video. If not provided, it will be inherited
      from the parent class (ImageClip) or set to the default value.
    - duration (int or float, optional): Duration of the video in seconds. If not provided, it will be
      inherited from the parent class (ImageClip) or set to the default value.

    Attributes:
    - image (PIL Image): The PIL Image representation of the provided data.
    - size (tuple): The size (width, height) of the image.

    Methods:
    - _import_image(image): Private method to convert the provided data (numpy array or PIL Image)
      into a PIL Image.

    Example:
    ```
    # Import necessary libraries

    # Create a Data2ImageClip instance from a numpy array
    data_array = np.random.randint(0, 255, size=(480, 640, 3), dtype=np.uint8)
    video_clip = Data2ImageClip(data=data_array, fps=30, duration=5)

    # Create a Data2ImageClip instance from a PIL Image
    from PIL import Image
    data_image = Image.new('RGB', (640, 480), color='red')
    video_clip = Data2ImageClip(data=data_image, fps=24, duration=10)
    ```

    Note:
    The `Data2ImageClip` class extends the `ImageClip`. It allows
    users to create video clips from raw data, supporting either numpy arrays or PIL Images as input.
    """

    def __init__(
        self,
        data: np.ndarray | Image.Image,
        fps: int | float | None = None,
        duration: int | float | None = None,
    ):
        # Initialize the class by calling the parent constructor
        super().__init__(fps=fps, duration=duration)

        # Import the image from the provided data
        self.image = self._import_image(data)

        # Set the size attribute based on the image size
        self.size = self.image.shape[:2]

    def _import_image(self, image) -> npt.NDArray[np.uint8]:
        """
        Private method to convert the provided data (numpy array or PIL Image) into a PIL Image.

        Parameters:
        - image (np.ndarray or PIL Image): The raw data to be converted.

        Returns:
        - PIL Image: The PIL Image representation of the provided data.

        Raises:
        - TypeError: If the input type is not supported (neither numpy array nor PIL Image).
        """
        # Convert the provided data (numpy array or PIL Image) into a PIL Image
        if isinstance(image, np.ndarray):
            return image
        elif isinstance(image, Image.Image):
            return np.array(image)

        else:
            # Raise an error if the input type is not supported
            raise TypeError(f"{type(image)} is not an Image.Image or numpy array Type.")


class ColorClip(Data2ImageClip):
    """
    A video clip class with a solid color.

    Parameters:
    - color: str or tuple[int, ...]
        Color of the image. It can be a color name (e.g., 'red', 'blue') or RGB tuple.
    - mode: str
        Mode to use for the image. Default is 'RGBA'.
    - size: tuple
        Size of the image in pixels (width, height). Default is (1, 1) for changing size after wards.
    - fps: float, optional
        Frames per second for the video clip.
    - duration: float, optional
        Duration of the video clip in seconds.

    Examples:
    1. Create a red square video clip (500x500, 30 FPS, 5 seconds):
    ```python
    red_square = ColorClip(color='red', size=(500, 500), fps=30, duration=5)
    ```

    2. Create a blue fullscreen video clip (1920x1080, default FPS and duration):
    ```python
    blue_fullscreen = ColorClip(color='blue', size=(1920, 1080))
    ```

    3. Create a green transparent video clip (RGBA mode, 800x600):
    ```python
    green_transparent = ColorClip(color=(0, 255, 0, 0), mode='RGBA', size=(800, 600))
    ```
    Accepted Color string:
    ```
    {   "aliceblue": "#f0f8ff",
        "antiquewhite": "#faebd7",
        "aqua": "#00ffff",
        "aquamarine": "#7fffd4",
        "azure": "#f0ffff",
        "beige": "#f5f5dc",
        "bisque": "#ffe4c4",
        "black": "#000000",
        "blanchedalmond": "#ffebcd",
        "blue": "#0000ff",
        "blueviolet": "#8a2be2",
        "brown": "#a52a2a",
        "burlywood": "#deb887",
        "cadetblue": "#5f9ea0",
        "chartreuse": "#7fff00",
        "chocolate": "#d2691e",
        "coral": "#ff7f50",
        "cornflowerblue": "#6495ed",
        "cornsilk": "#fff8dc",
        "crimson": "#dc143c",
        "cyan": "#00ffff",
        "darkblue": "#00008b",
        "darkcyan": "#008b8b",
        "darkgoldenrod": "#b8860b",
        "darkgray": "#a9a9a9",
        "darkgrey": "#a9a9a9",
        "darkgreen": "#006400",
        "darkkhaki": "#bdb76b",
        "darkmagenta": "#8b008b",
        "darkolivegreen": "#556b2f",
        "darkorange": "#ff8c00",
        "darkorchid": "#9932cc",
        "darkred": "#8b0000",
        "darksalmon": "#e9967a",
        "darkseagreen": "#8fbc8f",
        "darkslateblue": "#483d8b",
        "darkslategray": "#2f4f4f",
        "darkslategrey": "#2f4f4f",
        "darkturquoise": "#00ced1",
        "darkviolet": "#9400d3",
        "deeppink": "#ff1493",
        "deepskyblue": "#00bfff",
        "dimgray": "#696969",
        "dimgrey": "#696969",
        "dodgerblue": "#1e90ff",
        "firebrick": "#b22222",
        "floralwhite": "#fffaf0",
        "forestgreen": "#228b22",
        "fuchsia": "#ff00ff",
        "gainsboro": "#dcdcdc",
        "ghostwhite": "#f8f8ff",
        "gold": "#ffd700",
        "goldenrod": "#daa520",
        "gray": "#808080",
        "grey": "#808080",
        "green": "#008000",
        "greenyellow": "#adff2f",
        "honeydew": "#f0fff0",
        "hotpink": "#ff69b4",
        "indianred": "#cd5c5c",
        "indigo": "#4b0082",
        "ivory": "#fffff0",
        "khaki": "#f0e68c",
        "lavender": "#e6e6fa",
        "lavenderblush": "#fff0f5",
        "lawngreen": "#7cfc00",
        "lemonchiffon": "#fffacd",
        "lightblue": "#add8e6",
        "lightcoral": "#f08080",
        "lightcyan": "#e0ffff",
        "lightgoldenrodyellow": "#fafad2",
        "lightgreen": "#90ee90",
        "lightgray": "#d3d3d3",
        "lightgrey": "#d3d3d3",
        "lightpink": "#ffb6c1",
        "lightsalmon": "#ffa07a",
        "lightseagreen": "#20b2aa",
        "lightskyblue": "#87cefa",
        "lightslategray": "#778899",
        "lightslategrey": "#778899",
        "lightsteelblue": "#b0c4de",
        "lightyellow": "#ffffe0",
        "lime": "#00ff00",
        "limegreen": "#32cd32",
        "linen": "#faf0e6",
        "magenta": "#ff00ff",
        "maroon": "#800000",
        "mediumaquamarine": "#66cdaa",
        "mediumblue": "#0000cd",
        "mediumorchid": "#ba55d3",
        "mediumpurple": "#9370db",
        "mediumseagreen": "#3cb371",
        "mediumslateblue": "#7b68ee",
        "mediumspringgreen": "#00fa9a",
        "mediumturquoise": "#48d1cc",
        "mediumvioletred": "#c71585",
        "midnightblue": "#191970",
        "mintcream": "#f5fffa",
        "mistyrose": "#ffe4e1",
        "moccasin": "#ffe4b5",
        "navajowhite": "#ffdead",
        "navy": "#000080",
        "oldlace": "#fdf5e6",
        "olive": "#808000",
        "olivedrab": "#6b8e23",
        "orange": "#ffa500",
        "orangered": "#ff4500",
        "orchid": "#da70d6",
        "palegoldenrod": "#eee8aa",
        "palegreen": "#98fb98",
        "paleturquoise": "#afeeee",
        "palevioletred": "#db7093",
        "papayawhip": "#ffefd5",
        "peachpuff": "#ffdab9",
        "peru": "#cd853f",
        "pink": "#ffc0cb",
        "plum": "#dda0dd",
        "powderblue": "#b0e0e6",
        "purple": "#800080",
        "rebeccapurple": "#663399",
        "red": "#ff0000",
        "rosybrown": "#bc8f8f",
        "royalblue": "#4169e1",
        "saddlebrown": "#8b4513",
        "salmon": "#fa8072",
        "sandybrown": "#f4a460",
        "seagreen": "#2e8b57",
        "seashell": "#fff5ee",
        "sienna": "#a0522d",
        "silver": "#c0c0c0",
        "skyblue": "#87ceeb",
        "slateblue": "#6a5acd",
        "slategray": "#708090",
        "slategrey": "#708090",
        "snow": "#fffafa",
        "springgreen": "#00ff7f",
        "steelblue": "#4682b4",
        "tan": "#d2b48c",
        "teal": "#008080",
        "thistle": "#d8bfd8",
        "tomato": "#ff6347",
        "turquoise": "#40e0d0",
        "violet": "#ee82ee",
        "wheat": "#f5deb3",
        "white": "#ffffff",
        "whitesmoke": "#f5f5f5",
        "yellow": "#ffff00",
        "yellowgreen": "#9acd32",
    }
    ```
    """

    def __init__(
        self,
        color: str | tuple[int, ...],
        mode="RGBA",
        size=(1, 1),
        fps=None,
        duration=None,
    ):
        data = Image.new(mode, size, color)  # type: ignore
        self.color = color
        self.mode = mode
        super().__init__(data, fps=fps, duration=duration)

    def __repr__(self):
        return f"""{self.__class__.__name__}(fps={self.fps}, size={self.size}, start={self.start}, end={self.end}, duration={self.duration}, color={self.color}, mode={self.mode}, id={hex(id(self))})"""

    def __str__(self):
        return f"""{self.__class__.__name__}(fps={self.fps}, size={self.size}, start={self.start}, end={self.end}, duration={self.duration}, color={self.color}, mode={self.mode})"""

    def set_size(self, size: tuple[int, int]):
        """
        Set the size of the video clip.

        Parameters:
        - size: tuple[int, int]
            New size of the video clip in pixels (width, height).

        Examples:
        1. Resize the video clip to 800x600:
        ```python
        color_clip.set_size((800, 600))
        ```
        """
        self.image = Image.fromarray(self.image).resize(size)
        self.size = size


class TextClip(Data2ImageClip):
    """
    A class representing a text clip to be used in video compositions.

    Parameters:
    - text (str): The text content to be displayed in the clip.
    - font_pth (None | str, optional): The file path to the TrueType font file (.ttf). If None, the default system font is used. Defaults to None.
    - font_size (int, optional): The font size for the text. Defaults to 20.
    - txt_color (str | tuple[int, ...], optional): The color of the text specified as either a string (e.g., 'white') or a tuple representing RGBA values. Defaults to (255, 255, 255, 0) (fully transparent white).
    - bg_color (str | tuple[int, ...], optional): The background color of the text clip, specified as either a string (e.g., 'black') or a tuple representing RGBA values. Defaults to (0, 0, 0, 0) (fully transparent black).
    - fps (float, optional): Frames per second of the video. If None, the value is inherited from the parent class. Defaults to None.
    - duration (float, optional): Duration of the video clip in seconds. If None, the value is inherited from the parent class. Defaults to None.

    Attributes:
    - font (PIL.ImageFont.FreeTypeFont): The font object used for rendering the text.
    - image (PIL.Image.Image): The image containing the rendered text.
    - fps (float): Frames per second of the video clip.
    - duration (float): Duration of the video clip in seconds.

    Example:
    ```python
    # Create a TextClip with custom text and styling
    text_clip = TextClip("Contribute to Vidiopy", font_size=30, txt_color='red', bg_color='blue', fps=24, duration=5.0)

    # Use the text clip in a video composition
    composition = CompositeVideoClip([other_clip, text_clip])
    composition.write_videofile("output.mp4", codec='libx264', fps=24)
    ```
    """

    def __init__(
        self,
        text: str,
        font_pth: None | str = None,
        font_size: int = 20,
        txt_color: str | tuple[int, ...] = (255, 255, 255, 0),
        bg_color: str | tuple[int, ...] = (0, 0, 0, 0),
        fps=None,
        duration=None,
    ):
        font = (
            ImageFont.truetype(font_pth, font_size)
            if font_pth
            else ImageFont.load_default(font_size)
        )

        bbox = font.getbbox(text)
        image_width, image_height = bbox[2] - bbox[0] + 20, bbox[3] - bbox[1] + 20
        image = Image.new("RGBA", (image_width, image_height), bg_color)  # type: ignore
        draw = ImageDraw.Draw(image)
        draw.text(
            (10, 10), text, font=font, align="center", fill=txt_color
        )  # type: ignore

        self.text = text
        self.font = font
        self.font_size = font_size
        self.txt_color = txt_color
        self.bg_color = bg_color

        super().__init__(image, fps=fps, duration=duration)

    def __repr__(self):
        return f"""{self.__class__.__name__}(fps={self.fps}, size={self.size}, start={self.start}, end={self.end}, duration={self.duration}, text={self.text}, font_size={self.font_size}, text_color={self.txt_color}, bg_color={self.bg_color}, id={hex(id(self))})"""

    def __str__(self):
        return f"""{self.__class__.__name__}(fps={self.fps}, size={self.size}, start={self.start}, end={self.end}, duration={self.duration}, text={self.text}, font_size={self.font_size}"""
