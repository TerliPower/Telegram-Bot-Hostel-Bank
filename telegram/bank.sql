PGDMP     !                    {            bank #   14.7 (Ubuntu 14.7-0ubuntu0.22.04.1) #   14.7 (Ubuntu 14.7-0ubuntu0.22.04.1)     1           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            2           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            3           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            4           1262    16445    bank    DATABASE     Y   CREATE DATABASE bank WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8';
    DROP DATABASE bank;
                postgres    false            5           0    0    DATABASE bank    ACL     *   GRANT CONNECT ON DATABASE bank TO myuser;
                   postgres    false    3380            �            1259    16506    users    TABLE       CREATE TABLE public.users (
    id bigint NOT NULL,
    name text,
    rrid bigint,
    code bigint,
    emitent text,
    "✅Ривалы" bigint,
    "✅Ривалы_yes" bigint,
    "✅Ривалы_pyes" bigint,
    "✅Ривалы_ppyes" bigint,
    "✅Ривалы_mean" bigint,
    "Хостел_Коины" bigint,
    "Хостел_Коины_yes" bigint,
    "Хостел_Коины_pyes" bigint,
    "Хостел_Коины_ppyes" bigint,
    "Хостел_Коины_mean" bigint,
    tgid integer
);
    DROP TABLE public.users;
       public         heap    myuser    false            �            1259    16505    users_id_seq    SEQUENCE     u   CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          myuser    false    215            6           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          myuser    false    214            �            1259    16500    bonds    TABLE       CREATE TABLE public.bonds (
    id bigint DEFAULT nextval('public.users_id_seq'::regclass) NOT NULL,
    description text,
    name text,
    emitent text,
    couponcurr text,
    couponprice bigint,
    commonamount bigint,
    dates text,
    isdef boolean
);
    DROP TABLE public.bonds;
       public         heap    myuser    false    214            �            1259    16487    exchange    TABLE     �   CREATE TABLE public.exchange (
    id bigint NOT NULL,
    name text,
    get text,
    send text,
    amount bigint,
    reserve bigint,
    tgid integer
);
    DROP TABLE public.exchange;
       public         heap    myuser    false            �            1259    16486    exchange_id_seq    SEQUENCE     x   CREATE SEQUENCE public.exchange_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.exchange_id_seq;
       public          myuser    false    212            7           0    0    exchange_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.exchange_id_seq OWNED BY public.exchange.id;
          public          myuser    false    211            �           2604    16490    exchange id    DEFAULT     j   ALTER TABLE ONLY public.exchange ALTER COLUMN id SET DEFAULT nextval('public.exchange_id_seq'::regclass);
 :   ALTER TABLE public.exchange ALTER COLUMN id DROP DEFAULT;
       public          myuser    false    211    212    212            �           2604    16509    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          myuser    false    214    215    215            ,          0    16500    bonds 
   TABLE DATA           t   COPY public.bonds (id, description, name, emitent, couponcurr, couponprice, commonamount, dates, isdef) FROM stdin;
    public          myuser    false    213           +          0    16487    exchange 
   TABLE DATA           N   COPY public.exchange (id, name, get, send, amount, reserve, tgid) FROM stdin;
    public          myuser    false    212   =       .          0    16506    users 
   TABLE DATA           R  COPY public.users (id, name, rrid, code, emitent, "✅Ривалы", "✅Ривалы_yes", "✅Ривалы_pyes", "✅Ривалы_ppyes", "✅Ривалы_mean", "Хостел_Коины", "Хостел_Коины_yes", "Хостел_Коины_pyes", "Хостел_Коины_ppyes", "Хостел_Коины_mean", tgid) FROM stdin;
    public          myuser    false    215   Z       8           0    0    exchange_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.exchange_id_seq', 6, true);
          public          myuser    false    211            9           0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 20, true);
          public          myuser    false    214            �           2606    16519 .   exchange idx_16487_sqlite_autoindex_exchange_1 
   CONSTRAINT     l   ALTER TABLE ONLY public.exchange
    ADD CONSTRAINT idx_16487_sqlite_autoindex_exchange_1 PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.exchange DROP CONSTRAINT idx_16487_sqlite_autoindex_exchange_1;
       public            myuser    false    212            �           2606    16520    bonds idx_16500_bonds_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.bonds
    ADD CONSTRAINT idx_16500_bonds_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.bonds DROP CONSTRAINT idx_16500_bonds_pkey;
       public            myuser    false    213            �           2606    16522    users idx_16506_users_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.users
    ADD CONSTRAINT idx_16506_users_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.users DROP CONSTRAINT idx_16506_users_pkey;
       public            myuser    false    215            ,      x������ � �      +      x������ � �      .   �   x��O�J1<'�������(�Yd����ð�,���Q���w?A�����Y��8^lR���jf���k��l����L�.V� ? 3/� ! X��͈y�����6_����6��m��v�:!x�%��1x�?﹨�.$B��\�~̫W3AH�Y�NA
��H�������|w�˓&	�$Q�)/e?=L�嵼o�sٗ��1=�T4�#�t$�A�5����g�͢��������(�jX     