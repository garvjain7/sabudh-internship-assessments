-- FinanceHub SQL Coursework | Garv Jain
-- Dialect: MySQL 8.0+

USE FinanceHub;

-- Q1: Customers with credit score > 700 and income > 80000
SELECT CONCAT(first_name, ' ', last_name) AS customer_name,
       credit_score,
       annual_income,
       risk_profile
FROM Customers
WHERE credit_score > 700
  AND annual_income > 80000
ORDER BY credit_score DESC;

-- Q2: Category totals for 2024 above 5000
SELECT category,
       SUM(amount) AS total_amount
FROM Transactions
WHERE transaction_date >= '2024-01-01'
  AND transaction_date <  '2025-01-01'
GROUP BY category
HAVING SUM(amount) > 5000
ORDER BY total_amount DESC;

-- Q3: Active loans with last payment date and status
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       l.loan_type,
       l.loan_amount,
       l.outstanding_balance,
       l.monthly_emi,
       (SELECT MAX(lp.payment_date)
          FROM LoanPayments lp
         WHERE lp.loan_id = l.loan_id) AS last_payment_date,
       COALESCE((SELECT lp.payment_status
                   FROM LoanPayments lp
                  WHERE lp.loan_id = l.loan_id
                  ORDER BY lp.payment_date DESC
                  LIMIT 1), 'No Payments') AS current_payment_status
FROM Loans l
JOIN Customers c ON c.customer_id = l.customer_id
WHERE l.loan_status = 'Active'
ORDER BY l.outstanding_balance DESC;

-- Q4: Customers with total balance above the average total balance
WITH cust_balance AS (
    SELECT c.customer_id,
           CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
           SUM(a.current_balance) AS total_balance,
           COUNT(a.account_id)    AS num_accounts
    FROM Customers c
    JOIN Accounts a ON a.customer_id = c.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT customer_name, total_balance, num_accounts
FROM cust_balance
WHERE total_balance > (SELECT AVG(total_balance) FROM cust_balance)
ORDER BY total_balance DESC;

-- Q5: Investment segmentation (current_price holds total position value)
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       SUM(i.current_price) AS total_investment_value,
       CASE
           WHEN SUM(i.current_price) >  100000 THEN 'High Value'
           WHEN SUM(i.current_price) >= 50000  THEN 'Medium Value'
           WHEN SUM(i.current_price) >= 20000  THEN 'Low Value'
           ELSE 'New Investor'
       END AS segment
FROM Customers c
JOIN Investments i ON i.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_investment_value DESC;

-- Q6: Customers with accounts but no loans
SELECT c.customer_id,
       CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       SUM(a.current_balance) AS total_balance,
       COUNT(a.account_id)    AS num_accounts
FROM Customers c
JOIN Accounts a ON a.customer_id = c.customer_id
WHERE NOT EXISTS (SELECT 1 FROM Loans l WHERE l.customer_id = c.customer_id)
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY c.customer_id;

-- Q7: Employees with manager name (top-level employees included)
SELECT CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
       e.job_title,
       CONCAT(m.first_name, ' ', m.last_name) AS manager_name,
       e.department
FROM Employees e
LEFT JOIN Employees m ON m.employee_id = e.manager_id
ORDER BY e.employee_id;

-- Q8: Credit card utilisation rank within card type
SELECT cc.card_type,
       CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       cc.credit_limit,
       cc.current_balance,
       ROUND(cc.current_balance / cc.credit_limit * 100, 2) AS utilisation_pct,
       RANK() OVER (PARTITION BY cc.card_type
                    ORDER BY cc.current_balance / cc.credit_limit DESC) AS rank_in_type
FROM CreditCards cc
JOIN Customers c ON c.customer_id = cc.customer_id
ORDER BY cc.card_type, rank_in_type;

-- Q9: Monthly transaction volume for 2024
SELECT DATE_FORMAT(transaction_date, '%Y-%m') AS month,
       COUNT(*)                AS num_transactions,
       SUM(amount)             AS total_amount,
       ROUND(AVG(amount), 2)   AS avg_amount
FROM Transactions
WHERE transaction_date >= '2024-01-01'
  AND transaction_date <  '2025-01-01'
GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
ORDER BY month;

-- Q10: Top 5 customers by Travel card spending
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       SUM(ct.amount)               AS total_travel_spending,
       COUNT(*)                     AS num_travel_transactions,
       SUM(ct.reward_points_earned) AS total_reward_points
FROM CardTransactions ct
JOIN CreditCards cc ON cc.card_id = ct.card_id
JOIN Customers c    ON c.customer_id = cc.customer_id
WHERE ct.merchant_category = 'Travel'
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_travel_spending DESC
LIMIT 5;

-- Q11: Accounts with deposits > 5000 in the last 60 days
-- Reference date = latest transaction in the data (sample data is from 2024)
SET @ref_date = (SELECT MAX(transaction_date) FROM Transactions);

SELECT a.account_number,
       a.account_type,
       CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       a.current_balance
FROM Accounts a
JOIN Customers c ON c.customer_id = a.customer_id
WHERE EXISTS (SELECT 1
                FROM Transactions t
               WHERE t.account_id = a.account_id
                 AND t.transaction_type = 'Deposit'
                 AND t.amount > 5000
                 AND t.transaction_date >= DATE_SUB(@ref_date, INTERVAL 60 DAY));

-- Q12: Unified product report for customer 1004
SELECT 'Account' AS product_type,
       account_number AS product_identifier,
       current_balance AS current_value
FROM Accounts
WHERE customer_id = 1004
UNION
SELECT 'Loan',
       CAST(loan_id AS CHAR),
       outstanding_balance
FROM Loans
WHERE customer_id = 1004
UNION
SELECT 'Credit Card',
       card_number,
       current_balance
FROM CreditCards
WHERE customer_id = 1004
UNION
SELECT 'Investment',
       CONCAT(investment_type, ' - ', security_name),
       current_price
FROM Investments
WHERE customer_id = 1004;

-- Q13: Running balance for account 5001 in 2024
-- Opening balance is derived from the first transaction's balance_after
WITH txn AS (
    SELECT transaction_id,
           transaction_date,
           transaction_type,
           amount,
           balance_after,
           CASE WHEN transaction_type IN ('Deposit', 'Transfer In')
                THEN amount ELSE -amount END AS signed_amount
    FROM Transactions
    WHERE account_id = 5001
      AND transaction_date >= '2024-01-01'
      AND transaction_date <  '2025-01-01'
)
SELECT transaction_date,
       transaction_type,
       amount,
       FIRST_VALUE(balance_after - signed_amount)
           OVER (ORDER BY transaction_date, transaction_id)
       + SUM(signed_amount)
           OVER (ORDER BY transaction_date, transaction_id
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_balance
FROM txn
ORDER BY transaction_date, transaction_id;

-- Q14: Loan performance by loan type
SELECT l.loan_type,
       COUNT(*)                      AS num_loans,
       SUM(l.loan_amount)            AS total_disbursed,
       SUM(l.outstanding_balance)    AS total_outstanding,
       ROUND(AVG(l.interest_rate), 2) AS avg_interest_rate,
       ROUND(SUM(COALESCE(p.total_paid, 0)) / SUM(l.loan_amount) * 100, 2) AS payment_completion_pct
FROM Loans l
LEFT JOIN (SELECT loan_id, SUM(amount_paid) AS total_paid
             FROM LoanPayments
            GROUP BY loan_id) p ON p.loan_id = l.loan_id
GROUP BY l.loan_type
ORDER BY total_disbursed DESC;

-- Q15: Branch employees, customers and share of bank customers
-- Customers per branch = distinct customers holding an account at that branch
SELECT b.branch_name,
       (SELECT COUNT(*) FROM Employees e
         WHERE e.branch_id = b.branch_id) AS total_employees,
       (SELECT COUNT(DISTINCT a.customer_id) FROM Accounts a
         WHERE a.branch_code = b.branch_code) AS total_customers,
       ROUND((SELECT COUNT(DISTINCT a.customer_id) FROM Accounts a
               WHERE a.branch_code = b.branch_code)
             / (SELECT COUNT(*) FROM Customers) * 100, 2) AS pct_of_bank_customers
FROM Branches b
ORDER BY b.branch_id;

-- Q16: Customers with > 5 transactions and average amount > 500
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       COUNT(t.transaction_id)  AS num_transactions,
       SUM(t.amount)            AS total_amount,
       ROUND(AVG(t.amount), 2)  AS avg_amount
FROM Customers c
JOIN Accounts a     ON a.customer_id = c.customer_id
JOIN Transactions t ON t.account_id = a.account_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(t.transaction_id) > 5
   AND AVG(t.amount) > 500
ORDER BY total_amount DESC;

-- Q17: Month-over-month change in loan disbursements
WITH monthly AS (
    SELECT DATE_FORMAT(disbursement_date, '%Y-%m') AS month,
           SUM(loan_amount) AS total_disbursed
    FROM Loans
    GROUP BY DATE_FORMAT(disbursement_date, '%Y-%m')
)
SELECT month,
       total_disbursed,
       LAG(total_disbursed) OVER (ORDER BY month) AS previous_month_amount,
       ROUND((total_disbursed - LAG(total_disbursed) OVER (ORDER BY month))
             / LAG(total_disbursed) OVER (ORDER BY month) * 100, 2) AS pct_change
FROM monthly
ORDER BY month;

-- Q18: Fraud risk assessment
-- High: confirmed fraud or > 3 alerts | Medium: card utilisation > 80% | Low: otherwise
WITH alerts AS (
    SELECT customer_id,
           COUNT(*) AS num_alerts,
           SUM(CASE WHEN is_fraud_confirmed = TRUE THEN 1 ELSE 0 END) AS confirmed_count
    FROM FraudAlerts
    GROUP BY customer_id
),
cards AS (
    SELECT customer_id,
           MAX(current_balance / credit_limit * 100) AS max_utilisation
    FROM CreditCards
    GROUP BY customer_id
)
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       COALESCE(a.num_alerts, 0)      AS num_fraud_alerts,
       COALESCE(a.confirmed_count, 0) AS confirmed_fraud_count,
       ROUND(COALESCE(cd.max_utilisation, 0), 2) AS max_card_utilisation_pct,
       CASE
           WHEN COALESCE(a.confirmed_count, 0) > 0 OR COALESCE(a.num_alerts, 0) > 3 THEN 'High'
           WHEN COALESCE(cd.max_utilisation, 0) > 80 THEN 'Medium'
           ELSE 'Low'
       END AS risk_level
FROM Customers c
LEFT JOIN alerts a ON a.customer_id = c.customer_id
LEFT JOIN cards cd ON cd.customer_id = c.customer_id
WHERE COALESCE(a.num_alerts, 0) > 3
   OR COALESCE(a.confirmed_count, 0) > 0
   OR COALESCE(cd.max_utilisation, 0) > 80
ORDER BY num_fraud_alerts DESC, confirmed_fraud_count DESC;

-- Q19: Credit card + active loan, no investments
SELECT c.customer_id,
       CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       c.email,
       c.risk_profile
FROM Customers c
WHERE EXISTS (SELECT 1 FROM CreditCards cc
               WHERE cc.customer_id = c.customer_id)
  AND EXISTS (SELECT 1 FROM Loans l
               WHERE l.customer_id = c.customer_id
                 AND l.loan_status = 'Active')
  AND NOT EXISTS (SELECT 1 FROM Investments i
                   WHERE i.customer_id = c.customer_id)
ORDER BY c.customer_id;

-- Q20: Index-friendly query and index suggestion
SELECT *
FROM Transactions
WHERE account_id = 5001
  AND transaction_date BETWEEN '2024-01-01' AND '2024-03-31'
  AND amount > 1000
ORDER BY transaction_date;

-- Index suggestion (equality on account_id, range + sort on transaction_date, amount covered):
-- CREATE INDEX idx_txn_account_date_amount ON Transactions (account_id, transaction_date, amount);

-- Q21: Employee hierarchy (CEO / top-level = Level 1)
WITH RECURSIVE org AS (
    SELECT employee_id,
           CONCAT(first_name, ' ', last_name) AS employee_name,
           CAST(NULL AS CHAR(150)) AS manager_name,
           1 AS emp_level,
           department
    FROM Employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id,
           CONCAT(e.first_name, ' ', e.last_name),
           o.employee_name,
           o.emp_level + 1,
           e.department
    FROM Employees e
    JOIN org o ON e.manager_id = o.employee_id
)
SELECT employee_name, manager_name, emp_level AS level, department
FROM org
ORDER BY emp_level, employee_name;

-- Q22: Percentile rank of total balance within risk profile
WITH cust_balance AS (
    SELECT c.customer_id,
           CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
           c.risk_profile,
           SUM(a.current_balance) AS total_balance
    FROM Customers c
    JOIN Accounts a ON a.customer_id = c.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.risk_profile
)
SELECT customer_name,
       risk_profile,
       total_balance,
       ROUND(PERCENT_RANK() OVER (PARTITION BY risk_profile
                                  ORDER BY total_balance) * 100, 2) AS percentile_rank
FROM cust_balance
ORDER BY risk_profile, percentile_rank DESC;

-- Q23: Monthly EMI obligations for a customer (parameterised via @customer_id)
SET @customer_id = 1001;

SELECT loan_type, monthly_emi AS emi_amount
FROM Loans
WHERE customer_id = @customer_id
  AND loan_status = 'Active'
UNION ALL
SELECT 'TOTAL', COALESCE(SUM(monthly_emi), 0)
FROM Loans
WHERE customer_id = @customer_id
  AND loan_status = 'Active';

-- Stored procedure conversion: replace @customer_id with an IN parameter, e.g.
-- DELIMITER //
-- CREATE PROCEDURE sp_monthly_emi_obligation(IN p_customer_id INT)
-- BEGIN
--     SELECT loan_type, monthly_emi AS emi_amount
--       FROM Loans WHERE customer_id = p_customer_id AND loan_status = 'Active'
--     UNION ALL
--     SELECT 'TOTAL', COALESCE(SUM(monthly_emi), 0)
--       FROM Loans WHERE customer_id = p_customer_id AND loan_status = 'Active';
-- END //
-- DELIMITER ;
-- CALL sp_monthly_emi_obligation(1001);

-- Q24: Data integrity checks
WITH txn AS (
    SELECT transaction_id,
           account_id,
           balance_after,
           CASE WHEN transaction_type IN ('Deposit', 'Transfer In')
                THEN amount ELSE -amount END AS signed_amount,
           LAG(balance_after) OVER (PARTITION BY account_id
                                    ORDER BY transaction_date, transaction_id) AS prev_balance
    FROM Transactions
)
SELECT 'Negative Account Balance' AS issue_type,
       CAST(account_id AS CHAR)  AS affected_record_id,
       CONCAT('Balance: ', current_balance) AS details
FROM Accounts
WHERE current_balance < 0
UNION ALL
SELECT 'Outstanding Exceeds Loan Amount',
       CAST(loan_id AS CHAR),
       CONCAT('Outstanding: ', outstanding_balance, ', Loan Amount: ', loan_amount)
FROM Loans
WHERE outstanding_balance > loan_amount
UNION ALL
SELECT 'Negative Available Credit',
       CAST(card_id AS CHAR),
       CONCAT('Available Credit: ', available_credit)
FROM CreditCards
WHERE available_credit < 0
UNION ALL
SELECT 'Balance After Mismatch',
       CAST(transaction_id AS CHAR),
       CONCAT('Account: ', account_id, ', Expected: ', prev_balance + signed_amount,
              ', Recorded: ', balance_after)
FROM txn
WHERE prev_balance IS NOT NULL
  AND prev_balance + signed_amount <> balance_after;

-- Q25: Dashboard (month = latest month present in Transactions)
WITH ref AS (
    SELECT DATE_FORMAT(MAX(transaction_date), '%Y-%m-01') AS month_start
    FROM Transactions
),
risk AS (
    SELECT risk_profile, COUNT(*) AS cnt
    FROM Customers
    GROUP BY risk_profile
),
flow AS (
    SELECT COALESCE(SUM(CASE WHEN t.transaction_type IN ('Deposit', 'Transfer In')
                             THEN t.amount ELSE 0 END), 0) AS deposits,
           COALESCE(SUM(CASE WHEN t.transaction_type IN ('Withdrawal', 'Transfer Out')
                             THEN t.amount ELSE 0 END), 0) AS withdrawals
    FROM Transactions t
    JOIN ref ON t.transaction_date >= ref.month_start
            AND t.transaction_date <  DATE_ADD(ref.month_start, INTERVAL 1 MONTH)
),
util AS (
    SELECT card_type,
           ROUND(AVG(current_balance / credit_limit * 100), 2) AS avg_util
    FROM CreditCards
    GROUP BY card_type
),
health AS (
    SELECT ROUND(SUM(CASE WHEN payment_status = 'Paid' AND late_fee = 0 THEN 1 ELSE 0 END)
                 / COUNT(*) * 100, 2) AS on_time_pct
    FROM LoanPayments
),
top_cat AS (
    SELECT category, SUM(amount) AS volume
    FROM Transactions
    GROUP BY category
    ORDER BY volume DESC
    LIMIT 3
)
SELECT 'Customers by Risk Profile' AS section, risk_profile AS metric, cnt AS value FROM risk
UNION ALL
SELECT 'Monthly Cash Flow', 'Total Deposits', deposits FROM flow
UNION ALL
SELECT 'Monthly Cash Flow', 'Total Withdrawals', withdrawals FROM flow
UNION ALL
SELECT 'Monthly Cash Flow', 'Net Flow', deposits - withdrawals FROM flow
UNION ALL
SELECT 'Avg Card Utilisation (%)', card_type, avg_util FROM util
UNION ALL
SELECT 'Loan Portfolio Health', 'On-time Payments (%)', on_time_pct FROM health
UNION ALL
SELECT 'Top 3 Transaction Categories', category, volume FROM top_cat;
