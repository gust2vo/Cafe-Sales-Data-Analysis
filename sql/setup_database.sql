IF DB_ID('CafeSales') IS NULL
  BEGIN
    CREATE DATABASE CafeSales;
  END


GO
USE CafeSales;


GO
IF NOT EXISTS (SELECT 1
               FROM   sys.schemas
               WHERE  name = 'staging')
  BEGIN
    EXECUTE ('CREATE SCHEMA staging');
  END


GO
IF NOT EXISTS (SELECT 1
               FROM   sys.schemas
               WHERE  name = 'dw')
  BEGIN
    EXECUTE ('CREATE SCHEMA dw');
  END


GO
IF NOT EXISTS (SELECT 1
               FROM   sys.schemas
               WHERE  name = 'marts')
  BEGIN
    EXECUTE ('CREATE SCHEMA marts');
  END