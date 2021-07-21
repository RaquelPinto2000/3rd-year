CREATE SCHEMA reservas_voos;
GO

CREATE TABLE reservas_voos.Airport(
	Name 			VARCHAR(50) 	NOT NULL,
	State 			VARCHAR(30)  	NOT NULL,
	City 			VARCHAR(30) 	NOT NULL,
	Airport_code 	INT PRIMARY KEY NOT NULL CHECK(Airport_code >= 0)
);
GO

CREATE TABLE reservas_voos.Airplane_type(
	Company 	VARCHAR(50) 	NOT NULL,
	Max_seats 	SMALLINT 		NOT NULL 		CHECK(Max_seats > 0),
	Type_name 	VARCHAR(50) 	PRIMARY KEY 	NOT NULL
);
GO

CREATE TABLE reservas_voos.Can_land(
	Airport 		INT 		REFERENCES reservas_voos.Airport(Airport_code) 		NOT NULL,
	Airplane_type 	VARCHAR(50) REFERENCES reservas_voos.Airplane_type(Type_name) 	NOT NULL,
	PRIMARY KEY(Airport ,Airplane_type)
);
GO

CREATE TABLE reservas_voos.Airplane(
	Airplane_id			INT PRIMARY KEY 	NOT NULL,
	Total_no_of_seats	SMALLINT NOT NULL	CHECK(Total_no_of_seats > 0),
	Type VARCHAR(50) 	REFERENCES 			reservas_voos.Airplane_type(Type_name) NOT NULL
);
GO

CREATE TABLE reservas_voos.Flight_Leg(
	dep_time 	DATE 		NOT NULL,
	arr_time 	DATE 		NOT NULL,
	Leg_no 	 	INT 		NOT NULL CHECK(Leg_no >= 0),
	Flight 		INT 		REFERENCES reservas_voos.Flight(Number) NOT NULL,
	dep_airport INT			REFERENCES reservas_voos.Airport(Airport_code) NOT NULL,
	arr_airport INT			REFERENCES reservas_voos.Airport(Airport_code) NOT NULL,
	PRIMARY KEY(Flight, Leg_no)
);
GO

CREATE TABLE reservas_voos.Flight(
	Weekdays	CHAR(7)				NOT NULL,
	Airline		VARCHAR(60) 		NOT NULL,	
	Number		INT	PRIMARY KEY 	NOT NULL
);
GO
CREATE TABLE reservas_voos.Leg_instance(
	No_of_avail_seats 	SMALLINT	NOT NULL,
	Data_instance		DATE 		NOT NULL,
	Departs 			DATE 		NOT NULL,
	Arrives 			TIMESTAMP 	NOT NULL,
	Airplane_id			INT 		REFERENCES reservas_voos.Airplane(Airplane_id) NOT NULL,
	Airport_arrives		INT			REFERENCES reservas_voos.Airport(Airport_code) NOT NULL,
	Airport_departs		INT			REFERENCES reservas_voos.Airport(Airport_code) NOT NULL,
	Flight 				INT			NOT NULL,
	Leg_no				INT			NOT NULL,
	FOREIGN KEY(Flight,Leg_no) 		REFERENCES reservas_voos.Flight_Leg(Flight,Leg_no) NOT NULL,
	PRIMARY KEY(Data_instance,Flight,Leg_no)
);
GO

CREATE TABLE reservas_voos.Fare(
	Amount 			INT 		NOT NULL,
	Restrictions 	VARCHAR(200),
	Code 			INT 		NOT NULL,
	Num 			INT REFERENCES reservas_voos.Flight(Number) NOT NULL,
	PRIMARY KEY(Code,Num)
);
GO

CREATE TABLE reservas_voos.Seat(
	Seat_no 		SMALLINT NOT NULL,
	Customer_name	VARCHAR(60) NOT NULL,
	CPhone		 	VARCHAR(13) NOT NULL,
	Num_flight		INT NOT NULL,
	Leg_date 		DATE NOT NULL,
	Leg_no 			SMALLINT NOT NULL,
	Airplane_id		INT NOT NULL, 	
	FOREIGN KEY (Num_flight,Leg_date,Leg_no,Airplane_id) REFERENCES reservas_voos.Leg_instance(Number,Date,Leg_no,Airplane_id) NOT NULL,			
	PRIMARY KEY(Seat_no,Num_flight,Leg_no,Date)
);
GO