from io import BytesIO
from PIL import Image
from iv2 import ResNet

resnet: ResNet = ResNet(
    runtime_model='models/gl18-tl-resnet50-gem-w-83fdc30.pth',
    device='cpu'
)
# from PIL import ImageFile
# ImageFile.LOAD_TRUNCATED_IMAGES = True


def create_vector(file: BytesIO | bytes) -> list[float]:
    if isinstance(file, bytes):
        file = BytesIO(file)
    image = Image.open(file)
    image = image.convert('RGB')
    vector = resnet.gen_vector(image)
    return vector


def distance_2_score(distance: float, threshold: float = 0.5) -> float:
    return (threshold-distance)/threshold*100
