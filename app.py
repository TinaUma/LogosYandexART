from flask import Flask, request, render_template
import os
from logo_generator import generate_logo

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    error = None
    form_data = {"forma": "", "style": "", "description": ""}  # Значения по умолчанию

    if request.method == "POST":
        forma = request.form.get("forma")
        style = request.form.get("style")
        description = request.form.get("description")
        # Сохраняем введённые данные
        form_data = {"forma": forma, "style": style, "description": description}

        if forma and style and description:
            image_path = generate_logo(forma, style, description)
            if image_path and "Ошибка" not in image_path:
                image_url = "/" + image_path
            else:
                error = image_path if image_path else "Не удалось сгенерировать логотип"
                print(error)
        else:
            error = "Заполните все поля"

    return render_template("index.html", image=image_url, error=error, form_data=form_data)

if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)