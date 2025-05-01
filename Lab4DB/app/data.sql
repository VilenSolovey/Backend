INSERT INTO RequestStatus (id, name) VALUES
(1, 'Pending'),
(2, 'In Progress'),
(3, 'Resolved'),
(4, 'Closed'),
(5, 'Cancelled');


INSERT INTO RequestPriority (id, level) VALUES
(1, 'Low'),
(2, 'Medium'),
(3, 'High'),
(4, 'Urgent'),
(5, 'Critical');


INSERT INTO Locations (id, room_numbers, office_name, workplace_number) VALUES
(1, 101, 'Main Office', 1),
(2, 202, 'Development Lab', 2),
(3, 303, 'Design Studio', 3),
(4, 404, 'Testing Area', 4),
(5, 505, 'Support Center', 5);

INSERT INTO Software (id, name, version, Locations_id) VALUES
(1, 'Microsoft Office', '365', 1),
(2, 'Adobe Photoshop', '2024.1', 2),
(3, 'AutoCAD', '2024', 3),
(4, 'Chrome', '115', 4),
(5, 'Slack', '4.29.149', 5);

INSERT INTO Employees (id, first_name, last_name, position, email, phone_number, middle_name) VALUES
(1, 'John', 'Doe', 'Manager', 'john.doe@example.com', '1234567890', 'Michael'),
(2, 'Jane', 'Smith', 'Developer', 'jane.smith@example.com', '0987654321', 'Anne'),
(3, 'Alice', 'Johnson', 'Designer', 'alice.johnson@example.com', '1122334455', 'Marie'),
(4, 'Bob', 'Brown', 'Tester', 'bob.brown@example.com', '2233445566', 'James'),
(5, 'Charlie', 'Davis', 'Support', 'charlie.davis@example.com', '3344556677', 'Andrew'),
(6, 'David', 'White', 'Manager', 'david.white@example.com', '4455667788', 'John'),
(7, 'Emma', 'Green', 'Developer', 'emma.green@example.com', '5566778899', 'Sophia'),
(8, 'Michael', 'Taylor', 'Designer', 'michael.taylor@example.com', '6677889900', 'Lucas'),
(9, 'Olivia', 'Harris', 'Tester', 'olivia.harris@example.com', '7788990011', 'Grace'),
(10, 'Ethan', 'Clark', 'Support', 'ethan.clark@example.com', '8899001122', 'Lucas');

INSERT INTO Requests (id, description, creation_time, requeststatusid, request_priority_id, locations_id) VALUES
(1, 'Network issue in room 101', '2024-11-01 08:30:00', 1, 2, 1),
(2, 'Software installation required', '2024-11-01 09:00:00', 2, 1, 2),
(3, 'System update request', '2024-11-02 10:15:00', 3, 3, 3),
(4, 'Printer not working', '2024-11-02 11:45:00', 4, 2, 4),
(5, 'New employee setup', '2024-11-02 13:00:00', 5, 1, 5);

INSERT INTO Equipment (id, model, type, serial_number, end_of_warranty) VALUES
(1, 'Dell XPS', 'Laptop', 123456, '2025-01-01'),
(2, 'HP LaserJet', 'Printer', 789012, '2024-12-15'),
(3, 'Cisco Router', 'Networking', 345678, '2026-03-20'),
(4, 'Logitech Mouse', 'Peripheral', 901234, '2025-07-01'),
(5, 'Samsung Monitor', 'Display', 567890, '2025-05-10');

INSERT INTO EquipmentChanges (id, date, old_equipment_id, new_equipment_id, request_id) VALUES
(1, '2024-11-01', 1, 2, 1),
(2, '2024-11-02', 3, 4, 2),
(3, '2024-11-03', 2, 5, 3),
(4, '2024-11-04', 4, 1, 4),
(5, '2024-11-05', 5, 3, 5);

INSERT INTO Tasks (title, description, due_date, status, employee_id)
VALUES
('Task 1', 'Description for Task 1', '2024-12-01 10:00:00', 1, 1),
('Task 2', 'Description for Task 2', '2024-12-02 12:00:00', 2, 2),
('Task 3', 'Description for Task 3', '2024-12-03 14:00:00', 3, 3),
('Task 4', 'Description for Task 4', '2024-12-04 16:00:00', 1, 4),
('Task 5', 'Description for Task 5', '2024-12-05 18:00:00', 2, 5),
('Task 6', 'Description for Task 6', '2024-12-06 20:00:00', 3, 6),
('Task 7', 'Description for Task 7', '2024-12-07 22:00:00', 1, 7),
('Task 8', 'Description for Task 8', '2024-12-08 09:00:00', 2, 8),
('Task 9', 'Description for Task 9', '2024-12-09 11:00:00', 3, 9),
('Task 10', 'Description for Task 10', '2024-12-10 13:00:00', 1, 10);

INSERT INTO SoftwareIssues (id, description, software_id) VALUES
(1, 'Issue with installation of software A', 1),
(2, 'Software B crashes on startup', 2),
(3, 'Error message ', 1),
(4, 'Software D not responding', 3),
(5, 'Update issue with software E', 2);

INSERT INTO request_issue_type (id, type) VALUES
(1, 'Network Issue'),
(2, 'Software Installation'),
(3, 'Hardware Failure'),
(4, 'Account Access'),
(5, 'Performance Issue');

INSERT INTO SoftwareUpdates (id, update_date, software_id, requests_id) VALUES
(1, '2024-11-01', 1, 1),
(2, '2024-11-02', 2, 2),
(3, '2024-11-03', 3, 1),
(4, '2024-11-04', 4, 3),
(5, '2024-11-05', 5, 4);

INSERT INTO requests_has_employees(requests_id, employees_id) VALUES
(3, 1),
(4, 2),
(1, 3),
(2, 4),
(5, 5);

INSERT INTO requests_has_request_issue_type(requests_id, request_issue_type_id) VALUES
(3, 3),
(4, 4),
(1, 1),
(2, 2),
(5, 5);

