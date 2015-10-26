#!/usr/bin/python
# -*- coding: cp1252 -*-
# Consulta o banco somando as vazoes para cada mes do ano

import cgi
import os.path, sys
import psycopg2
import funcoesAcessaBanco

connection = psycopg2.connect("dbname=outorgas port=#### user=pi password=####")
cursor = connection.cursor()

FOOTER = "</body></html>"

meses = ['janeiro', 'fevereiro', 'mar&ccedil;o', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
labels = ['CPF','CNPJ','Endere&ccedil;o','janeiro', 'fevereiro', 'mar&ccedil;o', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

form = cgi.FieldStorage()

print 'Content-Type: text/html; charset=UTF-8\n\n'
print '<!DOCTYPE html>'
print '<html lang="en">'
print '    <head>'
print '        <meta charset="utf-8">'
print '        <meta http-equiv="X-UA-Compatible" content="IE=edge">'
print '        <meta name="viewport" content="width=device-width, initial-scale=1.0">'
print '        <meta name="description" content="Monitoramento de Aguas Superficiais - Dados de Outorga">'
print '        <meta name="author" content="Welber">'
print '        <title>Monitoramento de &Aacute;guas Superficiais - Dados de Outorga</title>'
print '        <!-- Bootstrap core CSS -->'
print '        <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">'
print '        <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->'
print '        <!--[if lt IE 9]>'
print '          <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>'
print '          <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>'
print '        <![endif]-->'
print '    </head>'

print '        <div class="container">'
print '            <table style="width: 100%;" border="0">'
print '                <tbody style="text-align: left;">'
print '                    <tr style="text-align: left; height: 20px;">'
print '                        <td style="background-color: #bfefff; text-align: center;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;">:. Disponibilidade H&iacute;Â­drica</span></span></a><br /></td>'
print '                    </tr>'
print '                    <tr style="text-align: left;">'
print '                        <td colspan="6" valign="top">'
print '                            <p></p>'
print '                            <p style="text-align: center;"><span style="font-size: 10pt;"><strong>MONITORAMENTO DE &Aacute;GUAS SUPERFICIAIS</strong></span><br /></p>'
print '                            <p style="text-align: center;"><span style="font-size: 10pt;"><strong>Sistema de gerenciamento de outorgas</strong></span></p>'
#print '                            <span style="font-size: 8pt;"><span style="color: #006cb7;"><em><a target="_self" href="index.php?option=com_content&amp;view=article&amp;id=993:porbacias&amp;catid=81">Bacias</a></em></span></span>'
print '                        </td>'
print '                    </tr>'
print '                </tbody>'
print '            </table>'

#try:
#Variaveis
x = float(form['x'].value)
y = float(form['y'].value)
funcoesAcessaBanco.open_conection()
id_river = funcoesAcessaBanco.returnIdRiver(x,y)
area_montante = float(funcoesAcessaBanco.returnAreaMontante(id_river))
data = funcoesAcessaBanco.getQmmmByXY(x,y)
#areaUh = data[0][0]
areaUh = float(327.36696037)
coef = float(areaUh/area_montante)
vazoes = funcoesAcessaBanco.getSomaVazOutorgas(id_river)
outorgas = funcoesAcessaBanco.getInfoOutorgas(id_river)

####################################
##### Dados de Disponibilidade
print '<p>'
print "Abaixo s&atilde;o listadas as vaz&otilde;es j&aacute; outorgadas para cada mes do ano"
print '<br>'
print '        <div class="container">'
print '            <table style="width: 100%;" border="0">'
print '                <tbody style="text-align: left;">'

print '                    <tr style="text-align: left; height: 20px;">'
print '                 	<td style="background-color: #ffffff; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;">', '	' , '</span></span></a><br />'
for mes in meses:
	print '                 <td style="background-color: #e3faf1; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;">', mes, '</span></span></a><br />'
	print '			</td>'
print '        	           </tr>'

print '			   <tr>'
print '                 	<td style="background-color: #ffffff; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;">', 'Vaz&atilde;o regionalizada menos outorgada', '</span></span></a><br />'
#get Qmmm
for i in range(12):
	print '                 <td style="background-color: #e3faf1; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;">', vazoes[i], '</span></span></a><br />'
print '			   </tr>'

print '			   <tr>'
print '                 	<td style="background-color: #ffffff; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;">', 'Qmmm', '</span></span></a><br />'
#get Qmmm
#vazao regionalizada menos somatoria das vazoes outorgadas a montante
for i in range(1,13):
	print '                 <td style="background-color: #e3faf1; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;"> %.2f </span></span></a><br />' %((coef * float(data[0][i]))-vazoes[i-1])
print '			   </tr>'

print '			   <tr>'
print '                 	<td style="background-color: #ffffff; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;">', 'M&aacute;ximo por usu&aacute;rio ', '</span></span></a><br />'
#get Vazao limite por usuario
#20% dos 80% da vazao regionalizada
for i in range(1,13):
	print '                 <td style="background-color: #e3faf1; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;"> %.2f </span></span></a><br />'  %(0.2 * (0.8*(coef * data[0][i])))
print '			   </tr>'
print '                </tbody>'
print '            </table>'
print '        </div>'

#############
print '        <div class="space">'
print '            <table style="width: 100%;" border="0">'
print '                <tbody style="text-align: left;">'
print '                    <tr style="text-align: left; height: 20px;">'
print '                        <td style="background-color: #ffffff; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;"> </span></span></a><br />'
print '			       </td>'
print '         	   </tr>'

print '                </tbody>'
print '            </table>'
print '        </div>'

############## Insercao de dados

print '                    <form style="text-align: center;" method="POST" action="digitaInfoOut.py" role="form">'
print '<input type="hidden" name="x" value ='+ str(x) + '>'
print '<input type="hidden" name="y" value ='+ str(y) + '>'
print '                        <p><input type="submit" value="Para inserir uma nova outorga clique aqui: " class="btn btn-primary"></p>'
print '                    </form>'
print '<p>'

####################################
#Outorgas Emitidas
####################################

print '        <div class="space">'
print '            <table style="width: 100%;" border="0">'
print '                <tbody style="text-align: left;">'
print '                    <tr style="text-align: left; height: 20px;">'
print '                        <td style="background-color: #ffffff; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #006cb7;"> </span></span></a><br />'
print '			       </td>'
print '         	   </tr>'

print '                </tbody>'
print '            </table>'
print '        </div>'

print '        <div class="out">'
print '            <table style="width: 100%;" border="1">'
print '                <tbody style="text-align: left;">'
print '                    <tr style="text-align: left; height: 20px;">'
for label in labels:
	print '                 <td style="background-color: #c5b7b7; text-align: center;" colspan="2" valign="middle"><span style="font-size: 10pt;"><b><span style="color: #000000;">', label, '</span></span></a><br />'
print '         	   </tr>'

for outorga in outorgas:
	print '                    <tr style="text-align: left; height: 20px;">'
	#outorgas
	for  data in outorga:
		if data is None:
			print '                        <td style="background-color: #c5b7b7; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #000000;">  </span></span></a><br />'
			print '			       </td>'
		else:
			print '                        <td style="background-color: #c5b7b7; text-align: justify;" colspan="2" valign="middle"><span style="font-size: 10pt;"><span style="color: #000000;">', data, '</span></span></a><br />'
			print '			       </td>'
	print '         	   </tr>'

print '                </tbody>'
print '            </table>'
print '        </div>'

connection.commit()

#except:
#	print "Insira a coordenada correta"

print FOOTER
