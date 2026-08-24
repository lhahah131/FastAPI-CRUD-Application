--
-- PostgreSQL database dump
--

\restrict JpUJqXvKK7QTe02wmCwzAsauFWGNYuOoTiw0s4OZCGeXJL4qKcv3hDmFeyGagV7

-- Dumped from database version 15.19
-- Dumped by pg_dump version 15.19

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: items; Type: TABLE; Schema: public; Owner: Composer
--

CREATE TABLE public.items (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    price numeric(10,2) NOT NULL
);


ALTER TABLE public.items OWNER TO "Composer";

--
-- Name: items_id_seq; Type: SEQUENCE; Schema: public; Owner: Composer
--

CREATE SEQUENCE public.items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.items_id_seq OWNER TO "Composer";

--
-- Name: items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Composer
--

ALTER SEQUENCE public.items_id_seq OWNED BY public.items.id;


--
-- Name: items id; Type: DEFAULT; Schema: public; Owner: Composer
--

ALTER TABLE ONLY public.items ALTER COLUMN id SET DEFAULT nextval('public.items_id_seq'::regclass);


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: Composer
--

COPY public.items (id, name, description, price) FROM stdin;
\.


--
-- Name: items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Composer
--

SELECT pg_catalog.setval('public.items_id_seq', 1, false);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: Composer
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict JpUJqXvKK7QTe02wmCwzAsauFWGNYuOoTiw0s4OZCGeXJL4qKcv3hDmFeyGagV7

