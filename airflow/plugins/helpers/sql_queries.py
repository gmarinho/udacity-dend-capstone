class SqlQueries:
    dimcity_insert = ("""
        SELECT DISTINCT cmb  as city_id,
				municipio as city_name,
				uf as state,
				'Brazil' as country
            FROM empresa_report er 
    """)

    categories_insert = ("""
 SELECT DISTINCT categoria_produto_id as category_id,
				descricao  as category_name,
				categoria_mae as macro_category,
				descricao_categoria_nivel1  as description
FROM app_categoria_nielsen acn
    """)

    time_insert = ("""
SELECT DISTINCT date(aegw.data_emissao), extract(day from data_emissao), extract(week from data_emissao), 
               extract(month from data_emissao), extract(year from data_emissao), extract(dayofweek from data_emissao)
FROM app_ean_genuino_weekly aegw
    """)

    product_sales_insert = ("""
 SELECT ap.codigo_ean_gapp as product_id,
	   ap.descricao as name,
	   ap.categoria_relatorio_id as category_id,
	   er.cmb  as city_id,
	   SUM(aegw.valor) as total_sales,
	   sum(aegw.qtd) as total_volume,
       date(aegw.data_emissao) as date_id,
	   ap.unidade_volume  as unit
FROM app_ean_genuino_weekly aegw JOIN app_produto ap
	ON aegw.ean_genuino = ap.codigo_ean_gapp 
	JOIN empresa_report er 
	ON aegw.cnpj14 = er.cnpj
WHERE date(aegw.data_emissao) = '{{ ds }}'
GROUP BY aegw.ean_genuino, ap.codigo_ean_gapp,
		ap.descricao,ap.categoria_relatorio_id,
		er.cmb, date(aegw.data_emissao),ap.unidade_volume
    """)
