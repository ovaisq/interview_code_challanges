--table with column name id which is of type int
SELECT MAX(id)
FROM (SELECT id
      FROM patient_documents
      ORDER BY id DESC
      LIMIT 1 OFFSET 1
) AS sq;
