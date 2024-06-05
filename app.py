from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from src.pipelines.predict_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def prediction():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        # Validate the incoming data
        try:
            gender = request.form.get('gender')
            race_ethnicity = request.form.get('race_ethnicity')
            parental_level_of_education = request.form.get('parental_level_of_education')
            lunch = request.form.get('lunch')
            test_preparation_course = request.form.get('test_preparation_course')
            reading_score = float(request.form.get('reading_score'))
            writing_score = float(request.form.get('writing_score'))
            
            # Check for any None values
            if None in [gender, race_ethnicity, parental_level_of_education, lunch, test_preparation_course, reading_score, writing_score]:
                raise ValueError("All form fields must be filled out.")

            data = CustomData(
                gender=gender,
                race_ethnicity=race_ethnicity,
                parental_level_of_education=parental_level_of_education,
                lunch=lunch,
                test_preparation_course=test_preparation_course,
                reading_score=reading_score,
                writing_score=writing_score,
            )
            pred_df = data.get_data_as_data_frame()
            print(pred_df)

            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            return render_template('home.html', results=results[0])

        except ValueError as ve:
            return render_template('home.html', results=str(ve))

        except Exception as e:
            return render_template('home.html', results="An error occurred during prediction. Please try again.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
