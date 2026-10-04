SELECT LPAD(CAST(postcode AS VARCHAR), 4, '0') AS postcode_txt, suburb FROM dim_postcode WHERE state='NT' ORDER BY postcode
