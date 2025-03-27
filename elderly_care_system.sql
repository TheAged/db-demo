
-- Elderly table
CREATE TABLE Elderly (
    elderly_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    gender ENUM('男', '女'),
    birth_date DATE,
    emergency_contact VARCHAR(100),
    address TEXT
);

-- Health_Record table
CREATE TABLE Health_Record (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    elderly_id INT,
    record_date DATETIME,
    heart_rate INT,
    blood_pressure VARCHAR(20),
    temperature DECIMAL(4,1),
    FOREIGN KEY (elderly_id) REFERENCES Elderly(elderly_id)
);

-- Fall_Detection_Log table
CREATE TABLE Fall_Detection_Log (
    fall_id INT PRIMARY KEY AUTO_INCREMENT,
    elderly_id INT,
    fall_time DATETIME,
    location VARCHAR(100),
    is_emergency BOOLEAN,
    FOREIGN KEY (elderly_id) REFERENCES Elderly(elderly_id)
);

-- Caretaker table
CREATE TABLE Caretaker (
    caretaker_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- Assignment table
CREATE TABLE Assignment (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    elderly_id INT,
    caretaker_id INT,
    start_date DATE,
    FOREIGN KEY (elderly_id) REFERENCES Elderly(elderly_id),
    FOREIGN KEY (caretaker_id) REFERENCES Caretaker(caretaker_id)
);
