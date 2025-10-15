# load SaludMental.csv
import pandas as pd



def parse_fecha_intervencion(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return None
    try:
        # Asegura longitud y formato correcto
        valor = str(valor).strip()
        return datetime.strptime(valor, "%d%m%Y %H%M").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        # Si hay errores (por ejemplo formato inesperado)
        return None





















df = pd.read_csv('SaludMental.csv')
# limit to 10 rows for testing
df = df.head(1000)


# Drop columns with in which all values are NaN
df = df.dropna(axis=1, how='all')

print("##########Head:\n", df.head())
print("##########Info:\n", df.info())
print("##########Describe:\n", df.describe())
print("##########Columns:\n", df.columns)
print("##########Shape:\n", df.shape)

# Save cleaned data to a new CSV file
df.to_csv('SaludMental_cleaned.csv', index=False)

## Add other tables first

# tipos poa
sexos = {1: "Varon", 2: "Mujer", 3: "Indeterminado", 9: "No específicado"}
comunidades = {n: i+1 for i, n in enumerate(df["Comunidad Autónoma"].dropna().unique())}
circunstancias = {1:"No Programado", 2:"Programado", 9:"Desconocido"}

###no verificados
tipos_alta = {1:"Alta voluntaria", 2:"Alta médica", 3:"Alta a otro centro", 4:"Fallecimiento", 5:"Otro", 9:"Desconocido"}

print("##########Sexos:\n", sexos)
print("##########Comunidades:\n", comunidades)



paciente_rows = []
for _, r in df.iterrows():
    paciente_rows.append({
        "comunidad_autonoma_id": comunidades.get(r["Comunidad Autónoma"]),
        "nombre": r["Nombre"],
        "fecha_nacimiento": pd.to_datetime(r["Fecha de nacimiento"],format="%m/%d/%Y", errors="coerce") if pd.notna(r["Fecha de nacimiento"]) else None,
        "sexo_id": r["Sexo"],
        "fecha_ingreso": pd.to_datetime(r["Fecha de Ingreso"], format="%d/%m/%Y", errors="coerce") if pd.notna(r["Fecha de Ingreso"]) else None,
        "circunstancia_contacto_id": r["Circunstancia de Contacto"],
        "fecha_fin_contacto": pd.to_datetime(r["Fecha de Fin Contacto"], format="%d/%m/%Y", errors="coerce") if pd.notna(r["Fecha de Fin Contacto"]) else None,
        "tipo_alta_id": r["Tipo Alta"],
        "estancia_dias": r["Estancia Días"],
        "fecha_intervención": pd.to_datetime(r["Fecha de Intervención"], format="%d%m%Y %H%M", errors="coerce") if pd.notna(r["Fecha de Intervención"]) else None,
        "GRD_APR": r["GRD APR"],
        "CDM_APR": r["CDM APR"],
        "nivel_severidad": r["Nivel Severidad APR"],
        "riesgo_mortalidad_APR": r["Riesgo Mortalidad APR"],
        "servicio_id": r["Servicio"],
        "edad": r["Edad"],
        "coste_APR": r["Coste APR"],
        "CIE": r["CIE"],
        "num_registro_anual": r["Número de registro anual"],
        "centro_recod": r["Centro Recodificado"],
        "CIP_SNS_recod": r["CIP SNS Recodificado"],
        "pais_nacimiento_id": r["País Nacimiento"],
        "pais_residencia_id": r["País Residencia"],
        "fecha_inicio_contacto": pd.to_datetime(r["Fecha de Inicio contacto"], format="%d/%m/%Y", errors="coerce") if pd.notna(r["Fecha de Inicio contacto"]) else None,
        "regimen_finalizacion": r["Régimen Financiación"],
        "procedencia_id": r["Procedencia"],
        "continualidad_asistencial_id": r["Continuidad Asistencial"],
        "ingreso_UCI_id": r["Ingreso en UCI"],
        "dias_UCI": r["Días UCI"],
        "GRD_APR_id": r["Tipo GRD APR"],
        "peso_espanol_APR": r["Peso Español APR"],
        "edad_en_ingreso": r["Edad en Ingreso"],
        "year_ingreso": pd.to_datetime(r["Fecha de Ingreso"], format="%d/%m/%Y", errors="coerce").year if pd.notna(r["Fecha de Ingreso"]) else None,
        "mes_ingreso": pd.to_datetime(r["Fecha de Ingreso"], format="%d/%m/%Y", errors="coerce").month if pd.notna(r["Fecha de Ingreso"]) else None,
    })
    
"""
diagnostico_rows = []
for i, r in df.iterrows():
    for j in range(1, 21):
        col = f"Diagnóstico {j}"
        if pd.notna(r[col]):
            diagnostico_rows.append({
                "paciente_id": i+1,
            })
"""

def insert_sql(table, row):
    cols = ", ".join(row.keys())
    vals = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in row.values()])
    return f"INSERT INTO {table} ({cols}) VALUES ({vals});"

# Ejemplo:
for row in paciente_rows:
    print(insert_sql("paciente", row))

"""
for row in diagnostico_rows:
    print(insert_sql("diagnostico", row))
"""