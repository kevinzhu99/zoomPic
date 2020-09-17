from flask import Flask
from flask import render_template, url_for, request, redirect
import os
from PIL import Image

app = Flask(__name__)

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))							#getting the image path

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/form', methods = ['GET', 'POST'])
def form():
	if request.method == 'POST':
		length = request.form['length']
		base = request.form['base']
		height = request.form['height']
		width = request.form['width']
	
	return render_template('display.html', length=length, base=base, height=height, width=width)

@app.route("/picture")
def picture():
	return render_template("upload.html")

@app.route("/upload", methods = ['POST'])
def upload():
	target = os.path.join(APP_ROUTE, 'static/')									#uploading into a directory called static
	print(target)


	if not os.path.isdir(target):
		os.mkdir(target)

	else:
		print("Couldn't create the directory: {}" .format(target))
	print(request.files.getlist("file"))


	for file in request.files.getlist("file"):
		print(file)
		filename = file.filename
		destination = "/".join([target, filename])
		print(destination)
		file.save(destination)
		picImage = Image.open(destination)
		width, height = picImage.size


	return render_template("complete.html", image_name = filename, width=width, height=height)

#@app.route("/editImage")
#def editImage():

	

@app.route("/gallery")
def get_gallery():
	image_names = os.listdir('./static')
	print(image_names)
	return render_template("gallery.html", image_names = image_names)

if __name__ == '__main__':
	app.run()           