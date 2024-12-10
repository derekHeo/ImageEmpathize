from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from openai import OpenAI
import ollama

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

os.environ["OPENAI_API_KEY"] = "your-api"
model_gpt = "gpt-4o-mini"
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def generate_caption(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

def generate_warm_message(caption):
    prompt = f"""
    당신은 사용자에게 공감하고 위로를 제공하는 역할을 맡았습니다.당신의 공감의 말로 사용자의 하루를 더 기분 좋고 풍성하게 만들어 줄 겁니다.
    아래의 입력(사진 설명)을 보고 따뜻한 공감이나 칭찬, 위로를 담은 메시지를 생성해주세요.
    반드시 한국어로 답변해야합니다.

    ### 예시
    입력: "a dog playing with a ball in a park"
    출력: "사진 속 강아지가 공원에서 신나게 공놀이를 하고 있네요! 오늘도 즐겁고 활기찬 하루 되세요~"

    입력: "a sunset over a mountain range"
    출력: "산맥 위로 지는 아름다운 노을이 정말 멋져요. 오늘 하루도 이 노을처럼 따뜻하고 평온하길 바랍니다."

    입력: "a group of friends sitting around a campfire"
    출력: "캠프파이어 주위에 친구들과 함께한 추억이 느껴지네요! 소중한 순간처럼 행복한 날이 가득하길 바랄게요~"

    ### 요청
    입력: "{caption}"
    출력:
    """

    response = client.chat.completions.create(
        model=model_gpt,
        messages=[
            {"role": "system", "content": "You are an assistant that empathize user's image captions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def generate_warm_message_ollama(caption):
    prompt = f"""
    당신은 사용자에게 공감하고 위로를 제공하는 역할을 맡았습니다. 당신의 공감의 말로 사용자의 하루를 더 기분 좋고 풍성하게 만들어 줄 겁니다.
    아래의 입력(사진 설명)을 보고 따뜻한 공감이나 칭찬, 위로를 담은 메시지를 생성해주세요.
    반드시 한국어로 답변해야합니다. 문장 길이는 50토큰 이내로 해주세요.

    ### 예시
    입력: "a dog playing with a ball in a park"
    출력: "강아지가 공원에서 신나게 공놀이를 하고 있네요! 오늘도 즐겁고 활기찬 하루 되세요~"

    입력: "a sunset over a mountain range"
    출력: "산맥 위로 지는 아름다운 노을이 정말 멋져요. 오늘 하루도 이 노을처럼 따뜻하고 평온하길 바랍니다."

    입력: "a group of friends sitting around a campfire"
    출력: "캠프파이어 주위에 친구들과 함께한 추억이 느껴지네요! 소중한 순간처럼 행복한 날이 가득하길 바랄게요~"

    ### 요청
    입력: "{caption}"
    출력:
    """

    response = ollama.chat(model='ollama-ko-0710', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    return response['message']['content']

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "" or not allowed_file(file.filename):
            return redirect(request.url)

        # 파일 저장 -> result에서 불러와서 사용하기 위함.
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        caption = generate_caption(file_path)
        #여기서 모델 변경 가능함 - ollama/gpt
        warm_message = generate_warm_message(caption)

        return render_template("result.html", image_url=url_for("static", filename=f"uploads/{filename}"),
                               caption=caption, warm_message=warm_message)
    return render_template("index.html")

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

if __name__ == "__main__":
    app.run(debug=True)
