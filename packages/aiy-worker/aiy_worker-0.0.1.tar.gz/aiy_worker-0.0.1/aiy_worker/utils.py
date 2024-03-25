import base64

def encode_image(file: str) -> str:
    """将图片编码为 Base64"""
    with open(file, 'rb') as f:
        return base64.encodebytes(f.read()).decode('utf8').replace('\n', '').replace('\r', '')

if __name__ == '__main__':
    print(encode_image('assets/demo.png'))
