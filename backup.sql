PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE categories (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO "categories" VALUES(1,'დაზიანებული გზები');
INSERT INTO "categories" VALUES(2,'გაუმართავი განათება');
INSERT INTO "categories" VALUES(3,'ნაგვის დაგროვება');
INSERT INTO "categories" VALUES(4,'დაზიანებული სკვერები');
INSERT INTO "categories" VALUES(5,'წყლის გაჟონვა');
INSERT INTO "categories" VALUES(6,'საგზაო ნიშნები');
CREATE TABLE cities (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO "cities" VALUES(1,'თბილისი');
INSERT INTO "cities" VALUES(2,'ბათუმი');
INSERT INTO "cities" VALUES(3,'ქუთაისი');
INSERT INTO "cities" VALUES(4,'მცხეთა');
INSERT INTO "cities" VALUES(5,'რუსთავი');
INSERT INTO "cities" VALUES(6,'გორი');
INSERT INTO "cities" VALUES(7,'ზუგდიდი');
INSERT INTO "cities" VALUES(8,'ფოთი');
INSERT INTO "cities" VALUES(9,'სამტრედია');
INSERT INTO "cities" VALUES(10,'ახალციხე');
INSERT INTO "cities" VALUES(11,'ოზურგეთი');
INSERT INTO "cities" VALUES(12,'სენაკი');
INSERT INTO "cities" VALUES(13,'ხაშური');
INSERT INTO "cities" VALUES(14,'თელავი');
INSERT INTO "cities" VALUES(15,'ბორჯომი');
CREATE TABLE ratings (
	id INTEGER NOT NULL, 
	report_id INTEGER, 
	user_id INTEGER, 
	rating INTEGER, 
	comment TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(report_id) REFERENCES reports (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE report_status_history (
	id INTEGER NOT NULL, 
	report_id INTEGER, 
	status VARCHAR, 
	changed_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(report_id) REFERENCES reports (id)
);
CREATE TABLE reports (
	id INTEGER NOT NULL, 
	title VARCHAR NOT NULL, 
	description TEXT NOT NULL, 
	image_url VARCHAR, 
	city_id INTEGER, 
	category_id INTEGER, 
	user_id INTEGER, 
	latitude FLOAT, 
	longitude FLOAT, 
	status VARCHAR, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(city_id) REFERENCES cities (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO "reports" VALUES(1,'დაზიანებული გზა','დიდი ორმო ქუჩაზე',NULL,4,1,1,41.7,44.8,'pending','2026-07-01 18:00:44.145819','2026-07-01 18:00:44.145825');
CREATE TABLE users (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	email VARCHAR, 
	password VARCHAR NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE INDEX ix_users_id ON users (id);
CREATE INDEX ix_cities_id ON cities (id);
CREATE INDEX ix_categories_id ON categories (id);
CREATE INDEX ix_reports_id ON reports (id);
CREATE INDEX ix_report_status_history_id ON report_status_history (id);
CREATE INDEX ix_ratings_id ON ratings (id);
COMMIT;
