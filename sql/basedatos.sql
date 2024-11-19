/*TABLA DE usuarios*/
DROP TABLE IF EXISTS app.usuarios CASCADE;
CREATE TABLE app.usuarios(
	id SERIAL PRIMARY KEY, 
	nombre VARCHAR(100),	
	edad INTEGER,
	domicilio VARCHAR(100),
	email VARCHAR(100) UNIQUE,
	password VARCHAR(100),	
	fecha_registro TIMESTAMP WITH TIME ZONE
);

INSERT INTO app.usuarios(nombre, edad, domicilio, email,password, fecha_registro) VALUES('Marge Simpson',36,'Av. Siempre Viva','marge@email.com','1234','2018-08-31T15:20:30+08:00');
INSERT INTO app.usuarios(nombre, edad, domicilio, email,password, fecha_registro) VALUES('Homero Simpson',38,'Av. Siempre Viva','homero@email.com','1234','2019-08-31T15:20:30+08:00');
INSERT INTO app.usuarios(nombre, edad, domicilio, email,password, fecha_registro) VALUES('Lisa Simpson',8,'Av. Siempre Viva','lisa@email.com','1234','2020-08-31T15:20:30+08:00');
INSERT INTO app.usuarios(nombre, edad, domicilio, email,password, fecha_registro) VALUES('Bart Simpson',10,'Av. Siempre Viva','bart@email.com','1234','2021-08-31T15:20:30+08:00');

/*TABLA de compras*/
DROP TABLE IF EXISTS app.compras CASCADE;
CREATE TABLE app.compras(
	id SERIAL PRIMARY KEY, 
	id_usuario INTEGER,
	producto VARCHAR(100),	
	precio FLOAT,
	FOREIGN KEY(id_usuario) REFERENCES app.usuarios(id)	
);

INSERT INTO app.compras(id_usuario,producto,precio) VALUES(1,'Caballete',1730);
INSERT INTO app.compras(id_usuario,producto,precio) VALUES(1,'Disco vinil Ringo Starr',1500);
INSERT INTO app.compras(id_usuario,producto,precio) VALUES(2,'TV',20000);
INSERT INTO app.compras(id_usuario,producto,precio) VALUES(2,'Six pack cerveza duff',360);
INSERT INTO app.compras(id_usuario,producto,precio) VALUES(2,'Bolsa papas',500);


/* tabla de fotos*/
DROP TABLE IF EXISTS app.fotos CASCADE;
CREATE TABLE app.fotos(
	id SERIAL PRIMARY KEY, 
    id_usuario INTEGER,
	titulo VARCHAR(100),
	descripcion VARCHAR(100),
	ruta VARCHAR,		
    FOREIGN KEY(id_usuario) REFERENCES app.usuarios(id)	
);
INSERT INTO app.fotos(id_usuario,titulo,descripcion,ruta) VALUES(1,'titulo 1','descripción 1','/home/servidor/fotos/sfd235fg.jpg');
INSERT INTO app.fotos(id_usuario,titulo,descripcion,ruta) VALUES(1,'titulo 2','descripción 2','/home/servidor/fotos/tsdfw23f.jpg');
INSERT INTO app.fotos(id_usuario,titulo,descripcion,ruta) VALUES(1,'titulo 3','descripción 3','/home/servidor/fotos/terwe324.jpg');
INSERT INTO app.fotos(id_usuario,titulo,descripcion,ruta) VALUES(2,'titulo 4','descripción 4','/home/servidor/fotos/sfw23425.jpg');
INSERT INTO app.fotos(id_usuario,titulo,descripcion,ruta) VALUES(2,'titulo 5','descripción 5','/home/servidor/fotos/2345sdr2.jpg');

