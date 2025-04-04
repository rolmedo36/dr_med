from datetime import datetime, date
from django.db import connection
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.templatetags.static import static
from django.urls import reverse
from .models import Menu, MenuOpciones, Consultorios, Medicos, Productos, Clientes, CodigoPostal, Citas, Turnos, Turnos_agenda
from .forms import CreateNewConsultorio, CreateNewMedico, CreateNewProductos, CreateNewClientes
import ConectorPython
from fpdf import FPDF
from PIL import Image
import os
import subprocess
import sys

# Create your views here.
def index(request):
    titulo = 'Dr.Med'
    # menus = get_object_or_404(Menu)
    menus = Menu.objects.all()
    menuopciones = MenuOpciones.objects.all()
    print(menus)
    # print('lista: ', list(menuopciones))
    return render(request, "index.html", {
        'titulo': titulo,
        'menus': menus,
        'menuopciones': menuopciones
    })


def consultorios(request):
    if request.method == 'GET':
        consultorios = Consultorios.objects.all()
        return render(request, 'consultorio.html', {
            'title': 'CONSULTORIOS',
            'consultorios': consultorios,
            'nuevo': '0'
        })
    else:
        vnombre = request.POST['nombre']
        Consultorios.objects.create(nombre=vnombre)
        return redirect('consultorios')


def consultorio_mantto(request, id):
    i = str(id)
    tipo = str(i[0:1])
    id2 = str(i[1:])

    if request.method == 'POST' and request.POST['tipo'] == '1':
        vnombre = request.POST['nombre']
        Consultorios.objects.create(nombre=vnombre)
        return redirect('consultorios')
    if request.method == 'POST' and request.POST['tipo'] == '2':
        vnombre = request.POST['nombre']
        consultorio = Consultorios.objects.get(id=id2)
        consultorio.nombre = vnombre
        consultorio.save()
        return redirect('consultorios')

    if tipo == '1':
        consultorio = Consultorios.objects.get(id=id2)
        consultorio.delete()
    elif tipo == '0':
        return render(request, 'consultorio.html', {
            'title': 'NUEVO CONSULTORIO',
            'nuevo': '1',
            'form': CreateNewConsultorio
        })
    else:
        consultorio = Consultorios.objects.get(id=id2)
        nombre = consultorio.nombre
        return render(request, 'consultorio.html', {
            'title': 'MODIFICA CONSULTORIO',
            'nuevo': '2',
            'form': CreateNewConsultorio,
            'id': id2,
            'nombre': nombre
        })

    return redirect('consultorios')


def medicos(request):
    if request.method == 'GET':
        medicos = Medicos.objects.all()
        consultorios = Consultorios.objects.all()
        return render(request, 'medicos.html', {
            'title': 'MEDICOS',
            'medicos': medicos,
            'consultorios': consultorios,
            'nuevo': '0'
        })
    else:
        vnombre = request.POST['nombre']
        vcedula = request.POST['cedula']
        Medicos.objects.create(nombre=vnombre, cedula=vcedula)
        return redirect('medicos')


def medicos_mantto(request, id):
    i = str(id)
    tipo = str(i[0:1])
    id2 = str(i[1:])

    if request.method == 'POST' and request.POST['tipo'] == '1':
        vconsultorio = request.POST['consultorio']
        vnombre = request.POST['nombre']
        Medicos.objects.create(nombre=vnombre, consultorio_id=vconsultorio)
        return redirect('medicos')
    if request.method == 'POST' and request.POST['tipo'] == '2':
        vnombre = request.POST['nombre']
        medico = Medicos.objects.get(id=id2)
        medico.nombre = vnombre
        medico.save()
        return redirect('medicos')

    if tipo == '1':
        medico = Medicos.objects.get(id=id2)
        medico.delete()
    elif tipo == '0':
        consultorios = Consultorios.objects.all()
        return render(request, 'medicos.html', {
            'title': 'NUEVO MEDICO',
            'nuevo': '1',
            'consultorios': consultorios,
            'form': CreateNewMedico
        })
    else:
        medico = Medicos.objects.get(id=id2)
        nombre = medico.nombre
        return render(request, 'medicos.html', {
            'title': 'MODIFICA MEDICO',
            'nuevo': '2',
            'form': CreateNewMedico,
            'id': id2,
            'nombre': nombre
        })

    return redirect('medicos')


def productos(request, id):
    id1 = str(id)
    id2 = id1[0:1]
    id3 = id1[1:]
    if request.method == 'POST':
        print('GRABA: ', request.POST['nombre'], request)
        vnombre = request.POST['nombre']
        vdescripcion = request.POST['descripcion']
        vprecio = request.POST['precio']
        vprecio2 = float(vprecio)
        Productos.objects.create(nombre=vnombre, descripcion=vdescripcion, precio=vprecio2)
        return redirect('/productos/9')
    if request.method == 'GET' and id2 == '9':
        productos = Productos.objects.all()
        return render(request, 'productos.html', {
            'title': 'PRODUCTOS',
            'productos': productos,
            'nuevo': '0'
        })
    elif request.method == 'GET' and id2 == '0':
        productos = Productos.objects.all()
        return render(request, 'productos.html', {
            'title': 'NUEVO PRODUCTO',
            'nuevo': '1',
            'productos': productos,
            'form': CreateNewProductos
        })
    elif request.method == 'GET' and id2 == '1':
        producto = Productos.objects.get(id=id3)
        producto.delete()

    return redirect('/productos/9')

def clientes_turno(request):
    if request.method == 'POST':
        vturno_cte = ''
        vcliente = request.POST['buscar']
        vq = f"""
            SELECT 
                id,
                nombre, 
                apellido_paterno, 
                apellido_materno, 
                telefono1, 
                rfc 
            FROM laboratorio_clientes c 
            WHERE 1=1
                AND (c.nombre like '%{vcliente}%' OR 
                    c.apellido_paterno like '%{vcliente}%' OR 
                    c.apellido_materno like '%{vcliente}%' OR 
                    c.telefono1 like '%{vcliente}%' OR 
                    c.rfc like '%{vcliente}%' )
        """
        rows = my_custom_sql(vq)
        result_list = [
            {'id': row[0], 'nombre': row[1], 'apellido_paterno': row[2],'apellido_materno': row[3] , 'telefono': row[4], 'rfc': row[5]}
            for row in rows
        ]
        turnos = list(Turnos.objects.values())
        return render(request, 'clientes_turno.html', {
            'title': 'TURNO',
            'bandera': '1',
            'rows': result_list,
            'turnos': turnos
        })
    else:
        return render(request, 'clientes_turno.html', {
            'title': 'TURNO',
            'bandera': '0'
        })

def clientes_turno2(request):
    today = date.today()
    vfecha = today.strftime("%Y-%m-%d")
    vfecha2 = today.strftime("%d-%m-%Y")
    now = datetime.now()
    vhora = now.strftime("%H:%M:%S")
    if request.method == 'POST':
        vturno_cte = ''
        vturno_cte = request.POST['btnTurno']
        # selecciono turno para un cliente
        vturno_cte = request.POST['btnTurno']
        vturno_cte = vturno_cte.split('|')
        vcliente_id = vturno_cte[0]
        vturno_id = vturno_cte[1]
        vcliente_nombre = vturno_cte[2]
        vturno_descripcion = vturno_cte[3]
        vturno_siguiente = turno_siguiente()

        vsiguiente = str(vturno_siguiente) + " - " + vcliente_nombre
        # Crea registro
        Turnos_agenda.objects.create(
            turno_id=vturno_id,
            cliente_id=vcliente_id,
            turno_num=vturno_siguiente,
            fecha=vfecha,
            hora=vhora,
            mostrado='N'
        )
        # Imprime ticket
        imprime_ticket(vturno_descripcion, vsiguiente, vfecha2)
    return redirect('/clientes_turno/')

def clientes(request, id):
    id1 = str(id)
    id2 = id1[0:1]
    id3 = id1[1:]
    vnombre = ''
    vapellido_paterno = ''
    vapellido_materno = ''
    vtelefono1 = ''
    vtelefono2 = ''
    vcorreo = ''
    vcp = ''
    vcolonia = ''
    vcalle = ''
    vnumero_ext = ''
    vnumero_int = ''
    vfecha_nac =  ''
    vrfc = ''
    if request.method == 'POST' and request.POST['tipo'] == '1':
        vnombre = request.POST['nombre']
        vapellido_paterno = request.POST['apellido_paterno']
        vapellido_materno = request.POST['apellido_materno']
        vtelefono1 = request.POST['telefono1']
        vtelefono2 = request.POST['telefono2']
        vcorreo = request.POST['correo']
        if request.POST['codigo_postal']:
            vcp = request.POST['codigo_postal']
            vcolonia = request.POST['cboColonia']
            vcalle = request.POST['calle']
            vnumero_ext = request.POST['numero_ext']
            vnumero_int = request.POST['numero_int']
        vfecha_nac = request.POST['fecha_nac']
        vrfc = request.POST['rfc']
        Clientes.objects.create(
            nombre=vnombre,
            apellido_paterno=vapellido_paterno,
            apellido_materno=vapellido_materno,
            telefono1=vtelefono1,
            telefono2=vtelefono2,
            correo=vcorreo,
            codigopostal=vcp,
            calle=vcalle,
            numero_ext=vnumero_ext,
            numero_int=vnumero_int,
            colonia=vcolonia,
            fecha_nac=vfecha_nac,
            rfc=vrfc
        )
        return redirect('/clientes/9')
    if request.method == 'POST' and request.POST['tipo'] == '2':
        vid = request.POST['id']
        vnombre = request.POST['nombre']
        vapellido_paterno = request.POST['apellido_paterno']
        vapellido_materno = request.POST['apellido_materno']
        vtelefono1 = request.POST['telefono1']
        vtelefono2 = request.POST['telefono2']
        vcorreo = request.POST['correo']
        vcalle = request.POST['calle']
        vnumero_ext = request.POST['numero_ext']
        vnumero_int = request.POST['numero_int']
        vrfc = request.POST['rfc']

        cliente = Clientes.objects.get(id=vid)
        cliente.nombre = vnombre
        cliente.apellido_paterno = vapellido_paterno
        cliente.apellido_materno = vapellido_materno
        cliente.telefono1 = vtelefono1
        cliente.telefono2 = vtelefono2
        cliente.correo = vcorreo
        cliente.calle = vcalle
        cliente.numero_ext = vnumero_ext
        cliente.numero_int = vnumero_int
        cliente.rfc = vrfc

        cliente.save()
        return redirect('/clientes/9')

    if request.method == 'GET' and id2 == '9':
        clientes = Clientes.objects.all()
        return render(request, 'clientes.html', {
            'title': 'CLIENTES',
            'clientes': clientes,
            'nuevo': '0'
        })
    elif request.method == 'GET' and id2 == '0':
        clientes = Clientes.objects.all()
        return render(request, 'clientes.html', {
            'title': 'NUEVO CLIENTE',
            'nuevo': '1',
            'clientes': clientes,
            'form': CreateNewClientes
        })
    elif request.method == 'GET' and id2 == '1':
        clientes = Clientes.objects.get(id=id3)
        clientes.delete()
    elif request.method == 'GET' and id2 == '2':
        clientes = Clientes.objects.get(id=id3)
        return render(request, 'clientes.html', {
            'title': 'MODIFICA CLIENTE',
            'nuevo': '2',
            'form': CreateNewClientes,
            'id': id2,
            'clientes': clientes
        })

    return redirect('/clientes/9')


def get_codigos_postales(request, cp):
    cp = list(CodigoPostal.objects.filter(codigo_postal=cp).values())

    if len(cp) > 0:
        data = {'message': "Success", 'cp': cp}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)


def citas(request):
    if request.method == "POST":
        idConsultorio = request.POST["cboConsultorio"]
        idServicio = request.POST["cboServicios"]
        fecha = request.POST["txtFecha"]
        date_obj = datetime.strptime(fecha, '%Y-%m-%d')
        disponible = Citas.objects.filter(consultorio_id=idConsultorio, fecha=fecha).values()
        consultorio = Consultorios.objects.filter(id=idConsultorio).values()
        servicio = Productos.objects.filter(id=idServicio).values()

        cons_nombre = ''
        for cons in consultorio:
            cons_nombre = cons['nombre']
        servicio_nombre = ''
        for serv in servicio:
            servicio_nombre = serv['nombre']
        horario = []
        horario1 = 10
        horario2 = 15
        l = 0
        for r in range(horario1, horario2):
            r0 = str(r) + ":00"
            r1 = str(r) + ":30"
            horario.append(r0)
            horario.append(r1)
        for hora in disponible:
            print('CITA', hora['hora'])
            for i in horario:
                # l += 1
                if i == hora['hora']:
                    i = hora['hora'] + " RESERVADO"
                    horario[l] = i
                l += 1
            l = 0
        return render(request, 'agendar_cita.html', {
            'title': 'Agendar Consulta',
            'consultorio': idConsultorio,
            'cons_nombre': cons_nombre,
            'fecha': fecha,
            'fecha2': date_obj.strftime("%d/%b/%Y"),
            'horarios': horario,
            'servicio': idServicio,
            'servicio_nombre': servicio_nombre,
        })

    return render(request, 'citas.html', {
        'title': 'Consultas Médicas',

    })


def get_servicios(request):
    servicios = list(Productos.objects.values())

    if len(servicios) > 0:
        data = {'message': "Success", 'servicios': servicios}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)


def get_consultorios(request):
    consultorios = list(Consultorios.objects.values())

    if len(consultorios) > 0:
        data = {'message': "Success", 'consultorios': consultorios}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)


def get_disponible(request, idConsultorio, fecha):
    disponible = list(Citas.objects.filter(consultorio_id=idConsultorio, fecha=fecha).values())
    horario = []
    horario1 = 10
    horario2 = 15
    l = 0

    for r in range(horario1, horario2):
        r0 = str(r) + ":00"
        r1 = str(r) + ":30"
        horario.append(r0)
        horario.append(r1)
    for hora in disponible:
        for i in horario:
            l += 1
            if i == hora['hora']:
                i = hora['hora'] + " RESERVADO"
                horario[l - 1] = i

    if len(disponible) > 0:
        data = {'message': "Success", 'disponibles': horario}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)


def agendar_cita(request):
    horarios = request.POST['txtOpciones']
    return render(request, 'agendar_cita.html', {
        'title': 'Agenda Cita',
        'horarios': horarios

    })


def captura_reserva(request, idcons, fecha, hora, servicio):
    if request.method == "POST":
        vidcons = idcons
        vidmedico = ''
        vidcliente = request.POST['cboClientes']
        vfecha = fecha
        vhora = hora
        vobservaciones = request.POST['txtObservaciones']
        vidservicio = servicio
        Citas.objects.create(
            consultorio_id=vidcons,
            medico_id=vidmedico,
            cliente_id=vidcliente,
            fecha=vfecha,
            hora=vhora,
            observaciones=vobservaciones,
            servicio_id=vidservicio
        )
        return redirect('/citas')
    else:
        fecha = fecha
        date_obj = datetime.strptime(fecha, '%Y-%m-%d')
        consultorio = Consultorios.objects.filter(id=idcons).values()
        producto = Productos.objects.filter(id=servicio).values()
        cons_nombre = ''
        servicio_precio = ''
        for cons in consultorio:
            cons_nombre = cons['nombre']
        servicio_nombre = ''
        for prod in producto:
            servicio_nombre = prod['nombre']
            servicio_precio = prod['precio']
        return render(request, 'captura_reserva.html', {
            'title': 'Captura datos de reservación',
            'idcons': idcons,
            'idserv': servicio,
            'fecha': fecha,
            'hora': hora,
            'cons_nombre': cons_nombre,
            'serv_nombre': servicio_nombre,
            'fecha2': date_obj.strftime("%d/%b/%Y"),
            'precio': servicio_precio
        })


def get_clientes(request, inCliente):
    lista_clientes = list(Clientes.objects.filter(nombre__contains=inCliente).values())

    if len(lista_clientes) > 0:
        data = {'message': "Success", 'clientes': lista_clientes}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)


def graba_reserva(request):
    if request.method == "POST":
        vidcons = request.POST['idcons']
        vidserv = request.POST['idservicio']
        vidmedico = ''
        vidcliente = request.POST['cboClientes']
        vfecha = request.POST['fecha']
        vhora = request.POST['hora']
        vobservaciones = request.POST['txtObservaciones']
        vprecio = request.POST['servicio_precio']
        Citas.objects.create(
            consultorio_id=vidcons,
            medico_id=vidmedico,
            cliente_id=vidcliente,
            fecha=vfecha,
            hora=vhora,
            observaciones=vobservaciones,
            servicio_id=vidserv,
            precio=vprecio
        )
        return redirect('/citas')


def informe_citas(request):
    reporte = ''
    hoy = ''
    r = ''
    j2 = ''
    if request.method == 'POST':
        vfecha1 = request.POST['inFecha1']
        vfecha2 = request.POST['inFecha2']
        #  reporte = Citas.objects.filter(fecha__gte=vfecha1, fecha__lte=vfecha2).all()
        vquery = f"""
        SELECT a.fecha, a.hora, b.nombre, c.nombre, d.nombre
        FROM laboratorio_citas a, laboratorio_consultorios b, laboratorio_clientes c, laboratorio_productos d
        WHERE 1=1
            AND a.fecha >= '{vfecha1}'
            AND a.fecha <= '{vfecha2}'
            AND a.consultorio_id = b.id 
            AND a.cliente_id = c.id 
            AND a.servicio_id = d.id
        ORDER BY a.fecha DESC
        """
        r = my_custom_sql(vquery)
        i = 0
        j2 = ''
        j = '['
        for i in r:
            j += '{"fecha": "' + i[0] + '","hora": "' + i[1] + '",' + '"consultorio": "' + i[
                2] + '",' + '"cliente": "' + i[3] + '",' + '"servicio": "' + i[4] + '"' + '},'
        j += ']'
        j = j[0:len(j) - 2] + ']'
        j2 = json.loads(j)
    else:
        hoy = datetime.now()
        hoy = hoy.strftime('%d/%m/%Y')

    return render(request, 'informe_citas.html', {
        'title': 'Informe de citas',
        'hoy': hoy,
        'reporte': j2,
    })

def informe_expediente(request):
    if request.method == 'POST':
        vcliente_id = request.POST['cboClientes']

        vquery = f"""
            SELECT 
                lc.id,
                lc.fecha,
                lc.hora,
                lm.nombre,
                CONCAT(lc2.nombre,' ',lc2.apellido_paterno) as cliente,
                lc.checkin_edad,
                lc.checkin_sexo,
                lc.checkin_peso,
                lc.checkin_talla,
                lc.checkin_presion_arterial,
                lc.checkin_frecuencia_cardiaca,
                lc.checkin_frecuencia_respiratoria,
                lc.checkin_temperatura,
                lc.checkin_resumen,
                lc.checkin_exploracion_fisica,
                lc.checkin_resultado_servicios_auxiliares,
                lc.checkin_problemas_clinicos,
                lc.checkin_indicaciones_medicas,
                lc.checkin_pronostico,
                lc.turno_num,
                lta.hora
            FROM
                laboratorio_citas lc,
                laboratorio_medicos lm,
                laboratorio_clientes lc2,
                laboratorio_turnos_agenda lta 
            WHERE 1=1
                AND lc.cliente_id = {vcliente_id}
                AND lm.id = lc.medico_id
                AND lc2.id = lc.cliente_id
                AND (lta.turno_num = lc.turno_num AND lta.fecha = lc.fecha)
            ORDER BY lc.fecha DESC
        """

        # Use parameterized queries to prevent SQL injection
        r = my_custom_sql(vquery)

        # Prepare data
        results = []
        for row in r:
            record = {
                "id": str(row[0]),
                "fecha": str(row[1]),
                "hora_fin": str(row[2]),
                "medico": row[3],
                "cliente": row[4],
                "edad": str(row[5]),
                "sexo": row[6],
                "peso": str(row[7]),
                "talla": str(row[8]),
                "presion_arterial": str(row[9]),
                "frecuencia_cardiaca": str(row[10]),
                "frecuencia_respiratoria": str(row[11]),
                "temperatura": str(row[12]),
                "resumen": escape_newlines(row[13]),
                "exploracion_fisica": escape_newlines(row[14]),
                "resultado_servicios_auxiliares": escape_newlines(row[15]),
                "problemas_clinicos": escape_newlines(row[16]),
                "indicaciones_medicas": escape_newlines(row[17]),
                "pronostico": escape_newlines(row[18]),
                "turno_num": str(row[19]),
                "hora_ini": str(row[20]),
            }

            # Escape newline characters in string fields
            for key, value in record.items():
                record[key] = escape_newlines(value)

            results.append(record)

        # Convert results to JSON
        j2 = json.dumps(results)
        # Return the response
        return render(request, 'informe_expediente2.html', {
            'title': 'Expediente Clínico',
            'reporte': json.loads(j2)
        })

    return render(request, 'informe_expediente.html', {
        'title': 'Expediente Clínico'
    })

def atender_cita(request):
    if request.method == "POST":
        idConsultorio = request.POST["cboConsultorio"]
        fecha = request.POST["txtFecha"]
        date_obj = datetime.strptime(fecha, '%Y-%m-%d')
        vquery = (
            f"""SELECT a.id, a.fecha, a.hora, a.observaciones, b.nombre, c.nombre FROM laboratorio_citas a, laboratorio_clientes b, laboratorio_consultorios c WHERE a.consultorio_id = '{idConsultorio}' AND a.fecha = '{fecha}' AND a.checkout_hora = '' AND a.cliente_id = b.id AND a.consultorio_id = c.id""")
        r = my_custom_sql(vquery)
        if len(r) > 0:
            i = 0
            j2 = ''
            j = '['
            for i in r:
                cons_nombre = i[5]
                j += '{"id": "' + str(i[0]) + '", "fecha": "' + i[1] + '","hora": "' + i[2] + '",' + '"observaciones": "' + \
                     i[3] + '",' + '"nombre": "' + i[4] + '",' + '"consultorio": "' + i[5] + '"' + '},'
            j += ']'
            j = j[0:len(j) - 2] + ']'
            j2 = json.loads(j)
            return render(request, 'atender_cita2.html', {
                'title': 'Atender Consulta',
                'fecha2': date_obj.strftime("%d/%b/%Y"),
                'cons_nombre': cons_nombre,
                'citas': j2
            })

    return render(request, 'atender_cita.html', {
        'title': 'Atender Consulta',

    })


def atender_cita3(request, idcita):
    if request.method == 'POST':
        cita_id = request.POST['cita_id']
        cita = Citas.objects.get(id=cita_id)
        vreceta = request.POST['txtIndicacionesMedicas']
        vmedico = request.POST['cboMedicos']

        cita.medico_id = request.POST['cboMedicos']
        cita.checkin_fecha = request.POST['fecha_ini']
        cita.checkin_edad = request.POST['txtedad']
        cita.checkin_sexo = request.POST['txtsexo']
        cita.checkin_peso = request.POST['txtpeso']
        cita.checkin_talla = request.POST['txttalla']
        cita.checkin_presion_arterial = request.POST['txtpresion']
        cita.checkin_frecuencia_cardiaca = request.POST['txtcardiaca']
        cita.checkin_frecuencia_respiratoria = request.POST['txtrespiratoria']
        cita.checkin_temperatura = request.POST['txttemperatura']
        cita.checkin_resumen = request.POST['txtResumen']
        cita.checkin_exploracion_fisica = request.POST['txtExploracion']
        cita.checkin_resultado_servicios_auxiliares = request.POST['txtSrvAuxiliares']
        cita.checkin_problemas_clinicos = request.POST['txtProblemasClinicos']
        cita.checkin_indicaciones_medicas = request.POST['txtIndicacionesMedicas']
        cita.checkin_pronostico = request.POST['txtPronostico']
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        dt_archivo = now.strftime("%d%m%Y%H%M%S")
        cita.checkout_hora = dt_string
        cita.save()

        # Lee datos de medico
        vquery = f"""
            SELECT m.nombre 
            FROM laboratorio_medicos m
            WHERE 1=1
                AND m.id = '{vmedico}' 
            """
        r = my_custom_sql(vquery)
        vmedico_datos = ""
        for i in r:
            vmedico_datos = i[0]

        # Imprime la receta en PDF
        imprime_receta(vreceta, dt_archivo, vmedico_datos)

        return redirect('index')
    else:
        vid = idcita
        vquery = f"""
            SELECT a.id, a.fecha, a.hora, a.observaciones, b.nombre, c.nombre, a.consultorio_id, a.cliente_id, d.nombre 
            FROM laboratorio_citas a, laboratorio_clientes b, laboratorio_consultorios c, laboratorio_productos d
            WHERE 1=1
                AND a.id = '{vid}' 
                AND a.cliente_id = b.id 
                AND a.consultorio_id = c.id
                AND a.servicio_id = d.id
            """
        r = my_custom_sql(vquery)
        i = 0
        j2 = ''
        j = '['
        cita_id = ''
        consultorio_id = ''
        cliente_id = ''
        for i in r:
            cita_id = i[0]
            consultorio_id = i[6]
            cliente_id = i[7]
            j += ('{"id": "' + str(i[0]) + '", "fecha": "' + i[1] + '","hora": "' + i[2] + '",' +
                  '"observaciones": "' + i[3] + '",' + '"nombre": "' + i[4] + '",' + '"consultorio": "' +
                  i[5] + '",' + '"consultorio_id": "' + str(i[6]) + '",' + '"cliente_id": "' + str(i[7]) +
                  '",' + '"servicio": "' + str(i[8]) + '"' + '},')
        j += ']'
        j = j[0:len(j) - 2] + ']'
        j2 = json.loads(j)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return render(request, 'atender_cita3.html', {
            'title': 'Atender Consulta',
            'citas': j2,
            'cita_id': cita_id,
            'consultorio_id': consultorio_id,
            'cliente_id': cliente_id,
            'fecha_ini': dt_string
        })


def atender_consuta(request):
    now = datetime.now()
    dt_hoy = now.strftime("%Y-%m-%d")
    dt_hora = now.strftime("%H:%M:%S")
    vfecha = now.strftime("%Y-%m-%d")
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dt_archivo = now.strftime("%d%m%Y%H%M%S")
    checkout_hora = dt_string

    if request.method == 'POST':
        vturno_num = request.POST['turno_num']
        # Busca el tipo de servicio de acuerdo al turno
        vquery = f"""
            SELECT 
                ta.turno_id, 
                ta.producto_id,
                ta.cliente_id
            FROM 
                laboratorio_turnos_agenda ta 
            WHERE 1=1
                AND fecha = '{vfecha}' 
                AND turno_num = '{vturno_num}'
        """
        t = my_custom_sql(vquery)
        vservicio = ''
        vproducto = ''
        vprecio = ''
        if len(t) > 0:
            for tr in t:
                vservicio = tr[0]
                vproducto = tr[1]
                vcliente_id = tr[2]
                vqp = f"""
                    SELECT precio FROM laboratorio_productos WHERE id = '{vproducto}'
                """
                vp = my_custom_sql(vqp)
                for i in vp:
                    vprecio = i[0]

            # Lee todos los datos capturados por el medico
            vreceta = request.POST['txtIndicacionesMedicas']
            vmedico = request.POST['cboMedicos']
            vconsultorio_id = '0'

            medico_id = request.POST['cboMedicos']
            checkin_fecha = request.POST['fecha_ini']
            checkin_edad = request.POST['txtedad']
            checkin_sexo = request.POST['txtsexo']
            checkin_peso = request.POST['txtpeso']
            checkin_talla = request.POST['txttalla']
            checkin_presion_arterial = request.POST['txtpresion']
            checkin_frecuencia_cardiaca = request.POST['txtcardiaca']
            checkin_frecuencia_respiratoria = request.POST['txtrespiratoria']
            checkin_temperatura = request.POST['txttemperatura']
            checkin_resumen = request.POST['txtResumen']
            checkin_exploracion_fisica = request.POST['txtExploracion']
            checkin_resultado_servicios_auxiliares = request.POST['txtSrvAuxiliares']
            checkin_problemas_clinicos = request.POST['txtProblemasClinicos']
            checkin_indicaciones_medicas = request.POST['txtIndicacionesMedicas']
            checkin_pronostico = request.POST['txtPronostico']

            vquery = f"""
                    INSERT INTO laboratorio_citas (consultorio_id,medico_id,cliente_id,fecha,hora,observaciones,checkin_edad,
                        checkin_exploracion_fisica,checkin_fecha,checkin_frecuencia_cardiaca,checkin_frecuencia_respiratoria,
                        checkin_indicaciones_medicas, checkin_peso,checkin_presion_arterial,checkin_problemas_clinicos,
                        checkin_pronostico,checkin_resultado_servicios_auxiliares,checkin_resumen,checkin_sexo,checkin_talla,
                        checkin_temperatura,checkout_hora,servicio_id,precio,turno_num) 
                        VALUES ('{vconsultorio_id}','{vmedico}','{vcliente_id}','{dt_hoy}','{dt_hora}','','{checkin_edad}','{checkin_exploracion_fisica}','{dt_hoy}','{checkin_frecuencia_cardiaca}',
                        '{checkin_frecuencia_respiratoria}','{checkin_indicaciones_medicas}','{checkin_peso}','{checkin_presion_arterial}','{checkin_problemas_clinicos}',
                        '{checkin_pronostico}','{checkin_resultado_servicios_auxiliares}','{checkin_resumen}','{checkin_sexo}','{checkin_talla}','{checkin_temperatura}','{checkout_hora}','{vservicio}','{vprecio}','{vturno_num}')
                """
            my_custom_sql(vquery)

            # Actualiza turno como atendido
            vquery = f"""
                UPDATE laboratorio_turnos_agenda SET hora_atencion = '{dt_hora}'
                WHERE fecha = '{vfecha}' AND turno_num = '{vturno_num}'
            """
            my_custom_sql(vquery)

            # Lee datos de medico
            vquery = f"""
                        SELECT m.nombre, m.cedula
                        FROM laboratorio_medicos m
                        WHERE 1=1
                            AND m.id = '{vmedico}' 
                        """
            print("QUERY MEDICO: ", vquery)
            r = my_custom_sql(vquery)
            vmedico_datos = ""
            for i in r:
                vmedico_datos = i[0] + '|' + str(i[1])

            # Imprime la receta en PDF
            pdf_path = imprime_receta(vreceta, dt_archivo, vmedico_datos)
            # Generate the download URL (assuming your 'download_pdf' URL is set up correctly)
            download_url = reverse('download_pdf', kwargs={'filename': pdf_path.split('/')[-1]})

            # Render the template with the download URL, where you want to show the link
            return render(request, 'temp_pdf.html', {
                'download_url': download_url
            })
        return redirect('index')

    return render(request, 'atender_consulta.html', {
        'title': 'Atender Consulta',
        'fecha_ini': dt_string,
})


def get_medicos(request):
    lista_medicos = list(Medicos.objects.values())

    if len(lista_medicos) > 0:
        data = {'message': "Success", 'medicos': lista_medicos}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)


def get_turno(request, turno_num):
    today = date.today()
    vfecha = today.strftime("%Y-%m-%d")

    vt = f"""
        SELECT hora_atencion FROM laboratorio_turnos_agenda 
        WHERE fecha = '{vfecha}' AND turno_num = '{turno_num}' AND hora_atencion = ''
    """
    lista_turno = my_custom_sql(vt)

    # Si existe el turno y no ha sido atendido
    if len(lista_turno) > 0:
        data = {'message': "Success", 'medicos': lista_turno}
    # Puede existir el turno pero ya fue atendido
    else:
        data = {'message': "0"}

    return JsonResponse(data)

def get_buscaturno(request, turno_num):
    today = date.today()
    vfecha = today.strftime("%Y-%m-%d")

    vt = f"""
        SELECT 
            -- ta.hora_atencion,
            CONCAT(c.nombre,' ', c.apellido_paterno) as nombre
         FROM 
            laboratorio_turnos_agenda ta,
            laboratorio_clientes c             
        WHERE 1=1
            AND fecha = '{vfecha}' 
            AND turno_num = '{turno_num}' 
            AND hora_atencion = ''
            AND c.id = ta.cliente_id
    """
    lista_turno = my_custom_sql(vt)

    # Si existe el turno y no ha sido atendido
    if len(lista_turno) > 0:
        data = {'message': "Success", 'clientes': lista_turno}
    # Puede existir el turno pero ya fue atendido
    else:
        data = {'message': "0"}

    return JsonResponse(data)

def turnos(request):
    if request.method == 'POST':
        vturno = request.POST['btnTurno']
        today = date.today()
        vfecha = today.strftime("%Y-%m-%d")
        vfecha2 = today.strftime("%d-%m-%Y")
        now = datetime.now()
        vhora = now.strftime("%H:%M:%S")
        # Lee el ultimo
        vq = f"""
            SELECT turno_num FROM laboratorio_turnos_agenda WHERE fecha='{vfecha}' ORDER BY id DESC LIMIT 1
            """
        r = my_custom_sql(vq)
        if len(r) > 0:
            for turno in r:
                vnumero = turno[0]
        else:
            vnumero = 0
        vsiguiente = vnumero + 1

        # Crea registro
        Turnos_agenda.objects.create(
            turno_id=vturno,
            turno_num=vsiguiente,
            fecha=vfecha,
            hora=vhora,
            mostrado='N'
        )
        # Imprime ticket
        imprime_ticket(vturno, vsiguiente, vfecha2)

        return redirect('turnos')
    turnos = list(Turnos.objects.values())
    return render(request, 'turnos.html', {
        'title': 'TURNOS',
        'turnos': turnos
    })


def turno_liberar(request):
    today = date.today()
    vfecha = today.strftime("%Y-%m-%d")
    if request.method == 'POST':
        vturno = request.POST['turno_num']
        vproducto = request.POST['cboServicios']
        vquery = f"""
            UPDATE laboratorio_turnos_agenda SET liberado = 'S', producto_id = '{vproducto}' 
            WHERE fecha = '{vfecha}' AND turno_num = {vturno}
        """
        my_custom_sql(vquery)
        print(vquery)
    return render(request, 'turno_liberar.html', {
        'title': 'LIBERAR TURNOS',
    })

def turno_siguiente():
    today = date.today()
    vfecha = today.strftime("%Y-%m-%d")
    vnumero = 0
    # Lee el ultimo
    vq = f"""
        SELECT turno_num FROM laboratorio_turnos_agenda WHERE fecha='{vfecha}' ORDER BY id DESC LIMIT 1
        """
    r = my_custom_sql(vq)
    if len(r) > 0:
        for turno in r:
            vnumero = turno[0]
    else:
        vnumero = 0

    return vnumero + 1

def imprime_receta(vreceta, varchivo, vmedico):
    vpath = "/opt/progs/it911/static/pdfs/"
    varchivo = varchivo + ".pdf"
    # vimagen = 'C:\\Users\\rolme\\Documents\\projects\\laboratorio\\laboratorio\\static\\logo1.jpeg'
    vimagen = '/opt/progs/it911/laboratorio/static/logo1.jpeg'
    vmedico = vmedico.split("|")
    vmedico_nombre = vmedico[0]
    vmedico_cedula = vmedico[1]

    print(vmedico)

    # -*- coding: iso-8859-1 -*-
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', '', 13.0)
    pdf.set_xy(105.0, 8.0)
    pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt='Médico', border=0)
    pdf.set_line_width(0.0)
    pdf.rect(15.0, 15.0, 170.0, 245.0)
    pdf.set_line_width(0.0)
    pdf.rect(95.0, 15.0, 10.0, 10.0)
    pdf.image(vimagen, 20.0, 17.0, link='', type='', w=50.0, h=20.0)
    # pdf.image('logo1.jpeg', 20.0, 17.0, link='', type='', w=50.0, h=20.0)

    pdf.set_xy(20.0, 38.0)
    pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Domicilio:', border=0)
    pdf.set_xy(20.0, 42.0)
    pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Calle Bugambilias #12345', border=0)
    pdf.set_xy(20.0, 46.5)
    pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Colonia: Loma Bonita', border=0)
    pdf.set_xy(20.0, 51.0)
    pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Torreón, Coahuila.', border=0)

    pdf.set_line_width(0.0)
    pdf.line(100.0, 25.0, 100.0, 57.0)
    pdf.set_font('arial', 'B', 14.0)
    pdf.set_xy(100.0, 27.5)
    pdf.cell(ln=0, h=5.5, align='L', w=10.0, txt=vmedico_nombre, border=0)

    pdf.set_xy(100.0, 33.0)
    pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Cédula Prof.:', border=0)
    pdf.set_xy(135.0, 33.0)
    pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt=vmedico_cedula, border=0)

    # pdf.set_xy(125.0, 32.5)
    # pdf.cell(ln=0, h=9.5, align='L', w=60.0, txt='00000001', border=0)
    # pdf.set_font('arial', 'B', 12.0)
    # pdf.set_xy(17.0, 32.5)
    # pdf.cell(ln=0, h=5.0, align='L', w=98.0, txt='COMPANY', border=0)
    # pdf.set_font('arial', '', 12.0)

    pdf.set_line_width(0.0)
    pdf.line(15.0, 57.0, 185.0, 57.0)
    pdf.set_font('times', '', 10.0)
    pdf.set_xy(17.0, 59.0)
    pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='Indicaciones Médicas:', border=0)

    pdf.set_xy(17.0, 65.0)
    pdf.multi_cell(
        h=6.0,
        align='L',
        w=200.0,
        txt=f"""{vreceta}





                Firma doctor
                """,
        border=0)
    pdf.output(vpath + varchivo, 'F')
    return vpath + varchivo

    # subprocess.run(['xdg-open', varchivo])

    # if sys.platform.startswith('win'):
    #     os.startfile(vpath + varchivo)
    # if sys.platform.startswith("linux"):
    #     os.system(f"xdg-open {vpath + varchivo}")
    # elif sys.platform.startswith('darwin'):
    #     # macOS-specific code
    #     os.system(f'open {vpath + varchivo}')

    # download_url = reverse('download_pdf', kwargs={'filename': varchivo})
    # return render(request, 'temp_pdf.html', {
    #     'download_url': download_url
    # })
    # # return redirect(download_url)

def abrir_consultorio(request):
    if request.method == 'POST':
        vcons = request.POST['cboConsultorio']
        consultorio = Consultorios.objects.get(id=vcons)
        consultorio.disponible = "S"

        consultorio.save()

        return redirect('index')
    return render(request, 'abrir_consultorio.html', {
        'title': 'LIBERAR CONSULTORIO'
    })

def turnos_pantalla(request):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    # dt_string = '2024-05-10'
    j2 = []
    # Lee los turnos en espera
    vq = f"""
        SELECT 
            ta.turno_num, 
            ta.consultorio,
            t.descripcion ,
            c.nombre
        FROM 
            laboratorio_turnos_agenda ta,            
            laboratorio_turnos t,
            laboratorio_clientes c         
        WHERE 1=1
            AND fecha = '{dt_string}'
            AND liberado = 'S'
            AND hora_atencion = ''
            AND t.id = ta.turno_id
            AND c.id = ta.cliente_id
        ORDER By turno_num 
    """
    r = my_custom_sql(vq)
    i = 0
    j = '['
    consultorio = ''
    turno = ''
    for i in r:
        j += ('{"consultorio": "' + str(i[1]) + '", "turno": "' + str(i[0]) + ' - ' + i[3] + '", "descripcion": "' + str(i[2]) + '"' + '},')

    j += ']'
    j = j[0:len(j) - 2] + ']'
    if len(j) > 3:
        j2 = json.loads(j)

    return render(request, 'turnos_pantalla.html', {
            'title': 'TURNOS',
            'turnos': j2
        })

def turnos_pantalla3(request):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    # dt_string = '2024-05-10'
    j2 = []
    # 1 Limpia turnos mostrados solo el primero cuando sean mas de 10 en la fila
    vq = "SELECT turno_num FROM laboratorio_consultorios_turnos ORDER By turno_num"
    r = my_custom_sql(vq)
    if len(r) > 10:
        for turno in r:
            vborra_turno = r[0]
            vq2 = f""" DELETE FROM laboratorio_consultorios_turnos WHERE turno_num = {vborra_turno} """
            my_custom_sql(vq2)
    # vq = "DELETE FROM laboratorio_Consultorios_Turnos"
    # my_custom_sql(vq)

    # 2 Lee consultorios disponibles
    vquery = f"""
        SELECT c.id, c.tipo_id, c.nombre
        FROM 
            laboratorio_consultorios c
        WHERE 1=1
            AND c.disponible = 'S'
    """
    r = my_custom_sql(vquery)

    if len(r) > 0:
        for i in r:
            vcons_id = i[0]
            vtipo_id = i[1]
            vcons_nombre = i[2]
            # 3 Lee turnos de ese tipo de servicio del consultorio.
            vquery = f"""
                SELECT ta.turno_num, ta.id
                FROM 
                    laboratorio_turnos_agenda ta
                WHERE 1=1
                    AND ta.fecha = '{dt_string}'
                    AND ta.turno_id = '{vtipo_id}'
                    -- AND ta.mostrado = 'N'
                    AND ta.liberado = 'S'
                    AND ta.hora_atencion = ''
                LIMIT 1

            """
            turnos = my_custom_sql(vquery)
            if len(turnos) > 0:
                for t in turnos:
                    vturno_num = t[0]
                    vturno_id = t[1]
                    # Crear el registro en la tabla de turnos a mostrar
                    vinsert = f"""
                        INSERT INTO laboratorio_consultorios_turnos (cons_id, turno_num, nombre) VALUES('{vcons_id}','{vturno_num}','{vcons_nombre}' )
                    """
                    my_custom_sql(vinsert)
                    # # Consultorio marcado como ocupado
                    # vquery = f"""
                    #     UPDATE laboratorio_consultorios
                    #     SET disponible = 'N'
                    #     WHERE id = {vcons_id}
                    # """
                    # my_custom_sql(vquery)

                    # # ACTUALIZA EL TURNO COMO YA MOSTRADO
                    # vquery = f"""
                    #     UPDATE laboratorio_turnos_agenda
                    #     SET mostrado = 'S'
                    #     WHERE 1=1
                    #     AND id = {vturno_id}
                    # """
                    # my_custom_sql(vquery)

                    # 4 Lee la tabla de turnos
                    vquery = f"""
                        SELECT c.cons_id, c.turno_num, c.nombre
                        FROM 
                            laboratorio_consultorios_turnos c
                        WHERE 1=1
                    """
                    r = my_custom_sql(vquery)
                    i = 0
                    j2 = ''
                    j = '['
                    consultorio = ''
                    turno = ''
                    if len(r) > 0:
                        for i in r:
                            consultorio = i[0]
                            turno = i[1]
                            turno_id = i[2]
                            j += ('{"consultorio": "' + str(i[0]) + '", "turno": "' + str(i[1]) + '", "nombre": "' + str(i[2]) + '"' + '},')

                        j += ']'
                        j = j[0:len(j) - 2] + ']'
                        j2 = json.loads(j)
    else:
        j2 = []
    return render(request, 'turnos_pantalla.html', {
        'title': 'TURNOS',
        'turnos': j2
    })


def imprime_ticket(vturno, vsiguiente, vfecha):
    vdescripcion = vturno
    vsiguiente = str(vsiguiente)
    now = datetime.now()
    dt_archivo = now.strftime("%d%m%Y%H%M%S")
    varchivo = dt_archivo + ".bin"

    # Lee el ultimo
    # vq = f"""
    #     SELECT descripcion FROM laboratorio_turnos WHERE id='{vturno}'
    #     """
    # r = my_custom_sql(vq)
    # if len(r) > 0:
    #     for turno in r:
    #         vdescripcion = turno[0]

    with open(varchivo, "wb") as f:
        f.write(b'\x1B\x40')  # Initialize printer
        # f.write(b'\x1B\x61\x00') # Left
        f.write(b'\x1B\x61\x01') # Center
        # f.write(b'\x1B\x61\x02') # Right
        f.write(b'\x1D\x21\x11')  # Double height & width (big text)
        f.write(b'Dr.MED\n')  # Print text
        f.write(b'\x1B\x21\x10')  # Double height text
        f.write(b'Comprometidos con tu salud\n\n')  # Print text
        f.write(b'\x1D\x21\x00')  # Reset to normal size
        f.write(b'\x1B\x45\x01')  # Enable Bold
        f.write(b'\x1B\x21\x10')  # Double height text
        # f.write(b'TURNO\n\n')  # Print text
        f.write(vdescripcion.encode('utf-8'))  # Write text in bold
        f.write(b'\n\n')  # Enable Bold
        f.write(b'TURNO: ')  # Print text
        f.write(vsiguiente.encode('utf-8'))  # Write text in bold
        f.write(b'\x1B\x45\x00') # Disable BOLD
        f.write(b'\x1D\x21\x00')  # Reset to normal size
        f.write(b'\x1B\x64\x02')  # Feed 2 lines
        f.write(b'\n\n')  # Enable Bold
        f.write(b'\n\n')  # Enable Bold
        f.write(b'\x1D\x56\x00')  # Cut paper

    printer_name = "principal"  # Replace with your printer's name
    os.system(f"lp -d {printer_name} -o raw {varchivo} &")

# Function to replace newlines in the text
def escape_newlines(data):
    if isinstance(data, str):
        return data.replace("\n", "<br>")
    return data

    # if isinstance(data, str):
    #     return data.replace("\n", "\\n")
    # elif isinstance(data, dict):
    #     return {key: escape_newlines(value) for key, value in data.items()}
    # elif isinstance(data, list):
    #     return [escape_newlines(item) for item in data]
    # return data

def my_custom_sql(vquery):
    cursor = connection.cursor()
    cursor.execute(vquery)
    row = cursor.fetchall()
    return row

def serve_pdf(request, filename):
    # Path to the directory where PDFs are stored
    pdf_directory = '/opt/progs/it911/static/pdfs/'
    pdf_path = os.path.join(pdf_directory, filename)
    print('EN EL PDF: ', pdf_path)
    if os.path.exists(pdf_path):
        # Open the file in binary mode and return it as a response
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    else:
        raise Http404("PDF not found")
