-------------------------------------------------------tire_rack

SELECT DISTINCT c.make FROM car c 
-------------------------------------------------------tire_rack

SELECT ts.size, unnest(array_agg(concat(c.make, '-', c.year, '-',c.model))) AS cars
FROM tire_size ts JOIN car c ON ts.car_id = c.id
WHERE ts.size != '' AND c.make in ('BMW','Porsche','Audi','Lexus','Mercedes-Benz','Volvo','Volkswagen') AND c.year>2015
GROUP BY ts.size
ORDER BY ts.size

SELECT ts.front_size, unnest(array_agg(concat(c.make, '-', c.year, '-',c.model))) AS cars
FROM tire_size ts JOIN car c ON ts.car_id = c.id
WHERE ts.front_size != '' AND c.make in ('BMW','Porsche','Audi','Lexus','Mercedes-Benz','Volvo','Volkswagen') AND c.year>2015
GROUP BY ts.front_size
ORDER BY ts.front_size


SELECT ts.rear_size, unnest(array_agg(concat(c.make, '-', c.year, '-',c.model))) AS cars
FROM tire_size ts JOIN car c ON ts.car_id = c.id
WHERE ts.rear_size != '' AND c.make in ('BMW','Porsche','Audi','Lexus','Mercedes-Benz','Volvo','Volkswagen') AND c.year>2015
GROUP BY ts.rear_size
ORDER BY ts.rear_size


-------------------------------------------------------tire_rack
SELECT DISTINCT ts.size FROM tire_size ts JOIN car c ON ts.car_id = c.id WHERE ts.size != ''  AND c.make in ('BMW','Porsche','Audi','Lexus','Mercedes-Benz','Volvo','Volkswagen')
UNION
SELECT DISTINCT ts.front_size FROM tire_size ts JOIN car c ON ts.car_id = c.id WHERE ts.front_size != ''  AND c.make in ('BMW','Porsche','Audi','Lexus','Mercedes-Benz','Volvo','Volkswagen')
UNION
SELECT DISTINCT ts.rear_size FROM tire_size ts JOIN car c ON ts.car_id = c.id WHERE ts.rear_size != ''  AND c.make in ('BMW','Porsche','Audi','Lexus','Mercedes-Benz','Volvo','Volkswagen')

ORDER BY size

-------------------------------------------------------tire_rack

SELECT DISTINCT w.note FROM wiper w JOIN car c ON w.car_id = c.id WHERE c.make in ('BMW','Porsche','Audi','Lexus','Mercedes-Benz','Volvo','Volkswagen')

ORDER BY w.note

-------------------------------------------------------tire_rack

SELECT w.note,  unnest(array_agg(concat(c.make, '-', c.year, '-',c.model))) AS cars
FROM wiper w JOIN car c ON w.car_id = c.id
WHERE  c.make in ('BMW','Porsche','Audi','Lexus','Mercedes-Benz','Volvo','Volkswagen') AND c.year>2000
GROUP BY w.note
ORDER BY w.note

-------------------------------------------------------liqui_moly

SELECT DISTINCT c.make FROM car c 

-------------------------------------------------------liqui_moly


SELECT e.capacity,  unnest(array_agg(concat(c.make, '-', c.model, '-',c.sub_model))) AS cars
FROM engine e JOIN car c ON e.car_id = c.id
WHERE  c.make in ('BMW (EU)', 'Lexus (EU)','Volkswagen (VW) (EU)','Volvo (EU)','Volvo (EU)','Mercedes-Benz (EU)','Audi (EU)','Porsche (EU)') 
GROUP BY e.capacity
ORDER BY e.capacity



-------------------------------------------------------auto_data

SELECT DISTINCT c.make FROM car c 

-------------------------------------------------------auto_data

SELECT p.name, p.value ,unnest(array_agg(concat(c.make, '-', c.sub_model))) AS vehicle
FROM car c JOIN property p ON p.car_id = c.id
WHERE  c.make in ('BMW', 'Audi') AND p.name in ('Engine oil capacity')
GROUP BY p.name, p.value
ORDER BY p.name, p.value

SELECT p.name, p.value ,unnest(array_agg(concat(c.make, '-', c.sub_model))) AS vehicle
FROM car c JOIN property p ON p.car_id = c.id
WHERE  c.make in ('BMW', 'Audi') AND p.name in ('Tires size')
GROUP BY p.name, p.value
ORDER BY p.name, p.value