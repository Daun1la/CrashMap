import psycopg2
import os
import pandas as pd
import numpy as np
from config import host, user, password, db_name, folder_path
from flask import Flask, render_template_string
import folium

# Initialization
folder_path = folder_path
data_to_insert = []
descrip_value =''
level_value = 0
exp_value = 0
search_value_1 = 'Марка/модель ТС'
search_value_2 = 'Год выпуска'
count = 0
data_to_insert = []

#Check all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xls'):  # Check Excel-file
        file_path = os.path.join(folder_path, file_name)
        xl = pd.ExcelFile(file_path)

        # Check all lists in file
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Looking for a cell that satisfies the condition  
            for index, value in df.iloc[:, 0].items():
                Date_value = df.iloc[1,1]
                Time_value = df.iloc[1,3]
                type_value = df.iloc[3,3]
                value1 = df.iloc[2, 1]
                value2 = df.iloc[2, 3]
                    
                if value == 'Состояние проезжей части:':
                   cond_value = df.iloc[index, 1]
                          
                if value == search_value_1:
                    count += 1
                    model_value = df.iloc[index, 1] if  df.iloc[index, 1] != ' ' else 'N/A'
                    RY_value = 0 if pd.isna(df.iloc[(index-1), 5])  else pd.to_numeric(df.iloc[(index-1), 5], errors='coerce').astype(int)
                    data_to_insert.append({
                            'Date': Date_value, 
                            'Time': Time_value, 
                            'x_coord': value1,
                            'y_coord': value2,
                            'Type': type_value, 
                            'Model': model_value, 
                            'RY' : RY_value, 
                            'Cond_of_Road': cond_value})

                if value == 'Степень опьянения':
                    data_to_insert[count-1]['Desc'] = '-' if pd.isna(df.iloc[index+2, 1]) else df.iloc[index+2, 1]
                    data_to_insert[count-1]['Level'] = 0 if pd.isna(df.iloc[index, 1]) else int(pd.to_numeric(df.iloc[index, 1], errors='coerce'))
                    data_to_insert[count-1]['Exp'] = np.nan_to_num(pd.to_numeric(df.iloc[index-2, 5], errors = 'coerce')).astype(int)

# There may not be all fields in the source tables, so re-checking
for data in data_to_insert:
    if 'Desc' not in data:
        data['Desc'] = 'N/A'  
    if 'Level' not in data:
        data['Level'] = 0      
    if 'Exp' not in data:
        data['Exp'] = 0   

# Uncomment this section if you want connect to PostgreSQL
# try:
#     connection = psycopg2.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=db_name
#     )
    
#     connection.autocommit = True
    
#     # Creating table 'dtp'
#     # with connection.cursor() as cursor:
#     #     cursor.execute(
#     #         """CREATE TABLE dtp(
#     #             id serial PRIMARY KEY,
#     #             Date date,
#     #             Time time,
#     #             x_coord float,
#     #             y_coord float,
#     #             type varchar(50),
#     #             Description varchar(500),
#     #             Intoxication int,
#     #             Driving_exp int,
#     #             Model varchar(100),
#     #             RY int,
#     #             Cond_of_road varchar(50)
#     #         )
#     #         """
#     #     )     
#     #     print("[INFO] Table was created")
                  
#     #Creating and executing a database query
#     with connection.cursor() as cursor:
#         insert_query = '''INSERT INTO DTP (Date, Time, x_coord, y_coord, Type, Description, Intoxication, Driving_exp, Model, RY, Cond_of_Road)
#         VALUES (to_date(%s, 'DD/MM/YYY'), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
#         for data in data_to_insert:
#             cursor.execute(insert_query, (
#                 data['Date'], 
#                 data['Time'], 
#                 data['x_coord'],
#                 data['y_coord'],  
#                 data['Type'],
#                 data['Desc'],
#                 data['Level'],
#                 str(data['Exp']),
#                 data['Model'], 
#                 str(data['RY']), 
#                 data['Cond_of_Road']))

#     #Clear table
#     # with connection.cursor() as cursor:
#     #     cursor.execute(
#     #         "DELETE FROM dtp")
           
#     #     print("[INFO] Table was cleared")
    
#     #Drop table
#     # with connection.cursor() as cursor:
#     #     cursor.execute(
#     #         "DROP TABLE dtp")
           
#     #     print("[INFO] Table was dropped")
    
# except Exception as _ex:
#     print("[INFO] Error while working with PostgereSQL", _ex)
# finally:
#     if connection:
#         connection.close()
#         print("[INFO] PostgereSQL connection closed")
        
# create a flask application
app = Flask(__name__)

@app.route("/")
def home():
    """Create a map object"""
    mapObj = folium.Map(location=[data_to_insert[0]['x_coord'], data_to_insert[0]['y_coord']],
                        zoom_start=8, width=1860, height=960)

    # add a marker to the map object
    for c in data_to_insert:
        popup_text = f"<b>Дата:</b> {c['Date']}<br><b>Время:</b> {c['Time']}<br><b>Происшествие:</b> {c['Type']}<br><b>Описание:</b> {c['Desc']}<br><b>Модель:</b> <i>{c['Model']}</i><br><b>Год выпуска:</b> {c['RY']}<br><b>Покрытие:</b> {c['Cond_of_Road']}"
        folium.Marker([float(c['x_coord']), float(c['y_coord'])], popup=folium.Popup(popup_text, max_width=200)).add_to(mapObj)

    # render the map object
    mapObj.get_root().render()

    # Get component to insert in HTML
    header = mapObj.get_root().header.render()
    body_html = mapObj.get_root().html.render()
    script = mapObj.get_root().script.render()

    # return a web page with folium map components embeded in it. You can also use render_template.
    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head>
                    {{ header|safe }}
                </head>
                <body>
                    <div style="position: fixed; top: 20px; right: 20px; background-color: #f2f2f2; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-family: Arial, sans-serif; font-size: 14px; color: #333; z-index: 1000;">
                        <p style="margin: 0;">При отсутствии данных в поле Год выпуска ставится 0</p>
                    </div>
                    <div id="map" style="height: 100%; width: 100%;"></div>
                    {{ body_html|safe }}
                    <script>
                        {{ script|safe }}
                    </script>
                </body>
            </html>
        """,
        header=header,
        body_html=body_html,
        script=script,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50100, debug=True)
