--
-- PostgreSQL database dump
--

\restrict CXcoguMn5fPwbmHWirvkfx69O5utC2zs403Og0KRynGvE2UFF598m4rPfPWtNG7

-- Dumped from database version 16.14 (Homebrew)
-- Dumped by pg_dump version 16.14 (Homebrew)

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

--
-- Name: gist_geometry_ops; Type: OPERATOR FAMILY; Schema: public; Owner: wangmingyu
--

CREATE OPERATOR FAMILY public.gist_geometry_ops USING gist;


ALTER OPERATOR FAMILY public.gist_geometry_ops USING gist OWNER TO wangmingyu;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: api_author; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_author (
    id integer NOT NULL,
    forenames text,
    surname text NOT NULL,
    gender character(1),
    link text,
    ol_id character varying(16),
    CONSTRAINT api_author_surname_check CHECK ((surname <> ''::text))
);


ALTER TABLE public.api_author OWNER TO wangmingyu;

--
-- Name: api_author_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_author_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_author_id_seq OWNER TO wangmingyu;

--
-- Name: api_author_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_author_id_seq OWNED BY public.api_author.id;


--
-- Name: api_collection; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_collection (
    id integer NOT NULL,
    text character varying(64) NOT NULL
);


ALTER TABLE public.api_collection OWNER TO wangmingyu;

--
-- Name: api_collection_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_collection_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_collection_id_seq OWNER TO wangmingyu;

--
-- Name: api_collection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_collection_id_seq OWNED BY public.api_collection.id;


--
-- Name: api_document; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_document (
    id integer NOT NULL,
    docid character varying(96) NOT NULL,
    title text NOT NULL,
    pubdate date,
    type character varying(32),
    majlang character varying(3),
    collection_id integer NOT NULL,
    url character varying(128),
    publisher_id integer,
    ol_id character varying(16),
    active boolean
);


ALTER TABLE public.api_document OWNER TO wangmingyu;

--
-- Name: api_document_author; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_document_author (
    author_id integer NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.api_document_author OWNER TO wangmingyu;

--
-- Name: api_document_genre; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_document_genre (
    genre_id integer NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.api_document_genre OWNER TO wangmingyu;

--
-- Name: api_document_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_document_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_document_id_seq OWNER TO wangmingyu;

--
-- Name: api_document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_document_id_seq OWNED BY public.api_document.id;


--
-- Name: api_genre; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_genre (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.api_genre OWNER TO wangmingyu;

--
-- Name: api_genre_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_genre_id_seq OWNER TO wangmingyu;

--
-- Name: api_genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_genre_id_seq OWNED BY public.api_genre.id;


--
-- Name: api_location; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_location (
    id bigint NOT NULL,
    text text,
    lat double precision,
    lon double precision,
    gazref text,
    ptype text
);


ALTER TABLE public.api_location OWNER TO wangmingyu;

--
-- Name: api_location_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_location_id_seq OWNER TO wangmingyu;

--
-- Name: api_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_location_id_seq OWNED BY public.api_location.id;


--
-- Name: api_locationmention; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_locationmention (
    id integer NOT NULL,
    text character varying(128) NOT NULL,
    start_word character varying(10) NOT NULL,
    end_word character varying(10) NOT NULL,
    document_id integer NOT NULL,
    location_id integer NOT NULL,
    page_id integer NOT NULL,
    sentence_id integer NOT NULL
);


ALTER TABLE public.api_locationmention OWNER TO wangmingyu;

--
-- Name: api_locationmention_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_locationmention_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_locationmention_id_seq OWNER TO wangmingyu;

--
-- Name: api_locationmention_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_locationmention_id_seq OWNED BY public.api_locationmention.id;


--
-- Name: api_page; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_page (
    id integer NOT NULL,
    lang character varying(16),
    document_id integer NOT NULL,
    url character varying(200)
);


ALTER TABLE public.api_page OWNER TO wangmingyu;

--
-- Name: api_page_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_page_id_seq OWNER TO wangmingyu;

--
-- Name: api_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_page_id_seq OWNED BY public.api_page.id;


--
-- Name: api_partofspeech; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_partofspeech (
    id integer NOT NULL,
    tag character varying(4) NOT NULL,
    description character varying(40)
);


ALTER TABLE public.api_partofspeech OWNER TO wangmingyu;

--
-- Name: api_partofspeech_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_partofspeech_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_partofspeech_id_seq OWNER TO wangmingyu;

--
-- Name: api_partofspeech_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_partofspeech_id_seq OWNED BY public.api_partofspeech.id;


--
-- Name: api_posmention; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_posmention (
    id integer NOT NULL,
    text character varying(128) NOT NULL,
    pos_id integer NOT NULL,
    sentence_id integer NOT NULL
);


ALTER TABLE public.api_posmention OWNER TO wangmingyu;

--
-- Name: api_posmention_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_posmention_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_posmention_id_seq OWNER TO wangmingyu;

--
-- Name: api_posmention_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_posmention_id_seq OWNED BY public.api_posmention.id;


--
-- Name: api_publisher; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_publisher (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.api_publisher OWNER TO wangmingyu;

--
-- Name: api_publisher_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_publisher_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_publisher_id_seq OWNER TO wangmingyu;

--
-- Name: api_publisher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_publisher_id_seq OWNED BY public.api_publisher.id;


--
-- Name: api_sentence; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.api_sentence (
    id integer NOT NULL,
    identifier character varying(10) NOT NULL,
    text text NOT NULL,
    xml text NOT NULL,
    i_score double precision,
    palsnippet boolean NOT NULL,
    page_id integer NOT NULL
);


ALTER TABLE public.api_sentence OWNER TO wangmingyu;

--
-- Name: api_sentence_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.api_sentence_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_sentence_id_seq OWNER TO wangmingyu;

--
-- Name: api_sentence_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.api_sentence_id_seq OWNED BY public.api_sentence.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO wangmingyu;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auth_group_id_seq OWNER TO wangmingyu;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO wangmingyu;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auth_group_permissions_id_seq OWNER TO wangmingyu;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO wangmingyu;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auth_permission_id_seq OWNER TO wangmingyu;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO wangmingyu;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO wangmingyu;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auth_user_groups_id_seq OWNER TO wangmingyu;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auth_user_id_seq OWNER TO wangmingyu;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO wangmingyu;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNER TO wangmingyu;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO wangmingyu;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.django_admin_log_id_seq OWNER TO wangmingyu;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO wangmingyu;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.django_content_type_id_seq OWNER TO wangmingyu;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO wangmingyu;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: wangmingyu
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.django_migrations_id_seq OWNER TO wangmingyu;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wangmingyu
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO wangmingyu;

--
-- Name: mention_order; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.mention_order (
    id bigint,
    document_id bigint,
    location_id bigint,
    word_num bigint,
    mention_order bigint,
    position_pct double precision
);


ALTER TABLE public.mention_order OWNER TO wangmingyu;

--
-- Name: sentence_fts; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.sentence_fts (
    sentence_id integer,
    fts_tokens tsvector
);


ALTER TABLE public.sentence_fts OWNER TO wangmingyu;

--
-- Name: snippets; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.snippets (
    coll_id integer,
    coll_text character varying(64),
    fts_tokens tsvector,
    doc_id integer,
    doc_title text,
    doc_author text,
    page_url character varying,
    snippet text,
    decade text,
    loc_id integer,
    loc_name character varying(128)
);


ALTER TABLE public.snippets OWNER TO wangmingyu;

--
-- Name: version; Type: TABLE; Schema: public; Owner: wangmingyu
--

CREATE TABLE public.version (
    version character varying(5),
    "timestamp" timestamp without time zone DEFAULT now(),
    description text
);


ALTER TABLE public.version OWNER TO wangmingyu;

--
-- Name: api_author id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_author ALTER COLUMN id SET DEFAULT nextval('public.api_author_id_seq'::regclass);


--
-- Name: api_collection id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_collection ALTER COLUMN id SET DEFAULT nextval('public.api_collection_id_seq'::regclass);


--
-- Name: api_document id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_document ALTER COLUMN id SET DEFAULT nextval('public.api_document_id_seq'::regclass);


--
-- Name: api_genre id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_genre ALTER COLUMN id SET DEFAULT nextval('public.api_genre_id_seq'::regclass);


--
-- Name: api_location id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_location ALTER COLUMN id SET DEFAULT nextval('public.api_location_id_seq'::regclass);


--
-- Name: api_locationmention id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_locationmention ALTER COLUMN id SET DEFAULT nextval('public.api_locationmention_id_seq'::regclass);


--
-- Name: api_page id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_page ALTER COLUMN id SET DEFAULT nextval('public.api_page_id_seq'::regclass);


--
-- Name: api_partofspeech id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_partofspeech ALTER COLUMN id SET DEFAULT nextval('public.api_partofspeech_id_seq'::regclass);


--
-- Name: api_posmention id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_posmention ALTER COLUMN id SET DEFAULT nextval('public.api_posmention_id_seq'::regclass);


--
-- Name: api_publisher id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_publisher ALTER COLUMN id SET DEFAULT nextval('public.api_publisher_id_seq'::regclass);


--
-- Name: api_sentence id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_sentence ALTER COLUMN id SET DEFAULT nextval('public.api_sentence_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: api_author api_author_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_author
    ADD CONSTRAINT api_author_pkey PRIMARY KEY (id);


--
-- Name: api_collection api_collection_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_collection
    ADD CONSTRAINT api_collection_pkey PRIMARY KEY (id);


--
-- Name: api_document api_document_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_document
    ADD CONSTRAINT api_document_pkey PRIMARY KEY (id);


--
-- Name: api_genre api_genre_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_genre
    ADD CONSTRAINT api_genre_pkey PRIMARY KEY (id);


--
-- Name: api_location api_location_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_location
    ADD CONSTRAINT api_location_pkey PRIMARY KEY (id);


--
-- Name: api_locationmention api_locationmention_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_locationmention
    ADD CONSTRAINT api_locationmention_pkey PRIMARY KEY (id);


--
-- Name: api_page api_page_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_page
    ADD CONSTRAINT api_page_pkey PRIMARY KEY (id);


--
-- Name: api_partofspeech api_partofspeech_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_partofspeech
    ADD CONSTRAINT api_partofspeech_pkey PRIMARY KEY (id);


--
-- Name: api_posmention api_posmention_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_posmention
    ADD CONSTRAINT api_posmention_pkey PRIMARY KEY (id);


--
-- Name: api_publisher api_publisher_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_publisher
    ADD CONSTRAINT api_publisher_pkey PRIMARY KEY (id);


--
-- Name: api_sentence api_sentence_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_sentence
    ADD CONSTRAINT api_sentence_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_45f3b1d93ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_45f3b1d93ec8c61c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: api_document_0a1a4dd8; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX api_document_0a1a4dd8 ON public.api_document USING btree (collection_id);


--
-- Name: api_locationmention_1a63c800; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX api_locationmention_1a63c800 ON public.api_locationmention USING btree (page_id);


--
-- Name: api_locationmention_28fb0fea; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX api_locationmention_28fb0fea ON public.api_locationmention USING btree (sentence_id);


--
-- Name: api_locationmention_e274a5da; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX api_locationmention_e274a5da ON public.api_locationmention USING btree (location_id);


--
-- Name: api_locationmention_e7fafc10; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX api_locationmention_e7fafc10 ON public.api_locationmention USING btree (document_id);


--
-- Name: api_page_e7fafc10; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX api_page_e7fafc10 ON public.api_page USING btree (document_id);


--
-- Name: api_posmention_28fb0fea; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX api_posmention_28fb0fea ON public.api_posmention USING btree (sentence_id);


--
-- Name: api_posmention_6e6e97e3; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX api_posmention_6e6e97e3 ON public.api_posmention USING btree (pos_id);


--
-- Name: api_sentence_1a63c800; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX api_sentence_1a63c800 ON public.api_sentence USING btree (page_id);


--
-- Name: api_sentence_text_idx; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX api_sentence_text_idx ON public.api_sentence USING hash (text);


--
-- Name: auth_group_name_253ae2a6331666e8_like; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX auth_group_name_253ae2a6331666e8_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX auth_group_permissions_0e939a4f ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX auth_group_permissions_8373b171 ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX auth_permission_417f1b1c ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX auth_user_groups_0e939a4f ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX auth_user_groups_e8701ad4 ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX auth_user_user_permissions_8373b171 ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_51b3b110094b8aae_like; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX auth_user_username_51b3b110094b8aae_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX django_admin_log_417f1b1c ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX django_admin_log_e8701ad4 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX django_session_de54fa62 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_461cfeaa630ca218_like; Type: INDEX; Schema: public; Owner: wangmingyu
--

CREATE INDEX django_session_session_key_461cfeaa630ca218_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: api_document api_documen_collection_id_641804d29f1962b0_fk_api_collection_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_document
    ADD CONSTRAINT api_documen_collection_id_641804d29f1962b0_fk_api_collection_id FOREIGN KEY (collection_id) REFERENCES public.api_collection(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: api_document_author api_document_author_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_document_author
    ADD CONSTRAINT api_document_author_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.api_author(id);


--
-- Name: api_document_author api_document_author_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_document_author
    ADD CONSTRAINT api_document_author_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.api_document(id);


--
-- Name: api_document_genre api_document_genre_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_document_genre
    ADD CONSTRAINT api_document_genre_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.api_document(id);


--
-- Name: api_document_genre api_document_genre_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_document_genre
    ADD CONSTRAINT api_document_genre_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.api_genre(id);


--
-- Name: api_document api_document_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_document
    ADD CONSTRAINT api_document_publisher_id_fkey FOREIGN KEY (publisher_id) REFERENCES public.api_publisher(id);


--
-- Name: api_locationmention api_locationmen_document_id_255c0ea38cd05852_fk_api_document_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_locationmention
    ADD CONSTRAINT api_locationmen_document_id_255c0ea38cd05852_fk_api_document_id FOREIGN KEY (document_id) REFERENCES public.api_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: api_locationmention api_locationmen_sentence_id_2ee86ab896aa8ed2_fk_api_sentence_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_locationmention
    ADD CONSTRAINT api_locationmen_sentence_id_2ee86ab896aa8ed2_fk_api_sentence_id FOREIGN KEY (sentence_id) REFERENCES public.api_sentence(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: api_locationmention api_locationmention_page_id_1ff81c900862d654_fk_api_page_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_locationmention
    ADD CONSTRAINT api_locationmention_page_id_1ff81c900862d654_fk_api_page_id FOREIGN KEY (page_id) REFERENCES public.api_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: api_page api_page_document_id_255e859680f28deb_fk_api_document_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_page
    ADD CONSTRAINT api_page_document_id_255e859680f28deb_fk_api_document_id FOREIGN KEY (document_id) REFERENCES public.api_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: api_posmention api_posmention_pos_id_3ea031194c2879be_fk_api_partofspeech_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_posmention
    ADD CONSTRAINT api_posmention_pos_id_3ea031194c2879be_fk_api_partofspeech_id FOREIGN KEY (pos_id) REFERENCES public.api_partofspeech(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: api_posmention api_posmention_sentence_id_464d90ed58b66d8c_fk_api_sentence_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_posmention
    ADD CONSTRAINT api_posmention_sentence_id_464d90ed58b66d8c_fk_api_sentence_id FOREIGN KEY (sentence_id) REFERENCES public.api_sentence(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: api_sentence api_sentence_page_id_7539129a747f83d9_fk_api_page_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.api_sentence
    ADD CONSTRAINT api_sentence_page_id_7539129a747f83d9_fk_api_page_id FOREIGN KEY (page_id) REFERENCES public.api_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_content_type_id_508cf46651277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_content_type_id_508cf46651277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log djan_content_type_id_697914295151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT djan_content_type_id_697914295151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: wangmingyu
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict CXcoguMn5fPwbmHWirvkfx69O5utC2zs403Og0KRynGvE2UFF598m4rPfPWtNG7

