import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
import json
import time


# Función para verificar si hay cambios en la hoja de cálculo
def check_for_changes(worksheet, previous_data):
    current_data = worksheet.get_all_values()
    if current_data != previous_data:
        return True, current_data
    else:
        return False, previous_data

# Obtén el contenido de las credenciales desde la variable de entorno
credentials_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS")

# Verifica si se obtuvo correctamente el contenido de las credenciales
if credentials_json:
    # Carga las credenciales como un diccionario
    credentials_dict = json.loads(credentials_json)
    
    # Define el alcance de acceso
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Autoriza con las credenciales y el alcance
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(credentials)
    
    # ID de la hoja de cálculo
    spreadsheet_id = "1BQlvQyqoV08sEcHGgfFqL7OqCjSUZJZc8Pz_tWqdOIo"
    
    # Abrir la hoja de cálculo por su ID
    spreadsheet = client.open_by_key(spreadsheet_id)
    
    # Seleccionar una hoja por su nombre
    worksheet = spreadsheet.worksheet("Hoja 1")

    # Agarro una columna y le saco la longitud
    colum_list = worksheet.col_values(1)
    cant_filas = len(colum_list)

    for fila in range(1, (cant_filas+1)):
      print(worksheet.row_values(fila))

    previous_data = worksheet.get_all_values()

    while True:
        # Verifica cambios en la hoja de cálculo
        changes_detected, current_data = check_for_changes(worksheet, previous_data)
        if changes_detected:
            ruta_archivo = "datos.json"
            with open(ruta_archivo, "w") as archivo:
                json.dump(current_data, archivo, indent=4)
                print(f"Se ha creado/reescrito el archivo {ruta_archivo}")
            previous_data = current_data
  
            # Subir el archivo JSON a Amazon S3 utilizando el comando de la terminal
            os.system("aws s3 cp datos.json s3://pythonspreadsheets/datos.json")
          
          # Espera antes de volver a verificar
        time.sleep(2)  # Espera 2 segundos antes de la siguiente verificación
  
else:
    print("No se pudo obtener el contenido de las credenciales.")