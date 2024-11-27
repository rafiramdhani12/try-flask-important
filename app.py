from flask import Flask,render_template,request,send_file
from rembg import remove
import os


konversi = {
    "1" : {"celcius": lambda x : {"fahrenheit" : (x * 9/5) +32 , "kelvin" : x + 273.15 , "reamur" : 4/5 * x}},
    "2" : {"fahrenheit": lambda x : {"celcius" : (x - 32) * 5/9 , "kelvin" : (x - 32 ) * 5/9 + 273.15 , "reamur" : (x - 32) * 4/5 }},
    "3" : {"kelvin": lambda x : {"celcius" : x - 273.15 , "fahrenheit" : (x - 273.15) * 5/9 + 32 , "reamur" :(x - 273.15) * 4/5  }},
    "4" : {"reamur": lambda x : {"celcius" : x * 5/4 , "kelvin" : (x * 5/4) + 273.15 , "fahrenheit" : (x * 5/4) + 32}},
}


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

@app.route("/calculator",methods=["GET","POST"])
def calculator():
    web_tile = "calculator"
    result = None
    
    if request.method == "POST":
        try:
            angka1 = int(request.form["angka1"])
            angka2 =  int(request.form["angka2"])
            operation = request.form["operation"]
        
            if operation == "+":
                result = angka1 + angka2
            elif operation == "-":
                result = angka1 - angka2
            elif operation == "*":
                result = angka1 * angka2
            elif operation == "/":
                result = angka1 / angka2 if angka2 != 0 else "Error : division by zero" 
            else:
                print("invalid operation")
        except ValueError:
            result = "error : invalid input"
        
    return render_template("calculator.html",web_title=web_tile,result=result)



@app.route("/derajat" , methods = ["GET","POST"])
def convert():
    result = None
    
    if request.method == "POST":
        try:
            data_input = request.form["konversi"]
            nilai_suhu = float(request.form["nilai_suhu"])
            
            if data_input in konversi:
                suhu, fungsi_konversi = list(konversi[data_input].items())[0]
                hasil = fungsi_konversi(nilai_suhu)
                
                result = {f"{suhu} ke {satuan}":nilai for satuan,nilai in hasil.items()}
            else:
                print("pilihan tidak valid")
                
        except ValueError:
            result = "error : invalid input"
            
    return render_template("derajat.html", result = result)

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

