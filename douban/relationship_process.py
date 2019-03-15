import csv
import pandas as pd

df = pd.read_csv('douban.csv', encoding='utf-8')
df_film = pd.read_csv('film.csv', encoding='utf-8')
df_director = pd.read_csv('director.csv', encoding='utf-8')
df_actor = pd.read_csv('actor.csv', encoding='utf-8')
df_types = pd.read_csv('types.csv', encoding='utf-8')

# # 生成关系文件

director_films = []
actor_films = []
director_actors = []
film_types = []

for index, row in df.iterrows():
    # print(row)
    film_name = row['电影名称']
    director = row['导演']
    actor = row['演员']
    types = row['类型']

    directorList = director.split('/')
    actorList = actor.split('/')
    typeList = types.split('/')
    # 获取电影ID
    filmID = df_film['index:ID'].loc[df_film['film'] == film_name].values[0]

    # 生成导演-电影关系
    for dir in directorList:
        directorID = df_director['index:ID'].loc[df_director['director']==dir].values[0]
        director_film = [directorID, filmID, '导演', '导演']
        director_films.append(director_film)

    # 生成演员-电影关系
    for act in actorList:
        actorID = df_actor['index:ID'].loc[df_actor['actor']==act].values[0]
        actor_film = [actorID, filmID, '出演', '出演']
        actor_films.append(actor_film)

    # 生成导演-演员关系
    for dir in directorList:
        directorID = df_director['index:ID'].loc[df_director['director'] == dir].values[0]
        for act in actorList:
            actorID = df_actor['index:ID'].loc[df_actor['actor'] == act].values[0]
            director_actor = [directorID, actorID, '合作', '合作']
            director_actors.append(director_actor)


    # 生成电影-类型关系
    for ty in typeList:
        typeID = df_types['index:ID'].loc[df_types['types'] == ty].values[0]
        film_type = [filmID, typeID, '属于类型', '属于类型']
        film_types.append(film_type)

# 导出导演-电影关系文件
df_director_film = pd.DataFrame(data=director_films, columns=[':START_ID', ':END_ID', 'relation', ':TYPE'])
df_director_film.to_csv('relationship_director_film.csv', index=False, encoding='utf-8_sig')
print('导演-电影关系导出到CSV成功')

# 生成演员-电影关系
df_actor_film = pd.DataFrame(data=actor_films, columns=[':START_ID', ':END_ID', 'relation', ':TYPE'])
df_actor_film.to_csv('relationship_actor_film.csv', index=False, encoding='utf-8_sig')
print('演员-电影关系导出到CSV成功')

# 生成导演-演员关系
df_director_actor = pd.DataFrame(data=director_actors, columns=[':START_ID', ':END_ID', 'relation', ':TYPE'])
df_director_actor.to_csv('relationship_director_actor.csv', index=False, encoding='utf-8_sig')
print('导演-演员关系导出到CSV成功')

# 生成电影-类型关系
df_film_type = pd.DataFrame(data=film_types, columns=[':START_ID', ':END_ID', 'relation', ':TYPE'])
df_film_type.to_csv('relationship_film_type.csv', index=False, encoding='utf-8_sig')
print('电影-类型关系导出到CSV成功')