from flask import Flask, send_file, request
from rembg import remove
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

def processar_imagem(upload_file):
    img = Image.open(upload_file).convert('RGBA')
    imgRemove = remove(img)

    imagem_fundo_branco = Image.new("RGBA", img.size, (255, 255, 255))
    imagem_fundo_branco = Image.alpha_composite(imagem_fundo_branco, imgRemove)

    return imagem_fundo_branco

def processar_imagem_sem_fundo(upload_file):

    img = Image.open(upload_file).convert('RGBA')
    imgRemove = remove(img)

    return imgRemove


@app.route("/imagem-semfundo", methods=["POST"])
def endpoint_processar_imagem_sem_fundo():
    upload_file = request.files['file']

    filename = secure_filename(upload_file.filename)
    imagem_processada = processar_imagem_sem_fundo(upload_file)

    arquivo_temporario = f"imagem_processada_{filename}"
    imagem_processada.save(arquivo_temporario, "png")

    return send_file(arquivo_temporario, mimetype="image/png")

@app.route("/imagem-comfundo", methods=["POST"])
def endpoint_processar_imagem_com_fundo():
    upload_file = request.files['file']

    filename = secure_filename(upload_file.filename)
    imagem_processada = processar_imagem(upload_file)

    # Salvar a imagem processada temporariamente
    arquivo_temporario = "imagem_processada.png"
    imagem_processada.save(arquivo_temporario, "png")

    return send_file(arquivo_temporario, mimetype="image/png")


if __name__ == '__main__':
    app.run(debug=True, port=8000)