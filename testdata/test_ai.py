from PIL import Image
import matplotlib.pyplot as plt
from utils.ai import AImodule


def test_ai_module():
    image_path = "testdata/italy_train2.webp"
    image = Image.open(image_path)
    plt.imshow(image)
    plt.axis('off')
    plt.show()
    ai_module = AImodule()  # AImodule 인스턴스 생성
    with open(image_path, "rb") as image:
        result = ai_module.analyze_image(image)  # 인스턴스를 통해 메서드 호출
    print(result)