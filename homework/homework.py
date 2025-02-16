"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
import os
import zipfile
import pandas as pd

def process_zip(zip_path):
    """Lee un archivo ZIP y devuelve un DataFrame con los datos concatenados."""
    dataframes = []
    with zipfile.ZipFile(zip_path, "r") as z:
        for csv in z.namelist():
            with z.open(csv) as f:
                dataframes.append(pd.read_csv(f))
    return pd.concat(dataframes, ignore_index=True) if dataframes else None


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    input_path = "files/input/"
    output_path = "files/output/"
    os.makedirs(output_path, exist_ok=True)

    # Eliminar archivos existentes en output
    for file in ["client.csv", "campaign.csv", "economics.csv"]:
        file_path = os.path.join(output_path, file)
        if os.path.exists(file_path):
            os.remove(file_path)

    # Obtener archivos ZIP
    zip_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".zip")]
    
    # Leer y concatenar datos
    dataframes = [process_zip(zip_file) for zip_file in zip_files if process_zip(zip_file) is not None]
    if not dataframes:
        raise ValueError("No se encontraron archivos de datos válidos en los ZIPs.")
    df = pd.concat(dataframes, ignore_index=True)
    
    # Procesar client.csv
    client_df = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    client_df["job"] = client_df["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client_df["education"] = client_df["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    client_df["credit_default"] = client_df["credit_default"].map(lambda x: 1 if x == "yes" else 0)
    client_df["mortgage"] = client_df["mortgage"].map(lambda x: 1 if x == "yes" else 0)
    client_df.to_csv(os.path.join(output_path, "client.csv"), index=False)
    
    # Procesar campaign.csv
    campaign_df = df[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "day", "month"]].copy()
    campaign_df["previous_outcome"] = campaign_df["previous_outcome"].map(lambda x: 1 if x == "success" else 0)
    campaign_df["campaign_outcome"] = campaign_df["campaign_outcome"].map(lambda x: 1 if x == "yes" else 0)
    campaign_df["last_contact_date"] = pd.to_datetime("2022-" + campaign_df["month"] + "-" + campaign_df["day"].astype(str), format="%Y-%b-%d", errors="coerce")
    campaign_df.drop(columns=["day", "month"], inplace=True)
    campaign_df.to_csv(os.path.join(output_path, "campaign.csv"), index=False)
    
    # Procesar economics.csv
    economics_df = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    economics_df.to_csv(os.path.join(output_path, "economics.csv"), index=False)
    

if __name__ == "__main__":
    clean_campaign_data()
