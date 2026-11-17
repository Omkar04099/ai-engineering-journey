-- 1. INSERT
INSERT INTO expenses (title, amount, category)
VALUES
    ('Dinner', 350, 'Food'),
    ('Petrol', 600, 'Travel'),
    ('Shopping', 1200, 'Personal');


-- 2. SELECT
SELECT * FROM expenses;

SELECT title, amount
FROM expenses;

SELECT *
FROM expenses
WHERE category = 'Food';

SELECT *
FROM expenses
WHERE amount > 500;


-- 3. ORDER BY, LIMIT and OFFSET
SELECT *
FROM expenses
ORDER BY amount DESC;

-- Second-highest expense
SELECT *
FROM expenses
ORDER BY amount DESC
LIMIT 1 OFFSET 1;


-- 4. UPDATE
UPDATE expenses
SET amount = 400
WHERE id = 1;

UPDATE expenses
SET amount = amount * 1.10
WHERE category = 'Travel';


-- 5. DELETE
DELETE FROM expenses
WHERE id = 3;


-- 6. COUNT
SELECT COUNT(*) AS total_expenses
FROM expenses;