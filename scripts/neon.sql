CREATE SEQUENCE public.neon_sites_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 5
  CACHE 1;
ALTER TABLE public.neon_sites_id_seq
  OWNER TO etlfires;


CREATE TABLE public.neon_sites
(
  id integer NOT NULL DEFAULT nextval('neon_sites_id_seq'::regclass),
  dataProducts text,
  domainCode character varying(250),
  domainName character varying(250),
  siteCode character varying(250),
  siteDescription character varying(250),
  siteName character varying(250),
  siteType character varying(250),
  stateCode character varying(2),
  stateName character varying(50),
  created_time timestamp with time zone default now(),
  geom geometry(Point,4326)
)

CREATE INDEX neon_sites_geom_gist
  ON public.neon_sites
  USING gist
  (geom);

ALTER TABLE public.neon_sites
  OWNER TO etlfires;
GRANT ALL ON TABLE public.neon_sites TO etlfires;
GRANT SELECT ON TABLE public.neon_sites TO public;
