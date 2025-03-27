from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultorios/', views.consultorios, name='consultorios'),
    path('consultorio_mantto/<int:id>', views.consultorio_mantto, name='consultorio_mantto'),
    path('medicos/', views.medicos, name='medicos'),
    path('medicos_mantto/<int:id>', views.medicos_mantto, name='medicos_mantto'),
    path('productos/<int:id>', views.productos, name='productos'),
    path('productos/', views.productos, name='productos'),
    path('clientes/<int:id>', views.clientes, name='clientes'),
    path('clientes/', views.clientes, name='clientes'),
    path('codigos_postales/<int:cp>', views.get_codigos_postales, name='get_codigos_postales'),
    path('citas/', views.citas, name='citas'),
    path('get_consultorios/', views.get_consultorios, name='get_consultorios'),
    path('get_disponible/<str:idConsultorio>/<str:fecha>', views.get_disponible, name='get_disponible'),
    path('agendar_cita/', views.agendar_cita, name='agendar_cita'),
    path('captura_reserva/<int:idcons>/<str:fecha>/<str:hora>/<int:servicio>', views.captura_reserva, name='captura_reserva'),
    path('get_clientes/<str:inCliente>', views.get_clientes, name='get_clientes'),
    path('graba_reserva/', views.graba_reserva, name='graba_reserva'),
    path('informe_citas/', views.informe_citas, name='informe_citas'),
    path('atender_cita/', views.atender_cita, name='atender_cita'),
    path('atender_cita3/<int:idcita>', views.atender_cita3, name='atender_cita3'),
    path('get_medicos/', views.get_medicos, name='get_medicos'),
    path('get_servicios/', views.get_servicios, name='get_servicios'),
    path('turnos/', views.turnos, name='turnos'),
    path('turnos_pantalla/', views.turnos_pantalla, name='turnos_pantalla'),
    path('abrir_consultorio/', views.abrir_consultorio, name='abrir_consultorio'),
    path('turno_liberar/', views.turno_liberar, name='turno_liberar'),
    path('atender_consuta/', views.atender_consuta, name='atender_consuta'),
    path('get_turno/<str:turno_num>', views.get_turno, name='get_turno'),
    # para downloads
    path('download_pdf/<str:filename>/', views.serve_pdf, name='download_pdf'),

]
