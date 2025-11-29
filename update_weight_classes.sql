-- SQL Script to Update Weight Classes for All Trainees
-- This script calculates and assigns weight classes based on the weight field
-- 
-- Weight Class Boundaries:
-- Flyweight: <= 50kg
-- Lightweight: 50 < weight <= 60kg
-- Welterweight: 60 < weight <= 70kg
-- Middleweight: 70 < weight <= 80kg
-- Light Heavyweight: 80 < weight <= 90kg
-- Heavyweight: > 90kg

UPDATE core_trainee
SET weight_class = 
    CASE 
        WHEN weight <= 50 THEN 'Flyweight'
        WHEN weight <= 60 THEN 'Lightweight'
        WHEN weight <= 70 THEN 'Welterweight'
        WHEN weight <= 80 THEN 'Middleweight'
        WHEN weight <= 90 THEN 'Light Heavyweight'
        ELSE 'Heavyweight'
    END
WHERE archived = 0;

-- Verify the update
SELECT 
    weight_class,
    COUNT(*) as count,
    MIN(weight) as min_weight,
    MAX(weight) as max_weight,
    AVG(weight) as avg_weight
FROM core_trainee
WHERE archived = 0
GROUP BY weight_class
ORDER BY min_weight;
