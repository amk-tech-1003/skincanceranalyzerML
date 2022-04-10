from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import pandas as pd

app = Flask(__name__)

dic = {0:'akiec', 1:'bcc', 2:'bkl', 3:'df', 4:'mel',5: 'noncancer',6:'nv',7:'random', 8:'vasc'}
prec = {0:['Applying sunscreen every day, even in cloudy weather or during winter, and re-applying often', 'Avoiding sun exposure when UV light is most intense, between 10 a.m. and 2 p.m.','Avoiding tanning salons, sun lamps and tanning beds.', 'Wearing sun-safe clothing, such as long-sleeved shirts, long pants and hats.'], 
1:['Avoid the sun during the middle of the day.', 'Wear sunscreen year-round.', 'Avoid tanning beds.', 'Check your skin regularly and report changes to your doctor.'], 
2:['Use a broad-spectrum (UVA/UVB) sunscreen', 'See a dermatologist', 'Examine your skin', 'Cover up with clothing, hat and UV-blocking sunglasses.'], 
3:['checked out by a doctor', 'may also take a tiny tissue sample, called a biopsy, to examine under a microscope.', 'You can leave it alone, or get it removed.'], 
4:['protect yourself from exposure to UV rays.','Avoid using tanning beds and sunlamps', 'Watch for abnormal moles', 'Avoid weakening your immune system'],
5: ['Non-Cancerous'],
6:['limiting exposure to sunlight and using sunscreens','Light-skinned persons should limit sun exposure', 'particularly important for children and teenagers', 'people can take to limit ultraviolet light exposure.'],
7:['Radom Image'], 
8:['Make healthy lifestyle changes', 'Dont smoke', 'Keep your blood pressure and cholesterol in check', 'If you have diabetes, control your blood sugar']}
model = load_model('model_94_9.h5')

model.make_predict_function()

def predict_label(img_path):
	i = image.load_img(img_path, target_size=(32,32))
	i = image.img_to_array(i)/255.0
	i = i.reshape(1, 32,32,3)
	p =  np.argmax(model.predict(i),axis=1)
	return dic[p[0]], prec[p[0]]


#home page 
@app.route('/')
def home():
    return render_template('base.html')

# routes
@app.route("/predicts", methods=['GET', 'POST'])
def pred():
	return render_template("predictcancer.html")


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']
		img_path = "static/" + img.filename	
		img.save(img_path)
		p,pr = predict_label(img_path)

	return render_template("predictcancer.html", prediction = p, precaution = pr, img_path = img_path)

@app.route('/nearbyareas',  methods=['GET', 'POST'])
def areas():
	return render_template("nearby.html")

@app.route("/submitcity", methods=['GET', 'POST'])
def city_output():
    if request.method == 'POST':
        c= request.form['city']
        doc_data = 'doctors_data.xlsx'
        df = pd.read_excel(doc_data)
        print(df)
        r = df[['Details']].where(df['City']==c).dropna()
        print(c)
        #print(r['Name'])

    return render_template("nearby.html", names=r['Details'])

@app.route("/services")
def services():
	return render_template("services.html")

@app.route("/research")
def research():
	return render_template("research.html")

@app.route("/about")
def about():
	return render_template("aboutus.html")

@app.route("/contact")
def contact():
	return render_template("contactus.html")

@app.route("/types")
def types():
	return render_template("types.html")
if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)