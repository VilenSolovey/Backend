CREATE TABLE Employees (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    position VARCHAR(20),
    email VARCHAR(50) ,
    phone_number VARCHAR(12) ,
    middle_name VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE RequestStatus (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE RequestPriority (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    level VARCHAR(45) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Locations (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    room_numbers INT NOT NULL,
    office_name VARCHAR(100) NOT NULL,
    workplace_number INT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Requests (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    description VARCHAR(255) NOT NULL,
    creation_time DATETIME NOT NULL,
    requeststatusid INT NOT NULL,
    request_priority_id INT NOT NULL,
    locations_id INT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Equipment (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    model VARCHAR(45) NOT NULL,
    type VARCHAR(45) NOT NULL,
    serial_number INT NOT NULL,
    end_of_warranty DATETIME NOT NULL
) ENGINE=InnoDB;

CREATE TABLE EquipmentChanges (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    date DATETIME NOT NULL,
    old_equipment_id INT NOT NULL ,
    new_equipment_id INT NOT NULL ,
    request_id INT NOT NULL 
) ENGINE=INNODB;;

CREATE TABLE Software (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(45) NOT NULL,
    version VARCHAR(45) NOT NULL,
    Locations_id INT NOT NULL
) ENGINE=INNODB;;

CREATE TABLE SoftwareIssues (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    description VARCHAR(200) NOT NULL,
    Software_id INT NOT NULL
) ENGINE=INNODB;;

CREATE TABLE SoftwareUpdates (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    update_date DATE,
    Software_id INT NOT NULL ,
    Requests_id INT NOT NULL
) ENGINE=INNODB;;

CREATE TABLE Requests_has_Employees (
    Requests_id INT NOT NULL,
    Employees_id INT NOT NULL,
    PRIMARY KEY (Requests_id, Employees_id)
) ENGINE=INNODB;;

CREATE TABLE Request_Issue_Type (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    type VARCHAR(45) NOT NULL
) ENGINE=INNODB;;

CREATE TABLE Requests_has_Request_Issue_Type (
    Requests_id INT NOT NULL,
    Request_Issue_Type_id INT NOT NULL,
    PRIMARY KEY (Requests_id, Request_Issue_Type_id)
) ENGINE=INNODB;;

CREATE TABLE Tasks (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    due_date DATETIME NOT NULL,
    status INT NOT NULL,
    employee_id INT NOT NULL,
    CONSTRAINT FK_Tasks_Employees FOREIGN KEY (employee_id) REFERENCES Employees(id) ON DELETE CASCADE
) ENGINE=InnoDB;

ALTER TABLE Requests
ADD CONSTRAINT FK_Requests_RequestStatus
FOREIGN KEY (RequestStatus_id) REFERENCES RequestStatus(id) ON DELETE CASCADE,
ADD CONSTRAINT FK_Requests_RequestPriority
FOREIGN KEY (RequestPriority_id) REFERENCES RequestPriority(id) ON DELETE CASCADE,
ADD CONSTRAINT FK_Requests_Locations
FOREIGN KEY (Locations_id) REFERENCES Locations(id) ON DELETE CASCADE;

ALTER TABLE EquipmentChanges
ADD CONSTRAINT FK_EquipmentChanges_oldEquipment
FOREIGN KEY (old_equipment_id) REFERENCES Equipment(id),
ADD CONSTRAINT FK_EquipmentChanges_newEquipment
FOREIGN KEY (new_equipment_id) REFERENCES Equipment(id),
ADD CONSTRAINT FK_EquipmentChanges_request
FOREIGN KEY (request_id) REFERENCES Requests(id),
ADD CONSTRAINT UNIQUE (request_id);

ALTER TABLE Software
ADD CONSTRAINT FK_Software_Locations
FOREIGN KEY (Locations_id) REFERENCES Locations(id) ON DELETE CASCADE;

ALTER TABLE SoftwareIssues
ADD CONSTRAINT FK_SoftwareIssues_Software
FOREIGN KEY (Software_id) REFERENCES Software(id);

ALTER TABLE SoftwareUpdates
ADD CONSTRAINT FK_SoftwareUpdates_Software
FOREIGN KEY (Software_id) REFERENCES Software(id),
ADD CONSTRAINT FK_SoftwareUpdates_Requests
FOREIGN KEY (Requests_id) REFERENCES Requests(id);

ALTER TABLE Requests_has_Employees
ADD CONSTRAINT FK_Requests_has_Employees_Requests
FOREIGN KEY (Requests_id) REFERENCES Requests(id) ON DELETE CASCADE,
ADD CONSTRAINT FK_Requests_has_Employees_Employees
FOREIGN KEY (Employees_id) REFERENCES Employees(id) ON DELETE CASCADE;

ALTER TABLE Requests_has_Request_Issue_Type
ADD CONSTRAINT FK_Requests_has_Request_Issue_Type_Requests
FOREIGN KEY (Requests_id) REFERENCES Requests(id) ON DELETE CASCADE,
ADD CONSTRAINT FK_Requests_has_Request_Issue_Type_Request_Issue_Type
FOREIGN KEY (Request_Issue_Type_id) REFERENCES Request_Issue_Type(id) ON DELETE CASCADE;



CREATE UNIQUE INDEX idx_email ON Employees (email);
CREATE UNIQUE INDEX idx_phone_number ON Employees (phone_number);
CREATE UNIQUE INDEX idx_serial_number ON Equipment (serial_number);
CREATE UNIQUE INDEX idx_software_serial_number ON Software (software_serial_number);
CREATE UNIQUE INDEX idx_office_name ON Locations (office_name);
