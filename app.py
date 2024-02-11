from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def read_excel_and_categorize(file_path):
    df = pd.read_excel(file_path, header=None)
    
    categorized_data = {}
    
    main_categories = df.iloc[8].fillna(method='ffill')  # Row 9 in Excel, fill forward NaN values
    sub_categories = df.iloc[9]  # Row 10 in Excel
    descriptions_row = df.iloc[2]  # Descriptions in Row 3

    for col in range(df.shape[1]):  # Iterate over DataFrame columns
        main_cat = main_categories[col]
        sub_cat = sub_categories[col]
        variable = df.iloc[0, col]  # Assuming the first row contains variable names
        description = descriptions_row[col]
        
        # Skip if no main category or variable name or if the main category is "Category of Variable"
        if pd.isnull(main_cat) or pd.isnull(variable) or main_cat == "Category of Variable":
            continue
        
        # Initialize nested dictionaries for categories and subcategories
        if main_cat not in categorized_data:
            categorized_data[main_cat] = {}
        if sub_cat not in categorized_data[main_cat]:
            categorized_data[main_cat][sub_cat] = []
        
        # Append variable and description to the appropriate subcategory list
        categorized_data[main_cat][sub_cat].append((variable, description))

    return categorized_data

@app.route('/collect-data', methods=['POST'])
def collect_data():
    data = request.json.get('data', [])
    
    # Create a DataFrame with the selected data
    df = pd.DataFrame(data, columns=['Selected Variables'])
    
    # Write the DataFrame to a new Excel file
    output_file = 'selected_variables.xlsx'
    df.to_excel(output_file, index=False)
    
    return jsonify({'message': 'Data collected and saved to ' + output_file})


@app.route('/')
def index():
    file_path = 'Variable Definitions.xlsx'  # Update this to the actual path of your Excel file
    headers_parts = read_excel_and_categorize(file_path)
    
    return render_template('index.html', headers_parts=headers_parts)

if __name__ == '__main__':
    app.run(debug=True)
