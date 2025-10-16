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

tipos_POA = {"S": "Sí", "N": "No", "E": "Extento", "D": "Desconocido","I":"Indeterminado Clínicamente"}

print("##########Sexos:\n", sexos)
print("##########Comunidades:\n", comunidades)

"""
Table paciente [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	comunidad_autonoma_id integer [ not null ]
	nombre varchar2(255) [ not null ]
	fecha_nacimiento date [ not null ]
...
	year_ingreso number [ not null ]
	mes_ingreso number [ not null ]
}

Table diagnostico [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	paciente_id integer [ not null ]
	codigo varchar2 [ not null ]
}

Table sexo [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	nombre varchar2 [ not null ]
}

Table tipo_alta [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	nombre integer [ not null ]
}

Table circunstancia_contacto [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	nombre integer [ not null ]
}

Table servicio [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
}

Table pais [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	nombre varchar2 [ not null ]
}

Table procedencia [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	nombre varchar2 [ not null ]
}

Table continualidad_asistencial [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	nombre varchar2 [ not null ]
}

Table ingreso_UCI [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	nombre varchar2 [ not null ]
}

Table GRD_APR [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	GRD integer [ not null ]
}

Table comunidad_autonoma [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	nombre varchar2 [ not null ]
}

Table POA_diagnostico [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	paciente_id integer [ not null ]
	tipo_POA_id integer [ not null ]
}

Table tipo_POA [headercolor: #175e7a] {
	id integer [ pk, increment, not null, unique ]
	nombre integer [ not null ]
}

Ref fk_Paciente_comunidad_autonoma_id_comunidad_autonoma {
	paciente.comunidad_autonoma_id > comunidad_autonoma.id [ delete: no action, update: no action ]
}

Ref "fk_sexo EE_id_Paciente" {
	sexo.id < paciente.sexo_id [ delete: no action, update: no action ]
}

Ref "fk_GRD_APR EE_id_paciente" {
	GRD_APR.id < paciente.GRD_APR_id [ delete: no action, update: no action ]
}

Ref "fk_ingreso_UCI EE_id_paciente" {
	ingreso_UCI.id < paciente.ingreso_UCI_id [ delete: no action, update: no action ]
}

Ref "fk_continualidad_asistencial EE_id_paciente" {
	continualidad_asistencial.id < paciente.continualidad_asistencial_id [ delete: no action, update: no action ]
}

Ref fk_procedencia_id_paciente {
	procedencia.id < paciente.procedencia_id [ delete: no action, update: no action ]
}

Ref "fk_tipo_alta EE_id_paciente" {
	tipo_alta.id < paciente.tipo_alta_id [ delete: no action, update: no action ]
}

Ref "fk_circunstancia_contacto EE_id_paciente" {
	circunstancia_contacto.id < paciente.circunstancia_contacto_id [ delete: no action, update: no action ]
}

Ref "fk_servicio EE_id_paciente" {
	servicio.id < paciente.servicio_id [ delete: no action, update: no action ]
}

Ref "fk_pais_nacimiento EE_id_paciente" {
	pais.id < paciente.pais_nacimiento_id [ delete: no action, update: no action ]
}

Ref "fk_pais_nacimiento EE_id_paciente" {
	pais.id < paciente.pais_residencia_id [ delete: no action, update: no action ]
}

Ref "fk_paciente_id_diagnostico EE" {
	paciente.id < diagnostico.paciente_id [ delete: no action, update: no action ]
}

Ref fk_paciente_id_POA_diagnostico {
	paciente.id < POA_diagnostico.paciente_id [ delete: no action, update: no action ]
}

Ref fk_tipo_POA_id_POA_diagnostico {
	tipo_POA.id < POA_diagnostico.tipo_POA_id [ delete: no action, update: no action ]
}

    Comunidad Autónoma	Nombre	Fecha de nacimiento	Sexo	CCAA Residencia	Fecha de Ingreso	Circunstancia de Contacto	Fecha de Fin Contacto	Tipo Alta	Estancia Días	Diagnóstico Principal	Categoría	Diagnóstico 2	Diagnóstico 3	Diagnóstico 4	Diagnóstico 5	Diagnóstico 6	Diagnóstico 7	Diagnóstico 8	Diagnóstico 9	Diagnóstico 10	Diagnóstico 11	Diagnóstico 12	Diagnóstico 13	Diagnóstico 14	Fecha de Intervención	Procedimiento 1	Procedimiento 2	Procedimiento 3	Procedimiento 4	Procedimiento 5	Procedimiento 6	Procedimiento 7	Procedimiento 8	Procedimiento 9	Procedimiento 10	Procedimiento 11	Procedimiento 12	Procedimiento 13	Procedimiento 14	Procedimiento 15	Procedimiento 16	Procedimiento 17	Procedimiento 18	Procedimiento 19	Procedimiento 20	GDR AP	CDM AP	Tipo GDR AP	Valor Peso Español	GRD APR	CDM APR	Tipo GDR APR	Valor Peso Americano APR	Nivel Severidad APR	Riesgo Mortalidad APR	Servicio	Edad	Reingreso	Coste APR	GDR IR	Tipo GDR IR	Tipo PROCESO IR	CIE	Número de registro anual	Centro Recodificado	CIP SNS Recodificado	País Nacimiento	País Residencia	Fecha de Inicio contacto	Régimen Financiación	Procedencia	Continuidad Asistencial	Ingreso en UCI	Días UCI	Diagnóstico 15	Diagnóstico 16	Diagnóstico 17	Diagnóstico 18	Diagnóstico 19	Diagnóstico 20	POA Diagnóstico Principal	POA Diagnóstico 2	POA Diagnóstico 3	POA Diagnóstico 4	POA Diagnóstico 5	POA Diagnóstico 6	POA Diagnóstico 7	POA Diagnóstico 8	POA Diagnóstico 9	POA Diagnóstico 10	POA Diagnóstico 11	POA Diagnóstico 12	POA Diagnóstico 13	POA Diagnóstico 14	POA Diagnóstico 15	POA Diagnóstico 16	POA Diagnóstico 17	POA Diagnóstico 18	POA Diagnóstico 19	POA Diagnóstico 20	Procedimiento Externo 1	Procedimiento Externo 2	Procedimiento Externo 3	Procedimiento Externo 4	Procedimiento Externo 5	Procedimiento Externo 6	Tipo GRD APR	Peso Español APR	Edad en Ingreso	Mes de Ingreso
ANDALUCÍA	MONICA TINEO RODRIGUEZ	8/17/1951	2		1/1/2016	1	08/01/2016	1	7	F25.0	Esquizofrenia, trastornos esquizotípicos y trastornos delirantes	Z63.79	Z91.19																																					750	19			2	1	PSQ	64		6340				10	8537155.0	-2088791444897190000	109457269-593755146	724	724	01012016 1622	1.0	21.0	9.0	2.0								S	E	S																								M	1.393611	64	2016-01
ANDALUCÍA	IRENE RODRIGUEZ HERNANDEZ	3/20/1929	2		1/1/2016	1	08/01/2016	1	7	F41.9	Trastornos neuróticos, trastornos relacionados con el estrés y trastornos somatomorfos	I11.9	I35.8	E11.9	I87.2	Z95.0										4B02XSZ	B246ZZZ	4A02X4Z																						756	19			1	2	CAR	86		2771				10	8992115.0	-1166333372325380000	-1589750168781380000	ZZZ	724	01012016 0453	1.0	21.0	9.0	2.0								S	S	S	S	S	E																					M	0.609264	86	2016-01

    """

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
    
# POA Diagnóstico Principal + POA Diagnóstico 2 ... POA Diagnóstico 20
filas_POA = {"POA Diagnóstico Principal"} | {f"POA Diagnóstico {i}" for i in range(2, 21)}

# FOr each row and for each POA Diagnóstico column, create a row in POA_diagnostico table, if a value does not exist, skip it, if a column from filas_POA does not exist, skip it
poa_diagnostico_rows = []
for i, r in enumerate(df.itertuples(), start=1):
    for col in filas_POA:
        if hasattr(r, col.replace(" ", "_")) and pd.notna(getattr(r, col.replace(" ", "_"))):
            poa_diagnostico_rows.append({
                "paciente_id": i,
                "tipo_POA_id": tipos_POA.get(getattr(r, col.replace(" ", "_")))
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

for i, row in enumerate(poa_diagnostico_rows, start=1):
    row["id"] = i
    print(insert_sql("POA_diagnostico", row))