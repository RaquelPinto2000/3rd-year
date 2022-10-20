CREATE TABLE ambulance (
	id_ambulance INTEGER PRIMARY KEY,
	id_user     INTEGER, 
	FOREIGN KEY(id_user) REFERENCES user(id)
);