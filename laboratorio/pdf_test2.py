# -*- coding: iso-8859-1 -*-

import os
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('helvetica', '', 13.0)
pdf.set_xy(105.0, 8.0)
pdf.cell(ln=0, h=22.0, align='C', w=75.0, txt='Médico', border=0)
pdf.set_line_width(0.0)
pdf.rect(15.0, 15.0, 170.0, 245.0)
pdf.set_line_width(0.0)
pdf.rect(95.0, 15.0, 10.0, 10.0)
pdf.image('static/logo1.jpeg', 20.0, 17.0, link='', type='', w=50.0, h=20.0)
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
pdf.cell(ln=0, h=5.5, align='L', w=10.0, txt='Dr. Pedro Pérez', border=0)

pdf.set_xy(100.0, 33.0)
pdf.cell(ln=0, h=7.0, align='L', w=60.0, txt='Cédula Prof.:', border=0)
pdf.set_xy(135.0, 33.0)
pdf.cell(ln=0, h=7.0, align='L', w=40.0, txt='1234567890', border=0)

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
         txt=f"""
            Tomar 2 MITROCIN 500 cada 8 horas
            Inyeccion de INTRAPIERNOSA MITILIN 200 por 4 días
            Salir a caminar 30 minutos diarios
            
            
            
            
            
            Firma doctor
            """,
         border=0)


# pdf.set_line_width(0.0)
# pdf.line(15.0, 77.0, 185.0, 77.0)
# pdf.set_xy(17.0, 80.0)
# pdf.cell(ln=0, h=5.0, align='L', w=15.0, txt='VAT:', border=0)
# pdf.set_xy(35.0, 80.0)
# pdf.cell(ln=0, h=5.0, align='L', w=70.0, txt='Responsable', border=0)
# pdf.set_xy(115.0, 80.0)
# pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='Tax ID:', border=0)
# pdf.set_xy(135.0, 80.0)
# pdf.cell(ln=0, h=5.0, align='L', w=40.0, txt='10-12345678-9', border=0)
# pdf.set_line_width(0.0)
# pdf.line(15.0, 88.0, 185.0, 88.0)
# pdf.set_xy(17.0, 90.0)
# pdf.cell(ln=0, h=5.0, align='L', w=48.0, txt='Due Date:', border=0)
# pdf.set_xy(65.0, 90.0)
# pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='23/07/1978', border=0)
# pdf.set_xy(92.0, 90.0)
# pdf.cell(ln=0, h=5.0, align='L', w=43.0, txt='Period', border=0)
# pdf.set_xy(125.0, 90.0)
# pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='01/01/2009', border=0)
# pdf.set_xy(150.0, 90.0)
# pdf.cell(ln=0, h=5.0, align='L', w=20.0, txt='31/01/2009', border=0)
# pdf.set_line_width(0.0)
# pdf.line(15.0, 95.0, 185.0, 95.0)
# pdf.set_line_width(0.0)
# pdf.line(155.0, 95.0, 155.0, 230.0)
# pdf.set_xy(20.0, 97.0)
# pdf.cell(ln=0, h=5.0, align='L', w=125.0, txt='Description', border=0)
# pdf.set_xy(160.0, 97.0)
# pdf.cell(ln=0, h=5.0, align='R', w=20.0, txt='Amount', border=0)
# pdf.set_line_width(0.0)
# pdf.line(15.0, 102.0, 185.0, 102.0)
# pdf.set_xy(20.0, 103.0)
# pdf.cell(ln=0, h=7.0, align='L', w=125.0, txt='Esto es una prueba y no es v\xe1lido como factura', border=0)
# pdf.set_xy(160.0, 103.0)
# pdf.cell(ln=0, h=7.0, align='R', w=20.0, txt='100,00', border=0)
# pdf.set_line_width(0.0)
# pdf.line(15.0, 230.0, 185.0, 230.0)
# pdf.set_xy(20.0, 233.0)
# pdf.cell(ln=0, h=5.0, align='L', w=95.0, txt='CAE N\xba', border=0)
# pdf.set_xy(45.0, 233.0)
# pdf.cell(ln=0, h=5.0, align='L', w=30.0, txt='01234567890', border=0)
# pdf.set_font('arial', '', 12.0)
# pdf.set_xy(105.0, 234.0)
# pdf.cell(ln=0, h=9.0, align='R', w=45.0, txt='Subtotal:', border=0)
# pdf.set_font('arial', 'B', 12.0)
# pdf.set_xy(145.0, 234.0)
# pdf.cell(ln=0, h=9.0, align='R', w=33.0, txt='100,00', border=0)
# pdf.set_font('arial', '', 10.0)
# pdf.set_xy(20.0, 238.0)
# pdf.cell(ln=0, h=5.0, align='L', w=95.0, txt='Fecha Vto. CAE:', border=0)
# pdf.set_xy(55.0, 238.0)
# pdf.cell(ln=0, h=5.0, align='L', w=30.0, txt='19/02/2009', border=0)
# pdf.set_font('arial', '', 12.0)
# pdf.set_xy(125.0, 241.0)
# pdf.cell(ln=0, h=9.0, align='R', w=25.0, txt='VAT 21%:', border=0)
# pdf.set_font('arial', 'B', 12.0)
# pdf.set_xy(145.0, 241.0)
# pdf.cell(ln=0, h=9.0, align='R', w=33.0, txt='21,00', border=0)
# pdf.interleaved2of5('012345678905', 20.0, 243.5, w=0.75)
# pdf.set_font('arial', 'B', 12.0)
# pdf.set_xy(105.0, 251.0)
# pdf.cell(ln=0, h=9.0, align='R', w=73.0, txt='121,00', border=0)
# pdf.set_font('arial', '', 12.0)
# pdf.set_xy(125.0, 251.0)
# pdf.cell(ln=0, h=9.0, align='R', w=25.0, txt='Total:', border=0)
# pdf.set_line_width(0.0)
# pdf.rect(155.0, 252.0, 25.0, 7.0)
# pdf.set_font('courier', '', 10.0)
# pdf.set_xy(20.0, 253.0)
# pdf.cell(ln=0, h=7.0, align='L', w=120.0, txt='012345678905', border=0)
pdf.output('invoice.pdf', 'F')

import sys
if sys.platform.startswith("linux"):
    os.system("xdg-open ./invoice.pdf")
else:
    varchivo =
    os.system("invoice.pdf")
