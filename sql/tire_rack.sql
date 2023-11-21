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
WHERE  c.make in ('BMW', 'Audi', 'Mercedes-Benz', 'Porsche') AND p.name in ('Engine oil capacity')
GROUP BY p.name, p.value
ORDER BY p.name, p.value

SELECT  p.value ,unnest(array_agg(concat(c.make, '-', c.sub_model))) AS vehicle
FROM car c JOIN property p ON p.car_id = c.id
WHERE  c.make in ('BMW', 'Audi', 'Mercedes-Benz', 'Porsche') AND p.name in ('Tires size') 
GROUP BY  p.value
ORDER BY  p.value


SELECT  p.value ,unnest(array_agg(concat(c.make, '-', c.sub_model))) AS vehicle
FROM car c JOIN property p ON p.car_id = c.id
WHERE  c.make in ('BMW', 'Audi', 'Mercedes-Benz', 'Porsche') AND p.name in ('simplify_tire_size') AND c.start_of_perduction_year >= 2008
GROUP BY  p.value
ORDER BY  p.value


SELECT DISTINCT p.value FROM property p JOIN car c ON p.car_id = c.id WHERE c.make in ('BMW', 'Audi', 'Mercedes-Benz', 'Porsche') and p.name='Tires size'
ORDER BY p.value




SELECT DISTINCT substring(p.value, 9,2) as od, p.value FROM property p JOIN car c ON p.car_id = c.id WHERE c.selected=true and p.name in ('simplify_tire_size_2','simplify_front_tire_size_2','simplify_rear_tire_size_2')
ORDER BY od




UPDATE car 
SET selected=true
WHERE make='Audi' and start_of_production_year>=2008 and model_category in (
    'A1',
    'A3',
    'A4',
    'A5',
    'A6',
    'A7',
    'A8',
    'e-tron',
    'e-tron GT',
    'Q2',
    'Q3',
    'Q4 e-tron',
    'Q5',
    'Q7',
    'Q8',
    'Q8 e-tron',
    'R8',
    'RS 3',
    'RS 4',
    'RS 5',
    'RS 6',
    'RS 7',
    'RS e-tron GT',
    'RS Q3',
    'RS Q8',
    'S1',
    'S3',
    'S4',
    'S5',
    'S6',
    'S7',
    'S8',
    'SQ2',
    'SQ5',
    'SQ7',
    'SQ8',
    'SQ8 e-tron',
    'TT') 


UPDATE car 
SET selected=true
WHERE make='BMW' and start_of_production_year>=2008 and model_category in (
'1 Series',
'2 Series',
'3 Series',
'4 Series',
'5 Series',
'6 Series',
'7 Series',
'8 Series',
'i3',
'i4',
'i5',
'i7',
'i8',
'iX',
'iX1',
'iX2',
'iX3',
'M2',
'M3',
'M4',
'M5',
'M6',
'M8',
'X1',
'X2',
'X3',
'X3 M',
'X4',
'X4 M',
'X5',
'X5 M',
'X6',
'X6 M',
'X7',
'XM',
'Z4'
) 


UPDATE car 
SET selected=true
WHERE make='Mercedes-Benz' and start_of_production_year>=2008 and model_category in (
'A-class',
'AMG GT',
'AMG GT 4-Door Coupe',
'B-class',
'C-class',
'CL',
'CLA',
'CLE',
'CLK',
'CLS',
'E-class',
'EQA',
'EQB',
'EQC',
'EQE',
'EQE SUV',
'EQG',
'EQS',
'EQS SUV',
'G-class',
'GL',
'GLA',
'GLB',
'GLC',
'GLE',
'GLK',
'GLS',
'M-class',
'R-class',
'S-class',
'SL',
'SLC',
'SLK',
'SLS',
'V-class',
'Vito') 



UPDATE car 
SET selected=true
WHERE make='Porsche' and start_of_production_year>=2008 and model_category in (

'718',
'911',
'Boxster',
'Cayenne',
'Cayman',
'Macan',
'Panamera',
'Taycan'
) 






