ALTER ROLE tgphonecheckuser SET client_encoding TO 'utf8';
ALTER ROLE tgphonecheckuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE tgphonecheckuser SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE tgphonecheck TO tgphonecheckuser;


