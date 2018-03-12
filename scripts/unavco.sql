CREATE SEQUENCE public.unavco_sites_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 5
  CACHE 1;
ALTER TABLE public.unavco_sites_id_seq
  OWNER TO etlfires;


CREATE TABLE public.unavco_sites
(
  unavco_sites_id integer NOT NULL DEFAULT nextval('unavco_sites_id_seq'::regclass),
  id character varying(4),
  stationName character varying(250),
  startTime timestamp with time zone,
  stopTime timestamp with time zone,
  created_time timestamp with time zone default now(),
  geom geometry(PointZ,4326)
)

CREATE INDEX unavco_sites_geom_gist
  ON public.unavco_sites
  USING gist
  (geom);

ALTER TABLE public.unavco_sites
  OWNER TO etlfires;
GRANT ALL ON TABLE public.unavco_sites TO etlfires;
GRANT SELECT ON TABLE public.unavco_sites TO public;
