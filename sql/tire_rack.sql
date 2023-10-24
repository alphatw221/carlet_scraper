-------------------------------------------------------

SELECT ts.size, unnest(array_agg(concat(c.make, '-', c.year, '-',c.model))) AS cars
FROM tire_size ts JOIN car c ON ts.car_id = c.id
WHERE ts.size != '' AND c.make in ('BMW') AND c.year>2015
GROUP BY ts.size
ORDER BY ts.size

SELECT ts.front_size, unnest(array_agg(concat(c.make, '-', c.year, '-',c.model))) AS cars
FROM tire_size ts JOIN car c ON ts.car_id = c.id
WHERE ts.front_size != '' AND c.make in ('BMW') AND c.year>2000
GROUP BY ts.front_size
ORDER BY ts.front_size


SELECT ts.rear_size, unnest(array_agg(concat(c.make, '-', c.year, '-',c.model))) AS cars
FROM tire_size ts JOIN car c ON ts.car_id = c.id
WHERE ts.rear_size != '' AND c.make in ('BMW') AND c.year>2000
GROUP BY ts.rear_size
ORDER BY ts.rear_size
-------------------------------------------------------

SELECT DISTINCT c.make FROM car c 


-------------------------------------------------------
SELECT DISTINCT ts.size FROM tire_size ts JOIN car c ON ts.car_id = c.id WHERE ts.size != ''  AND c.make in ('BMW')
UNION
SELECT DISTINCT ts.front_size FROM tire_size ts JOIN car c ON ts.car_id = c.id WHERE ts.front_size != ''  AND c.make in ('BMW')
UNION
SELECT DISTINCT ts.rear_size FROM tire_size ts JOIN car c ON ts.car_id = c.id WHERE ts.rear_size != ''  AND c.make in ('BMW')

ORDER BY size

-------------------------------------------------------

SELECT DISTINCT w.note FROM wiper w JOIN car c ON w.car_id = c.id WHERE c.make in ('BMW')

ORDER BY w.note

-------------------------------------------------------

SELECT w.note,  unnest(array_agg(concat(c.make, '-', c.year, '-',c.model))) AS cars
FROM wiper w JOIN car c ON w.car_id = c.id
WHERE  c.make in ('BMW') AND c.year>2000
GROUP BY w.note
ORDER BY w.note

-------------------------------------------------------

SELECT DISTINCT c.make FROM car c 

-------------------------------------------------------


SELECT e.capacity,  unnest(array_agg(concat(c.make, '-', c.model, '-',c.sub_model))) AS cars
FROM engine e JOIN car c ON e.car_id = c.id
WHERE  c.make in ('BMW (EU)', 'Lexus (EU)','Volkswagen (VW) (EU)','Volvo (EU)','Volvo (EU)','Mercedes-Benz (EU)','Audi (EU)','Porsche (EU)') 
GROUP BY e.capacity
ORDER BY e.capacity
