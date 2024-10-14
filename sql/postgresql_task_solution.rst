========================
POSTGRESQL TASK SOLUTION
========================

Used:  postgresql (14.12 (Homebrew))

Create database
===============
createdb domain_management

Create tables
=============

- create domain table

.. code-block:: sql
  CREATE TABLE domain (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      registered_at TIMESTAMP NOT NULL,
      unregistered_at TIMESTAMP,
      CONSTRAINT domain_unique_time UNIQUE (name, registered_at, unregistered_at),
      CHECK (registered_at < unregistered_at OR unregistered_at IS NULL)
  );


- create domain_flag table

.. code-block:: sql
  CREATE TABLE domain_flag (
      id SERIAL PRIMARY KEY,
      domain_id INT REFERENCES domain(id) ON DELETE CASCADE,
      flag VARCHAR(50) NOT NULL,
      enabled_at TIMESTAMP NOT NULL,
      disabled_at TIMESTAMP,
      CONSTRAINT no_past_disabled CHECK (disabled_at > enabled_at OR disabled_at IS NULL)
  );


Populate tables
===============

- domain table 

.. code-block:: sql
  INSERT INTO domain (name, registered_at, unregistered_at)
  VALUES 
  ('example.com', '2023-01-01 10:00:00', NULL),
  ('testdomain.com', '2022-01-01 10:00:00', '2023-01-01 10:00:00'),
  ('mywebsite.org', '2023-05-01 10:00:00', NULL); 


- domain_flag table

.. code-block:: sql
  INSERT INTO domain_flag (domain_id, flag, enabled_at, disabled_at)
  VALUES
  (1, 'EXPIRED', '2023-09-01 00:00:00', '2023-09-10 00:00:00'),
  (1, 'OUTZONE', '2023-09-01 00:00:00', NULL),
  (2, 'EXPIRED', '2022-12-01 00:00:00', '2023-01-01 10:00:00'),
  (3, 'DELETE_CANDIDATE', '2023-08-01 00:00:00', NULL);


Queryes
=======

- Write a SELECT query which will return fully qualified domain name of domains which are currently (at the time query is run) registered and do not have and active (valid) expiration (EXPIRED) flag.

.. code-block:: sql
  SELECT d.name 
  FROM domain d
  WHERE d.unregistered_at IS NULL
    AND d.id NOT IN (
      SELECT df.domain_id 
      FROM domain_flag df 
      WHERE df.flag = 'EXPIRED' AND df.disabled_at IS NULL
    );


- Write a ``SELECT`` query which will return fully qualified domain name of domains which have had active (valid) ``EXPIRED`` and ``OUTZONE`` flags (means both flags and not necessarily at the same time) in the past (relative to the query run time).

.. code-block:: sql
  SELECT DISTINCT d.name
  FROM domain d
  WHERE d.id IN (
      SELECT f1.domain_id
      FROM domain_flag f1
      WHERE f1.flag = 'EXPIRED'
  )
  AND d.id IN (
      SELECT f2.domain_id
      FROM domain_flag f2
      WHERE f2.flag = 'OUTZONE'
  );
