from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

# Assuming your datasets are named 'baseline.csv' and 'modal.csv' and located in the 'data' directory
DATA_DIR = 'data'
BASELINE_FILE = 'baseline.csv'
MODAL_FILE = 'modal.csv'

@app.route('/')
def index():
    df = pd.read_excel('Variable Definitions.xlsx')
    headers = df.iloc[0]  # Get the first row, which contains your headers
    return render_template('index.html', headers=headers.to_dict())

@app.route('/process-selection', methods=['POST'])
def process_selection():
    # Retrieve form data
    data_file_type = request.form.get('Variable Definitions.xlsx')
    # Load the appropriate dataset
    if data_file_type == 'baseline':
        df = pd.read_csv(os.path.join(DATA_DIR, BASELINE_FILE))
    elif data_file_type == 'modal':
        df = pd.read_csv(os.path.join(DATA_DIR, MODAL_FILE))
    
    # Add your data cleaning methods here
    # ...


    # Generate the CSV file to download
    output_file_path = os.path.join(DATA_DIR, 'output.csv')
    df.to_csv(output_file_path, index=False)

    # Return the file for download
    return send_file(output_file_path, as_attachment=True)

@app.route('/first-row')
def show_first_row():
    df = pd.read_excel('Variable Definitions.xlsx')
    first_row_dict = df.iloc[0].to_dict()
    return jsonify(first_row_dict)



if __name__ == '__main__':
    app.run(debug=True)
