create database project_1
go 
use project_1 

GO
CREATE TABLE users (
    id int PRIMARY KEY identity(1,1),
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at DATETIME  DEFAULT GETDATE(),
    last_active_at DATETIME2,
    status VARCHAR(20) DEFAULT 'active', -- active, blocked, vip
    is_vip bit DEFAULT 0, -- VIP foydalanuvchilar uchun
    total_balance BIGINT DEFAULT 0 -- Umumiy balans
);
GO
CREATE TABLE cards (
    id int PRIMARY KEY identity(1,1),
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    card_number VARCHAR(16) UNIQUE NOT NULL,
    balance BIGINT DEFAULT 0,
    is_blocked bit DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    card_type VARCHAR(20) CHECK (card_type IN ('debit', 'credit', 'savings')), -- Karta turi
    limit_amount BIGINT DEFAULT 150000000 -- Limitdan oshsa bloklanadi
);
GO
CREATE TABLE transactions (
    id int PRIMARY KEY identity(1,1),
    from_card_id INT foreign key REFERENCES cards(id) ON DELETE CASCADE,
    to_card_id INT foreign key REFERENCES cards(id) ON DELETE NO ACTION,
    amount BIGINT NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending', 'success', 'failed')) DEFAULT 'pending',
    created_at DATETIME  DEFAULT GETDATE(),
    transaction_type VARCHAR(20) CHECK (transaction_type IN ('transfer', 'withdrawal', 'deposit')),
    is_flagged bit DEFAULT 0 -- Shubhali tranzaksiyalarni aniqlash uchun
);  
GO
CREATE TABLE logs (
    id int PRIMARY KEY identity(1,1),
    transaction_id INT foreign key REFERENCES transactions(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    created_at DATETIME  DEFAULT GETDATE()
);
GO
CREATE TABLE reports (
    id int PRIMARY KEY identity(1,1),
    report_type VARCHAR(50), -- daily, weekly, monthly
    created_at DATETIME  DEFAULT GETDATE(),
    total_transactions BIGINT DEFAULT 0,
    flagged_transactions BIGINT DEFAULT 0, -- Shubhali tranzaksiyalar
    total_amount BIGINT DEFAULT 0
);
GO
CREATE TABLE fraud_detection (
    id int PRIMARY KEY identity(1,1),
    transaction_id INT FOREIGN KEY REFERENCES transactions(id) ON DELETE CASCADE,
    user_id INT FOREIGN KEY REFERENCES users(id) ON DELETE NO ACTION,
    reason TEXT NOT NULL, -- Shubhali harakat sababi
    status VARCHAR(20) CHECK (status IN ('pending', 'reviewed', 'blocked')) DEFAULT 'pending',
    created_at DATETIME  DEFAULT GETDATE()
);
GO
CREATE TABLE scheduled_payments (
    id int PRIMARY KEY identity(1,1),
    user_id INT FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE,
    card_id INT FOREIGN KEY REFERENCES cards(id) ON DELETE NO ACTION,
    amount BIGINT NOT NULL,
    payment_date DATETIME  NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending', 'completed', 'failed')) DEFAULT 'pending',
    created_at DATETIME  DEFAULT GETDATE()
);
GO
CREATE TABLE vip_users (
    id int PRIMARY KEY identity(1,1),
    user_id INT foreign key REFERENCES users(id) ON DELETE CASCADE,
    assigned_at DATETIME  DEFAULT GETDATE(),
    reason TEXT NOT NULL -- VIP bo‘lish sababi (mablag‘ miqdori, tranzaksiya hajmi va h.k)
);
 GO
CREATE TABLE blocked_users (
    id int PRIMARY KEY identity(1,1),
    user_id INT foreign key REFERENCES users(id) ON DELETE CASCADE,
    blocked_at DATETIME  DEFAULT GETDATE(),
    reason TEXT NOT NULL
); 
GO
INSERT INTO users (name, phone_number, email, status, is_vip, total_balance,last_active_at) VALUES
('Javohir Xudoyberdiyev', '998901112233', 'javohir@example.com', 'active', 0, 3000000,'2025-03-18 10:15:00'),
('Saida Karimova', '998902223344', 'saida@example.com', 'vip', 1, 50000000,'2025-03-17 08:30:00'),
('Azizbek Ergashev', '998903334455', 'azizbek@example.com', 'active', 0, 7000000,'2025-03-10 14:45:00'),
('Ali Valiyev', '998901234567', 'ali@example.com', 'active', 0, 5000000,'2025-02-25 19:00:00'),
('Olim Karimov', '998902345678', 'olim@example.com', 'vip', 1, 20000000,'2025-02-20 11:20:00'),
('Nodir Xasanov', '998903456789', 'nodir@example.com', 'blocked', 0, 1000000,'2025-01-15 16:10:00'),
('Shahnoza Yuldasheva', '998907654321', 'shahnoza@example.com', 'active', 0, 8000000,'2025-03-12 09:50:00'),
('Rustam Qosimov', '998908765432', 'rustam@example.com', 'active', 0, 6000000,'2025-03-05 17:40:00');
GO
INSERT INTO cards (user_id, card_number, balance, is_blocked, card_type, limit_amount) VALUES
(1, '8600111122223333', 3000000, 0, 'debit', 150000000),
(2, '8600222233334444', 50000000, 0, 'credit', 500000000),
(3, '8600333344445555', 7000000, 0, 'savings', 20000000),
(4, '8600123412341234', 5000000, 0, 'debit', 150000000),
(5, '8600234523452345', 20000000, 0, 'credit', 300000000),
(6, '8600345634563456', 1000000, 1, 'savings', 10000000),
(7, '8600456745674567', 8000000, 0, 'debit', 150000000),
(8, '8600567856785678', 6000000, 0, 'credit', 250000000);
GO
INSERT INTO transactions (from_card_id, to_card_id, amount, status, transaction_type, is_flagged) VALUES
(1, 2, 2500000, 'success', 'transfer', 0),
(2, null, 1000000, 'success', 'withdrawal', 0),
(null, 1, 500000, 'pending', 'deposit', 0),
(4, 5, 1500000, 'success', 'transfer', 0),
(5, null, 5000000, 'failed', 'withdrawal', 1),
(6, 4, 300000, 'pending', 'deposit', 0),
(7, 8, 2000000, 'success', 'transfer', 0),
(8, null, 1000000, 'failed', 'withdrawal', 1);
GO
INSERT INTO logs (transaction_id, message) VALUES
(1, 'Transaction completed successfully'),
(2, 'Withdrawal successful'),
(3, 'Deposit pending confirmation'),
(4, 'Transfer to credit card completed'),
(5, 'Transaction failed due to insufficient funds'),
(6, 'Transaction pending for approval'),
(7, 'Transfer completed successfully'),
(8, 'Transaction flagged for review');
GO
INSERT INTO reports (report_type, total_transactions, flagged_transactions, total_amount) VALUES
('daily', 50, 5, 25000000),
('weekly', 150, 15, 75000000),
('monthly', 500, 30, 200000000);
GO
INSERT INTO fraud_detection (transaction_id, user_id, reason, status) VALUES
(5, 2, 'Large withdrawal attempt detected', 'reviewed'),
(6, 3, 'Suspicious deposit pattern', 'pending'),
(8, 4, 'Unusual transaction frequency', 'reviewed');
GO
INSERT INTO scheduled_payments (user_id, card_id, amount, payment_date, status) VALUES
(1, 1, 700000, '2025-04-01 10:00:00', 'pending'),
(2, 2, 3000000, '2025-04-05 15:30:00', 'completed'),
(3, 3, 1500000, '2025-04-10 12:00:00', 'pending'),
(4, 4, 2000000, '2025-04-15 09:00:00', 'pending');
GO
SET LANGUAGE US_ENGLISH
GO
INSERT INTO vip_users (user_id, reason) VALUES
(2, 'High transaction volume and large deposits'),
(5, 'Consistent high balance and VIP status eligibility'),
(8, 'High spending habits and priority services');
GO
INSERT INTO blocked_users (user_id, reason) VALUES
(3, 'Suspicious activities detected multiple times'),
(6, 'Fraudulent transaction attempt detected'),
(7, 'Multiple failed login attempts and security concerns');
GO  

CREATE TRIGGER trg_insert_logs_withdrawal
ON transactions
AFTER INSERT
AS
BEGIN 
    INSERT INTO logs (transaction_id, message, created_at)
    SELECT i.id, 
           'Deposit pending confirmation', 
           GETDATE()
    FROM inserted i
    WHERE i.transaction_type = 'withdrawal' AND i.status = 'pending';
END;
  
create view get_active_users as
select * from users 
where last_active_at between DATEADD(MONTH,-1,last_active_at) and GETDATE()
