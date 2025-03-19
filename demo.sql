CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    
    PasswordHash VARCHAR(255) NOT NULL, -- 存儲加密後的密碼
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,-- Email (作為登入帳號，必須唯一)
    Age INT,
    Preferences JSON,  
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ChatHistory (
    ChatID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    MessageType ENUM('User', 'AI') NOT NULL,
    MessageText TEXT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
CREATE TABLE DailyRecords (
    RecordID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Date DATE NOT NULL,
    Activities TEXT, -- 例如 "散步, 吃早餐, 看書"
    Notes TEXT, -- 額外備註
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
CREATE TABLE Reminders (
    ReminderID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Type ENUM('Meal', 'Exercise', 'Event', 'Medication') NOT NULL,
    DateTime DATETIME NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
CREATE TABLE Alerts (
    AlertID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    AlertType ENUM('Inactivity', 'MissedReminder', 'Emergency') NOT NULL,
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
