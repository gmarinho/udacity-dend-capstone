
/*Stage app_categoria_nielsen*/
CREATE TABLE IF NOT EXISTS app_categoria_nielsen (
	id INT8 PRIMARY KEY,
	categoria_produto_id INTEGER,
	descricao VARCHAR,
	nielsen_id INTEGER,
	data_criacao TIMESTAMP,
	data_atualizacao TIMESTAMP,
	user_edicao VARCHAR,
	categoria_mae VARCHAR,
	categoria_mae_id INTEGER,
	descricao_categoria_nivel1 VARCHAR,
	id_categoria_nivel1_id INTEGER
);

/*Stage empresa_report*/
CREATE TABLE IF NOT EXISTS empresa_report (
	cnpj VARCHAR PRIMARY KEY,
	uf VARCHAR,
	cmb VARCHAR,
	municipio VARCHAR,
	bairro VARCHAR,
	rede VARCHAR,
	id_categoria INTEGER,
	franquia VARCHAR,
	engarrafador VARCHAR,
	codigo_regiao INTEGER,
	regiao_pinngo VARCHAR,
	classe_social VARCHAR,
	checkouts INTEGER,
	id_canal INTEGER,
	id_rede INTEGER
);

/*Stage app_produto*/
CREATE TABLE  IF NOT EXISTS app_produto(
	id INTEGER PRIMARY KEY,
	"file" VARCHAR NULL,
	descricao VARCHAR NULL,
	qtd REAL NULL,
	status VARCHAR NULL,
	marca_produto_id INTEGER NULL,
	codigo_ean_gapp INTEGER NULL,
	unidade_volume VARCHAR NULL,
	data_atualizacao VARCHAR NULL,
	data_criacao VARCHAR NULL,
	user_edicao VARCHAR NULL,
	categoria_id INTEGER NULL,
	fabricante_id INTEGER NULL,
	categoria_relatorio_id INTEGER NULL,
	mediana REAL NULL,
	relevancia INTEGER NULL,
	ncm INTEGER NULL
);


/*Stage app_ean_genuino_weekly*/
CREATE TABLE IF NOT EXISTS app_ean_genuino_weekly (
	id_row INT8,
	id_item INT8 PRIMARY KEY,
	nota_id INT8,
	cnpj14 VARCHAR,
	serie VARCHAR,
	nfce VARCHAR,
	codigo_produto VARCHAR,
	codigo_ncm VARCHAR,
	ean_genuino REAL,
	produto_id REAL,
	data_emissao TIMESTAMP,
	valor REAL,
	valor_desconto REAL,
	qtd REAL,
	status_ean INTEGER,
	valor_produto REAL,
	empresa_id INT8,
	descricao VARCHAR,
	modelo INTEGER,
	"user_id" INT8,
	year_day INTEGER,
	partner INTEGER,
	"user" VARCHAR
);

/*city dimension*/
CREATE TABLE IF NOT EXISTS city_dim(
	city_id VARCHAR PRIMARY KEY,
	city_name VARCHAR,
	"state" VARCHAR,
	country VARCHAR
);

/*categories dimension*/
CREATE TABLE IF NOT EXISTS categories_dim(
	category_id INT8 PRIMARY KEY,
	category_name VARCHAR,
	macro_category VARCHAR,
	description VARCHAR
);

/*time dimension*/
CREATE TABLE IF NOT EXISTS time_dim(
	date_id TIMESTAMP PRIMARY KEY,
	day_number INTEGER,
	week INTEGER,
	"month" INTEGER,
	"year" INTEGER,
	week_day INTEGER
);

/*product_sales fact*/
CREATE TABLE IF NOT EXISTS product_sales(
	product_id INT8 PRIMARY KEY,
	name VARCHAR,
	category_id INT8,
	city_id VARCHAR,
	total_sales REAL,
	total_volume REAL,
	date_id DATE,
	unit VARCHAR	
);