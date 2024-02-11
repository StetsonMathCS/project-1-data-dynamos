from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

def read_excel_and_categorize(file_path):
    df = pd.read_excel(file_path, header=None)
    
    # Descriptions are assumed to be in row 3 (index 2)
    descriptions_row = df.iloc[2]
    
    target_row_index = df.apply(lambda row: row.astype(str).str.contains('Label for Website').any(), axis=1).idxmax()
    
    ranges = {
        'Identifying Variables': (1, 8),
        'Eye Movement Data': (9, 52),
        'Lexical Variables': (53, 85),
        'Individual Differences': (86, 119),
    }

    categorized_data = {}
    for category, (start_idx, end_idx) in ranges.items():
        variables = df.iloc[target_row_index, start_idx:end_idx + 1].dropna().values.tolist()
        descriptions = descriptions_row[start_idx:end_idx + 1].values.tolist()
        categorized_data[category] = list(zip(variables, descriptions))

    return categorized_data

@app.route('/')
def index():
    file_path = 'Variable Definitions.xlsx'  # Adjust the path accordingly
    headers_parts = read_excel_and_categorize(file_path)
    return render_template('index.html', headers_parts=headers_parts)

@app.route('/process-selection', methods=['POST'])
def process_selection():
    selected_variables = request.form.getlist('variables')
    print("Selected Variables:", selected_variables)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
