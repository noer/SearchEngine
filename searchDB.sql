CREATE TABLE public.document
(
  id serial,
  url character varying(255),
  "timestamp" timestamp without time zone,
  CONSTRAINT docid_idx PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.document
  OWNER TO search;


CREATE TABLE public.term
(
  id serial,
  value character varying(255),
  CONSTRAINT termid_idx PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.term
  OWNER TO search;

CREATE TABLE public.term_doc
(
  docid integer NOT NULL,
  termid integer NOT NULL,
  "position" integer NOT NULL,
  CONSTRAINT term_doc_id_idx PRIMARY KEY (docid, termid, "position"),
  CONSTRAINT fk_docid FOREIGN KEY (docid)
      REFERENCES public.document (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_termid FOREIGN KEY (termid)
      REFERENCES public.term (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.term_doc
  OWNER TO search;


--INSERT INTO document (url,timestamp) VALUES ('test.pdf', NOW()::timestamp)