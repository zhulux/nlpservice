-- run with psql <crawler_pg_uri> < export-corpus.sql

CREATE TEMP VIEW v1 AS
  with raw_news as (
    select * from (
      select unnest(string_to_array(title, '；')) as title, entity_name
      from data.news
    ) t
    where length(title) < 100
    and title ~ '[^[:ascii:]]'
    and entity_name IS NOT NULL
    and length(title) > 10
  ),

  simple_match as (
    select title, entity_name as e2
    from raw_news
    where position(entity_name in title) > 0
  ),

  nonmatch_news as (
    select title, entity_name
    from raw_news
    where position(entity_name in title) = 0
  ),

  splitted as (
    select title, e1 as e from
    (
      select title, entity_name, unnest(e) as e1
      from nonmatch_news,
      lateral regexp_matches(entity_name, '[[:ascii:]]+|[^[:ascii:]]+', 'g') as e
    ) t1
    where length(e1) >= 3
  ),

  match_stripped as (
    select title, e2 from (
      select title, e, regexp_replace(e, '(中国|汽车|投资基金|基金|创新|股份|通讯|分期|咖啡|集团|网|投资部|科技|食品|游戏|体育|创投|互联|实业|俱乐部)$', '') as e2
      from splitted
    ) t
    where e != e2
    and position(e in title) = 0 and position(e2 in title) > 0
  ),

  match_non_stripped as (
    select title, e as e2 from splitted
    where position(e in title) > 0
  ),

  match_nonsplit_stripped as (
    select title, e2 from (
      select title, regexp_replace(entity_name, '(中国|汽车|投资基金|基金|创新|股份|通讯|分期|咖啡|集团|网|投资部|科技|食品|游戏|体育|创投|互联|实业|俱乐部)$', '') as e2
      from nonmatch_news
      where position(entity_name in title) = 0
    ) t
    where position(e2 in title) > 0
  ),

  dataset as (
    select title, e2, ROW_NUMBER() OVER (partition by title order by length(e2) desc) rn
    from (
      select * from simple_match
      union
      select * from match_non_stripped
      union
      select * from match_stripped
      union
      select * from match_nonsplit_stripped
    ) t
  )

  select title, e2 as entity, position(e2 IN title) - 1 AS begin, length(e2) AS length
  from dataset
  where rn = 1
  and length(e2) >= 2
  order by random()
;


\copy (select * from v1) to 'company.csv' with csv header;

DROP VIEW v1;




