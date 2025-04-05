import requests
import json
import re
import pymysql
from app.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


def manejar_pregunta(pregunta):
    def es_sql_seguro(sql):
        s = sql.lower().strip()
        if not s.startswith("select"):
            return False
        for p in ["drop", "delete", "update", "insert", "--", ";--", "alter"]:
            if p in s:
                return False
        return True

    def extraer_sql(texto):
        match = re.search(r"<sql>(.*?)</sql>", texto, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        match = re.search(r"(select .*?;)", texto, flags=re.IGNORECASE | re.DOTALL)
        if match:
            raw = match.group(1)
            return raw.split(";")[0].strip() + ";"
        return ""

    def ejecutar_sql(sql):
        if not es_sql_seguro(sql):
            raise ValueError("Consulta SQL no permitida")

        try:
            conn = pymysql.connect(
                host="db",
                user= MYSQL_USER,
                password= MYSQL_PASSWORD,
                database= MYSQL_DATABASE,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.Cursor
            )
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    rows = cur.fetchall()
                    cols = [desc[0] for desc in cur.description]

            if not rows:
                return "No se encontraron resultados"

            resultados = []
            for row in rows:
                resultados.append(", ".join(f"{col}: {val}" for col, val in zip(cols, row)))
            return "\n".join(resultados)

        except pymysql.MySQLError as e:
            raise Exception(f"Error en la base de datos: {str(e)}")

    def describir_bd():
        return """
      CREATE TABLE Brand (
  id_brand int NOT NULL,
  name varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE Model (
  id_model int NOT NULL,
  name varchar(50) NOT NULL,
  id_brand_fk int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE Description (
  id_description int NOT NULL,
  name varchar(100) NOT NULL,
  id_model_fk int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE Vehicle (
  id_vehicle int NOT NULL,
  id_model_fk int NOT NULL,
  id_description_fk int NOT NULL,
  id_brand_fk int NOT NULL,
  number_plate varchar(10) NOT NULL,
  serial_number varchar(10) NOT NULL,
  year int NOT NULL,
  color varchar(20) NOT NULL,
  km int NOT NULL,
  km_per_litre int NOT NULL,
  route_status varchar(9) DEFAULT NULL,
  assignment_status varchar(12) DEFAULT NULL
);

CREATE TABLE Role (
  id_role int NOT NULL,
  name varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE User (
  id_usuario int NOT NULL,
  first_name varchar(50) NOT NULL,
  last_name varchar(50) NOT NULL,
  email varchar(100) NOT NULL,
  password varchar(255) NOT NULL,
  id_role_fk int NOT NULL,
  id_vehicle_fk int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE Route (
  id_route int NOT NULL,
  id_vehicle_fk int NOT NULL,
  id_user_fk int NOT NULL,
  description varchar(255) NOT NULL,
  latitude_start varchar(50) DEFAULT NULL,
  longitude_start varchar(50) DEFAULT NULL,
  latitude_end varchar(50) DEFAULT NULL,
  longitude_end varchar(50) DEFAULT NULL,
  start_time datetime DEFAULT NULL,
  end_time datetime DEFAULT NULL,
  estimated_time double DEFAULT NULL,
  total_duration double DEFAULT NULL,
  on_time tinyint(1) DEFAULT NULL,
  start_km int DEFAULT NULL,
  end_km int DEFAULT NULL,
  total_km int DEFAULT NULL,
  estimated_km int DEFAULT NULL,
  image_start_km varchar(255) DEFAULT NULL,
  image_end_km varchar(255) DEFAULT NULL,
  on_distance tinyint(1) DEFAULT NULL,
  liters_consumed double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE FuelStop (
  id_fuel_stop int NOT NULL,
  id_route_fk int NOT NULL,
  Latitude_stop varchar(255) NOT NULL,
  Longitude_stop varchar(255) NOT NULL,
  stop_time datetime NOT NULL,
  resume_time datetime DEFAULT NULL,
  start_time datetime DEFAULT NULL,
  Latitude_start varchar(255) DEFAULT NULL,
  Longitude_start varchar(255) DEFAULT NULL,
  current_km int DEFAULT NULL,
  image_km varchar(255) DEFAULT NULL,
  liters_added decimal(5,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE Maintenance (
  id_maintenance int NOT NULL,
  id_vehicle_fk int NOT NULL,
  description text,
  start_time datetime NOT NULL,
  estimated_time time NOT NULL,
  end_time datetime DEFAULT NULL,
  status varchar(11) NOT NULL
);
      """  # No modifiqué esta parte, puedes mantener tu contenido tal cual

    try:
        contexto_db = describir_bd()
        prompt = f"""{contexto_db}

Eres un asistente inteligente.
- Si el usuario pregunta sobre la base de datos, genera SELECT dentro de <sql>...</sql>.
- Si no es sobre la BD, responde normalmente, pero enfocado a datos.
- NO uses DROP, DELETE, UPDATE, INSERT.

Pregunta:
{pregunta}
Responde:
"""
        response = requests.post(
            "http://ollama:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 200}
            }
        )
        data = response.json()
        respuesta_completa = data.get("response", "")

        posible_sql = extraer_sql(respuesta_completa)

        if posible_sql:
            resultado_bd = ejecutar_sql(posible_sql)

            segundo_prompt = f"""
Eres un asistente amable. El usuario preguntó:

{pregunta}

Resultado desde la base de datos:
{resultado_bd}

Responde de forma clara, sin mencionar SQL ni consultas. Si hay correos o roles, menciónalos.
"""
            response2 = requests.post(
                "http://ollama:11434/api/generate",
                json={
                    "model": "gemma:2b",
                    "prompt": segundo_prompt,
                    "stream": False,
                    "options": {"num_predict": 200}
                }
            )
            data2 = response2.json()
            return data2.get("response", "").replace("\n", " ").replace(" - ", ", ").strip()

        return respuesta_completa.strip()

    except Exception as e:
        return f"Error: {str(e)}"


# if __name__ == "__main__":
#     respuesta = manejar_pregunta("¿Cuántos usuarios hay en el sistema?")
#     print(respuesta)
