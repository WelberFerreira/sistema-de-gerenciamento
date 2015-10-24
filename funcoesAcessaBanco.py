# -*- coding: utf-8 -*-
"""
Created on mon mar 23 16:38:00 2015

@author: familia
"""
#database.py
import os.path
import psycopg2
#import pyproj
#from shapely.geometry import Polygon
#import shapely.wkt

##############################################################
# Edit these constants as necessary to match your setup.
POSTGIS_DBNAME = "outorgas"
POSTGIS_USERNAME = "pi"
POSTGIS_PASSWORD = "lua2012"
# ADICIONEI A PORTA
POSTGIS_PORT = "5433"
#############################################################
### alterei o nome da funcao de open para open_conection
def open_conection():
    global connection, cursor
    params = []
    params.append("dbname=" + POSTGIS_DBNAME)
    params.append("port=" + POSTGIS_PORT)	
    if POSTGIS_USERNAME != None:
	params.append("user=" + POSTGIS_USERNAME)
    if POSTGIS_PASSWORD != None:
	params.append("password=" + POSTGIS_PASSWORD)
    
    connection = psycopg2.connect(" ".join(params))
    cursor = connection.cursor()
      

#########Retorna o id do rio associado a area em que o ponto esta inserido
def returnIdRiver(x,y):
    global cursor
# hca_gm = geometria do poligono da area
# hca_pk = id do poligono envolvente ao ponto
# hin_drs_pk = id do rio associado ao poligono
# pghgt_hydrographic_catchment_area
    cursor.execute("SELECT hin_drs_pk FROM pghgt_hydro_intel WHERE hin_hca_pk = " +
		   "(SELECT hca_pk FROM pghgt_hydrographic_catchment_area WHERE " +
		   "ST_CONTAINS(hca_gm,ST_GeomFromText('POINT(" + str(x) + " " + str(y) + ")', 4291)))")
    for row in cursor:
      	id = row[0]
    return id

######### Retorna a area de contribuicao do ponto
def returnAreaMontante(id_river):
    	global cursor
	# id_river = id do rio associado ao poligono
	# pghgt_drainage_stretch = hidrografia
    	cursor.execute("SELECT drs_nu_upstreamarea FROM pghgt_drainage_stretch WHERE drs_pk = " +
		  	str(id_river))
	
	for row in cursor:
      		area = row[0]
	return area


######### Retorna ids dos rios a montantes
#### Usa a funcao pghfn_upstreamstretches(integer)
def returnIdsRiosMontante(id_river):
    	global cursor
	# id_river = id do rio associado ao poligono
	# pghgt_drainage_stretch = hidrografia
    	cursor.execute("SELECT pghfn_upstreamstretches(" + str(id_river) + ")")
	ids = []
	for row in cursor:
      		ids.append(row)
	return ids

######### Retorna poligono das areas de contribuicao
def returnGeomAreaMontante(id_river):
    	global cursor
	# id_river = id do rio associado ao poligono

    	cursor.execute(
		"SELECT ST_AsText(geom) FROM (SELECT (ST_Dump(g.geom)).* " +
		"FROM (SELECT ST_Union(ARRAY(" +
		"SELECT hca_gm FROM pghgt_hydrographic_catchment_area WHERE hca_pk IN (" +
		"SELECT hin_hca_pk FROM pghgt_hydro_intel WHERE hin_drs_pk IN (" +
		"SELECT pghfn_upstreamstretches(" + str(id_river) + ")))" +
		"))::geometry AS geom) AS g) j")

	for row in cursor:
      		pol = row[0]
	return pol

################## Retorna id das outorgas --- new
def getIdOutorgas(id_river):
    global cursor
    cursor.execute(
		   "SELECT out_pk FROM pghgt_outorga out, " +
		   "(SELECT drs.drs_pk, drs.drs_hca_pk as hca_pk, hca.hca_gm as hca_gm " +
		   "FROM pghgt_drainage_stretch drs, pghgt_hydrographic_catchment_area hca, " +
		   "(SELECT pghfn_upstreamstretches(" + str(id_river) + ") as drs_pk) as a " +
		   "WHERE drs.drs_pk = a.drs_pk AND hca.hca_pk = drs.drs_hca_pk) as a " +
		   "WHERE ST_INTERSECTS(a.hca_gm, out.out_gm) AND (a.hca_gm && out.out_gm)"
		  )
    ids = []
    for row in cursor:
	ids.append(row)
    return ids
  
################## Retorna soma das vazoes das outorgas --- new
def getSomaVazOutorgas(id_river):
    global cursor
    cursor.execute( "SELECT " +
		   "SUM(out_q_jan), SUM(out_q_fev), SUM(out_q_mar), SUM(out_q_abr), " +
		   "SUM(out_q_mai), SUM(out_q_jun), SUM(out_q_jul), SUM(out_q_ago), " +
		   "SUM(out_q_set), SUM(out_q_out), SUM(out_q_nov), SUM(out_q_dez) " +
		   "FROM pghgt_outorga out, " +
		   "(SELECT drs.drs_pk, drs.drs_hca_pk as hca_pk, hca.hca_gm as hca_gm " +
		   "FROM pghgt_drainage_stretch drs, pghgt_hydrographic_catchment_area hca, " +
		   "(SELECT pghfn_upstreamstretches(" + str(id_river) + ") as drs_pk) as a " +
		   "WHERE drs.drs_pk = a.drs_pk AND hca.hca_pk = drs.drs_hca_pk) as a " +
		   "WHERE ST_INTERSECTS(a.hca_gm, out.out_gm) AND (a.hca_gm && out.out_gm)"
		  )

    vazoes = []
    for row in cursor:
	for i in row:
	        vazoes.append(i)
    return vazoes

################## Retorna soma das vazoes das outorgas --- new
def getOutorgas(id_river):
    global cursor
    cursor.execute( "SELECT " +
		   "out_cpf, out_cnpj, out_end_emprend, out_q_jan, out_q_fev, out_q_mar, " +
		   "out_q_abr, out_q_mai, out_q_jun, out_q_jul, out_q_ago, out_q_set, " +
		   "out_q_out, out_q_nov, out_q_dez " +
		   "SELECT sum(out_vaz) FROM pghgt_outorga out, " +
		   "(SELECT drs.drs_pk, drs.drs_hca_pk as hca_pk, hca.hca_gm as hca_gm " +
		   "FROM pghgt_drainage_stretch drs, pghgt_hydrographic_catchment_area hca, " +
		   "(SELECT pghfn_upstreamstretches(" + str(id_river) + ") as drs_pk) as a " +
		   "WHERE drs.drs_pk = a.drs_pk AND hca.hca_pk = drs.drs_hca_pk) as a " +
		   "WHERE ST_INTERSECTS(a.hca_gm, out.out_gm) AND (a.hca_gm && out.out_gm)"
		  )

    for row in cursor:
	vaz = row[0]
    return vaz

################## Retorna qmmm da uh
def getQmmm(x,y):
    global cursor
    cursor.execute( "SELECT DISTINCT" +
			"qmmm_jan, qmmm_fev, qmmm_mar, qmmm_abr, qmmm_mai, "
			"qmmm_jun, qmmm_jul, qmmm_ago, qmmm_set, qmmm_out, "
			"qmmm_nov, qmmm_dez FROM pghgt_uh as uh "
			"WHERE ST_INTERSECTS(uh.uh_gm, ST_GeomFromText('POINT(" + str(x) + " " + str(y) + ")', 4291)) "
			"AND (uh.uh_gm && ST_GeomFromText('POINT(" + str(x) + " " + str(y) + ")', 4291))"
		  )
    qmmm = []
    for row in cursor:
	for i in row:
	        qmmm.append(i)
    return qmmm	
	
################## Retorna outorgas --- old
def getOutorgasOld(limite):
    global cursor
    cursor.execute("SELECT sum(vaz_janeiro), sum(vaz_fevereiro), sum(vaz_marco), " 	 +
		   "       sum(vaz_abril), sum(vaz_maio), sum(vaz_junho), "		 +
		   "	   sum(vaz_julho), sum(vaz_agosto), sum(vaz_setembro), "	 +
		   "	   sum(vaz_outubro), sum(vaz_novembro), sum(vaz_dezembro)" 	 +
		   " from out_ WHERE ST_CONTAINS (ST_GeomFromEWKT('" + limite + "'), position)")
    vazoes = []
    for row in cursor:
	for i in row:
	        vazoes.append(i)
    return vazoes

################################### Retorna as vazoes especificas
def getQmmm(id_sub_bacia):
    global cursor
    cursor.execute("SELECT 0.8 * qmmm_jan, 0.8 * qmmm_fev, 0.8 * qmmm_mar, " 	 +
		   "       0.8 * qmmm_abr, 0.8 * qmmm_mai, 0.8 * qmmm_jun, "	 +
		   "	   0.8 * qmmm_jul, 0.8 * qmmm_ago, 0.8 * qmmm_set, "	 +
		   "	   0.8 * qmmm_out, 0.8 * qmmm_nov, 0.8 * qmmm_dez  " 	 +
		   " 	   from uhs WHERE id = " + str(id_sub_bacia))
    qmmm = []
    for row in cursor:
	for i in row:
	        qmmm.append(i)
    return qmmm

#################################### Retorna a view contendo todos os dados para atualizar
########## exemplo curs.execute("SELECT name,age,dob,address FROM TABLENAME WHERE pmrn=%s", (self.pmrn,))
def getOut_by_cpf(cpf):
    global cursor
    cursor.execute("SELECT out_id, processoid, modalidade, quant_out, finalidade, interessado,"  +
           " endereco, cpf, tipo_out, dt_extrat, dt_valid," +
           " vaz_janeiro, vaz_fevereiro, vaz_marco," +
           " vaz_abril, vaz_maio, vaz_junho," +
           " vaz_julho, vaz_agosto, vaz_setembro," +
           " vaz_outubro, vaz_novembro, vaz_dezembro" +
           " from out_teste WHERE cpf = %s", (cpf,)) # para o psycopg2 tem que ter esse conversor de %s para adequar ńumero para string
    dados = []   
    for row in cursor:
        dados.append(row)
    return dados


############################3 Retorna a view contendo todos os dados da interferencia a partir do id
def getOut_by_id(id):
    global cursor
    cursor.execute("SELECT out_id, processoid, modalidade, quant_out, finalidade, interessado,"  +
           " endereco, cpf, tipo_out, dt_extrat, dt_valid," +
           " vaz_janeiro, vaz_fevereiro, vaz_marco," +
           " vaz_abril, vaz_maio, vaz_junho," +
           " vaz_julho, vaz_agosto, vaz_setembro," +
           " vaz_outubro, vaz_novembro, vaz_dezembro" +
           " from out_teste WHERE out_id = %s", (id,)) # para o psycopg2 tem que ter esse conversor de %s para adequar ńumero para string
    dados = []   
    for row in cursor:
        dados.append(row)
    return dados
