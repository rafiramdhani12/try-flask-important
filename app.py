from flask import Flask,render_template,request,send_file
from rembg import remove
import os

app = Flask(__name__) # ! mencerminkan semua yg ada di flask

# Folder untuk menyimpan file sementara
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/")
def main():
    web_title = "background remover"
    # ! parameter pertama untuk render file utama yg ke 2 untuk variable / data apa yg ingin di pharsing
    return render_template('index.html',web_title=web_title)

@app.route("/edit_photo", methods=["POST"])
def edit_photo():
    try:
        # ! validasi file yg akan diunggah
        if "image" not in request.files:
            return "Tidak ada file yang diunggah.", 400

        file = request.files["image"]
        if file.filename == "":
            return "Nama file tidak valid.", 400

        # ! Simpan file sementara
        input_filename = file.filename
        input_path = os.path.join(UPLOAD_FOLDER, input_filename)
        file.save(input_path)

        with open(input_path, "rb") as input_file:
            input_data = input_file.read()
            output_data = remove(input_data)

        # ! Simpan file di direktori processed
        output_filename = f"processed_{input_filename}"
        output_path = os.path.join(PROCESSED_FOLDER, output_filename)
        with open(output_path, "wb") as output_file:
            output_file.write(output_data)

        # ! kirim file ke user 
        return send_file(
            output_path,  
            as_attachment=True,
            download_name=output_filename
        )

    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}", 500

@app.route("/about")
def about():
    web_title = "about page"
    return render_template("about.html",web_title=web_title)

@app.route("/usia",methods=["GET","POST"])
def cek_usia():
    web_title = "page usia"
    
    
    if request.method == "POST":
        tahun_lahir = int(request.form['tahun_lahir'])
        tahun_sekarang = 2024
        usia = tahun_sekarang - tahun_lahir
        return render_template("usia.html",usia = usia)
        
        
    return render_template("usia.html" , web_title = web_title , usia=None)

if __name__ == "__main__":
    app.run(debug=True)

