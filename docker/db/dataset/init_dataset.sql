CREATE TABLE public."user" (
	id uuid NOT NULL,
	created timestamp NOT NULL,
	updated timestamp NOT NULL,
	username varchar NOT NULL,
	email varchar NOT NULL,
	"password" varchar NOT NULL,
	disabled bool NOT NULL,
	"role" int4 NOT NULL,
	CONSTRAINT user_email_key UNIQUE (email),
	CONSTRAINT user_pkey PRIMARY KEY (id)
);

COPY public."user"
FROM '/docker-entrypoint-initdb.d/initial_users.csv'
DELIMITER ','
CSV HEADER;