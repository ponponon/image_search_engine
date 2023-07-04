from PIL import Image
from PIL.Image import Image as PIL_Image
import io


def png_stream_2_png_image(png_stream: bytes) -> PIL_Image:
    file_like_obj = io.BytesIO(png_stream)

    png_image = Image.open(file_like_obj)
    return png_image


def png_image_2_jpg_stream(png_image: PIL_Image, quality=100) -> bytes:
    assert png_image.format == 'PNG'
    file_like_obj = io.BytesIO()
    png_image = png_image.convert('RGB')  # PNG 是 RGBA，多了一个透明通道，JPG不支持透明通道
    png_image.save(file_like_obj, format='JPEG', quality=quality)
    stream = file_like_obj.getvalue()
    return stream


def png_stream_2_jpg_stream(png_stream: bytes, quality=100) -> bytes:
    """
    png_stream into png_imgae
    png_imgae into jpg_stream
    """
    png_image = png_stream_2_png_image(png_stream)
    jpg_stream = png_image_2_jpg_stream(png_image, quality)
    return jpg_stream


def png_image_2_png_stream(png_image: PIL_Image) -> bytes:
    assert png_image.format == 'PNG'
    file_like_obj = io.BytesIO()
    png_image.save(file_like_obj, format='PNG')
    stream = file_like_obj.getvalue()
    return stream
