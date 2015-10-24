#!/usr/bin/python
# -*- coding: cp1252 -*-
# Consulta o banco somando as vazoes para cada mes do ano

import cgi
import os.path, sys
import psycopg2
import funcoesAcessaBanco

connection = psycopg2.connect("dbname=outorgas port=5433 user=pi password=lua2012")
cursor = connection.cursor()

HEADER = "Content-Type: text/html; charset=UTF-8\n\n" \
        + "<html><head><title>Sistema de gerenciamento de outorgas</title>" \
        + "</head><body>"

FOOTER = "</body></html>"

meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

form = cgi.FieldStorage()

print HEADER
print '<b>'+ "Sistema de gerenciamento de outorgas" +'</b>'
print '<p>'


try:
	x = float(form['x'].value)
	y = float(form['y'].value)
	funcoesAcessaBanco.open_conection()
	id_river = funcoesAcessaBanco.returnIdRiver(x,y)
	
	area_montante = funcoesAcessaBanco.returnAreaMontante(id_river)
	
	qmmm = funcoesAcessaBanco.getQmmm(x,y)
	
	vazoes = funcoesAcessaBanco.getSomaVazOutorgas(id_river)
		
	#connection.commit() 
	
	print '<p>'
	print "Abaixo s&atilde;o listadas as vaz&otilde;es j&aacute; outorgadas para cada mes do ano"
	print '<br>'
	print '<table>'
	print '<tr>'
	print '<td>	</td>'
	for mes in meses:
		print '  <td>', mes, '| </td>'	
	print '</tr>'
	
	print '<tr>'
	print '<td><b>Vaz&atilde;o outorgada |</td>'
	for i in range(12):
		print '  <td>', vazoes[i], '| </td>'
	print '</tr>'

	"""
	print '<tr>'
	print '<td><b>Qmmm |</td>'
	for i in range(12):
		print '  <td>', qmmm[i], '| </td>'
	print '</tr>'
	"""

	print '</table>'
	
	connection.commit()	

except:
	print "Insira a coordenada correta"

print '<p>'
print '<form method="POST" action="digitaInfoOut.py" >'
print '<input type="hidden" name="x" value ='+ str(x) + '>'
print '<input type="hidden" name="y" value ='+ str(y) + '>'
print '<p>'
print '<input type="submit" value = "Para inserir outorga clique aqui: "'
print '<br>'
print '</form>'

print FOOTER

	#print '<td> <b>M&ecirc;s</td>'
