
import os
import django
from datetime import datetime
from django.db import connection

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()


def update_turnos_status():
    now = datetime.now()
    vfecha = now.strftime("%Y-%m-%d")  # Ensure the date format is correct for SQL

    # SQL query
    vq = f"""
        SELECT 
            ta.id,
            ta.turno_num, 
            ta.turno_id,
            ta.consultorio,
            t.descripcion,
            t.tipo_id,
            c.id,
            c.nombre,
            c.disponible
        FROM 
            laboratorio_turnos_agenda ta
        JOIN 
            laboratorio_turnos t ON t.id = ta.turno_id
        JOIN 
            laboratorio_consultorios c ON c.tipo_id = t.tipo_id
        WHERE 
            ta.fecha = '{vfecha}'
            AND ta.liberado = 'S'
            AND ta.hora_atencion = ''
            AND ta.consultorio = ''
            AND c.disponible = 'S'
        LIMIT 1
    """

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(vq)
        rows = cursor.fetchall()

        # Process the results
        for r in rows:
            vturno_agenda_id = r[0]
            vturno_num = r[1]
            vturno_id = r[2]
            vconsultorio_id = r[6]
            vconsultorio_nombre = r[7]

            # Actualizar consultorio como NO disponible
            vqcons = f"""
                UPDATE laboratorio_consultorios SET disponible = 'N' WHERE id = {vconsultorio_id}  
            """
            cursor.execute(vqcons)

            # Actualizar turno_agenda como asignado
            vqturno = f"""
                UPDATE laboratorio_turnos_agenda SET consultorio = '{vconsultorio_nombre}' WHERE id = {vturno_agenda_id}
            """

            cursor.execute(vqturno)


if __name__ == "__main__":
    update_turnos_status()
