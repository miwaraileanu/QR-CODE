import openai
import qrcode
from PIL import Image
import requests

# add your openAI API key here !!!
openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_image(prompt: str, filename: str = "ai_image.png") -> str:
    print("Image generating...")
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response["data"][0]["url"]
    

    img_data = requests.get(image_url).content
    with open(filename, "wb") as f:
        f.write(img_data)

    print(f"Image save in: {filename}")
    return filename

def generate_custom_qr(data: str, logo_path: str, qr_color="#FFD700", bg_color="#000000", output="qr_with_ai.png"):
    print("QR-Code Generating...")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert('RGB')

    try:
        logo = Image.open(logo_path)

        basewidth = img.size[0] // 4
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
    except Exception as e:
        print(f"Error adding to logo: {e}")

    img.save(output)
    print(f"✅ QR-Code SAved: {output}")

def main():
    print("=== AI QR Code Generator ===\n")
    prompt = input("Enter a description for the image: ")
    qr_data = input("Enter the link or text for the QR code: ")

    image_path = generate_image(prompt)
    generate_custom_qr(qr_data, logo_path=image_path)

if __name__ == "__main__":
    main()
