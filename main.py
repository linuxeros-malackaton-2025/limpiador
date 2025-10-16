import pandas as pd
import datetime


df = pd.read_csv('SaludMental.csv')
# limit to 10 rows for testing
df = df.head(100)


# Drop columns with in which all values are NaN
# df = df.dropna(axis=1, how='all')

print("##########Head:\n", df.head())
print("##########Info:\n", df.info())
print("##########Describe:\n", df.describe())
print("##########Columns:\n", df.columns)

# Save cleaned data to a new CSV file
df.to_csv('SaludMental_cleaned.csv', index=False)

nombres={n: i+1 for i, n in enumerate(df["Nombre"].dropna().unique())}
sexos = {1: "Varon", 2: "Mujer", 3: "Indeterminado", 9: "No específicado"}
comunidades = {n: i+1 for i, n in enumerate(df["Comunidad Autónoma"].dropna().unique())}
circunstancias = {1:"No Programado", 2:"Programado", 9:"Desconocido"}

###no verificados
tipos_alta = {1:"Alta voluntaria", 2:"Alta médica", 3:"Alta a otro centro", 4:"Fallecimiento", 5:"Otro", 9:"Desconocido"}
servicios = {n: i+1 for i, n in enumerate(df["Servicio"].dropna().unique())}
paises = {724:"España", 826:"Reino Unido", 250:"Francia", 276:"Alemania", 380:"Italia", 56:"Bélgica"}
procedencias = {1:"Urgencias", 2:"Consulta Externa", 3:"Otro Servicio Hospitalario", 4:"Otro Centro Sanitario", 5:"Domicilio", 9:"Desconocido"}
continualidades = {1:"Ambulatoria", 2:"Domiciliaria", 3:"Hospitalización Parcial", 4:"Rehabilitación Psicosocial", 5:"Otro Centro Sanitario", 9:"Desconocido"}
ingresos_uci = {1:"No", 2:"Sí", 9:"Desconocido"}
grd_apr_tipos = {n: i+1 for i, n in enumerate(df["Tipo GRD APR"].dropna().unique())} 


print("##########Sexos:\n", sexos)
print("##########Comunidades:\n", comunidades)



paciente_rows = []
for _, r in df.iterrows():
    paciente_rows.append({
        "comunidad_autonoma_id": comunidades.get(r["Comunidad Autónoma"]),
        "nombre": nombres.get(r["Nombre"]),
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
        "servicio_id": servicios.get(r["Servicio"]),
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
        "GRD_APR_id": grd_apr_tipos.get(r["Tipo GRD APR"]),
        "peso_espanol_APR": r["Peso Español APR"],
        "edad_en_ingreso": r["Edad en Ingreso"],
        "year_ingreso": pd.to_datetime(r["Fecha de Ingreso"], format="%d/%m/%Y", errors="coerce").year if pd.notna(r["Fecha de Ingreso"]) else None,
        "mes_ingreso": pd.to_datetime(r["Fecha de Ingreso"], format="%d/%m/%Y", errors="coerce").month if pd.notna(r["Fecha de Ingreso"]) else None,
    })

def insert_sql(table, row):
    def format_val(v):
        # Convert pandas/None/NaN/NaT to SQL NULL
        if pd.isna(v):
            return "NULL"
        # Datetime types -> formatted string
        if isinstance(v, (pd.Timestamp, datetime.datetime, datetime.date)):
            # include time if present
            try:
                if getattr(v, "hour", 0) or getattr(v, "minute", 0) or getattr(v, "second", 0):
                    return f"'{v.strftime('%Y-%m-%d %H:%M:%S')}'"
            except Exception:
                pass
            return f"'{v.strftime('%Y-%m-%d')}'"
        # Strings -> escape single quotes
        if isinstance(v, str):
            return "'" + v.replace("'", "''") + "'"
        # Booleans -> integers
        if isinstance(v, bool):
            return '1' if v else '0'
        # Fallback (numbers, etc.)
        return str(v)

    cols = ", ".join(row.keys())
    vals = ", ".join(format_val(v) for v in row.values())
    return f"INSERT INTO {table} ({cols}) VALUES ({vals});"


for nombre in nombres.items():
    print(insert_sql("nombre", {"id": nombre[1], "nombre": nombre[0]}))

for sexo in sexos.items():
    print(insert_sql("sexo", {"id": sexo[0], "nombre": sexo[1]}))

for comunidad in comunidades.items():
    print(insert_sql("comunidad_autonoma", {"id": comunidad[1], "nombre": comunidad[0]}))

for circunstancia in circunstancias.items():
    print(insert_sql("circunstancia_contacto", {"id": circunstancia[0], "nombre": circunstancia[1]}))

for tipo_alta in tipos_alta.items():
    print(insert_sql("tipo_alta", {"id": tipo_alta[0], "nombre": tipo_alta[1]}))
    
for servicio in servicios.items():
    print(insert_sql("servicio", {"id": servicio[1], "nombre": servicio[0]}))

for pais in paises.items():
    print(insert_sql("pais", {"id": pais[0], "nombre": pais[1]}))

for procedencia in procedencias.items():
    print(insert_sql("procedencia", {"id": procedencia[0], "nombre": procedencia[1]}))

for continualidad in continualidades.items():
    print(insert_sql("continualidad_asistencial", {"id": continualidad[0], "nombre": continualidad[1]}))

for ingreso_uci in ingresos_uci.items():
    print(insert_sql("ingreso_UCI", {"id": ingreso_uci[0], "nombre": ingreso_uci[1]}))

for grd_apr_tipo in grd_apr_tipos.items():
    print(insert_sql("GRD_APR", {"id": grd_apr_tipo[1], "GRD": grd_apr_tipo[0]}))


# Generar e imprimir las sentencias SQL para la tabla paciente
for row in paciente_rows:
    print(insert_sql("paciente", row))
