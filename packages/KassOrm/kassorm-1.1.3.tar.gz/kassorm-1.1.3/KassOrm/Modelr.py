import json
from datetime import date
from datetime import datetime as dt
from .Querier import Querier


class HasMany:

    def run(self, rows: list, conn: dict, __has: dict):
        ids = []
        for row in rows:
            ids.append(str(row[__has["local_key"]]))
        ids = ", ".join(ids)

        related_rows = Querier(conn=conn).selectRaw(
            f"""
            SELECT 
                MODEL.* , 
                PIVOT.{__has['pivot_local_key']} AS pivot_{__has['pivot_local_key']},
                PIVOT.{__has['pivot_model_key']} AS pivot_{__has['pivot_model_key']}
            FROM {__has['model'].__table__} MODEL 
            INNER JOIN {__has['pivot_table']} PIVOT ON 
                MODEL.{__has['model_key']} = PIVOT.{__has['pivot_model_key']} 
            WHERE PIVOT.{__has['pivot_local_key']} in ({ids})"""
        )

        for row in rows:
            row[__has["related_name"]] = []
            for row2 in related_rows:
                if row[__has["local_key"]] == row2[f"pivot_{__has['pivot_local_key']}"]:
                    row[__has["related_name"]].append(row2)

        return rows


class HasOne:
    def run(self, rows: list, conn: dict, __has: dict):
        ids = []
        for row in rows:
            ids.append(str(row[__has["local_key"]]))
        ids = ", ".join(ids)

        related_rows = Querier(conn=conn).selectRaw(
            f"""
            SELECT * FROM {__has['model'].__table__} WHERE 
            """
        )

        for row in rows:
            row[__has["related_name"]] = {}
            for row2 in related_rows:
                if row[__has["local_key"]] == row2[f"pivot_{__has['pivot_local_key']}"]:
                    row[__has["related_name"]] = row2

        return rows


class Modelr:

    __conn__ = None
    __table__ = None
    __softdelete__ = None

    def __init__(self) -> None:
        self.querier = Querier(conn=self.__conn__).table(self.__table__)
        self.withtrashed = False

        self.__has = {}

    def withTrashed(self):
        self.withtrashed = True
        return self

    def __with_trash(self):
        if self.__softdelete__ is not None and self.withtrashed == False:
            return True
        else:
            return False

    def select(self, cols: str | list[str] = "*"):
        self.querier.select(cols)
        return self

    def where(self, conditional: list[dict] | dict):
        self.querier.where(conditional)
        return self

    def orWhere(self, conditional: list[dict] | dict):
        self.querier.orWhere(conditional)
        return self

    def whereIn(self, column: str, values: list[str]):
        self.querier.whereIn(column, values)
        return self

    def orWhereIn(self, column: str, values: list[str]):
        self.querier.orWhereIn(column, values)
        return self

    def whereNotIn(self, column: str, values: list[str]):
        self.querier.whereNotIn(column, values)
        return self

    def orWhereNotIn(self, column: str, values: list[str]):
        self.querier.orWhereNotIn(column, values)
        return self

    def whereIsNull(self, column: str):
        self.querier.whereIsNull(column)
        return self

    def orWhereIsNull(self, column: str):
        self.querier.orWhereIsNull(column)
        return self

    def whereIsNotNull(self, column: str):
        self.querier.whereIsNotNull(column)
        return self

    def orWhereIsNotNull(self, column: str):
        self.querier.orWhereIsNotNull(column)
        return self

    def whereLike(self, column: str, value: str):
        self.querier.whereLike(column, value)
        return self

    def orWhereLike(self, column: str, value: str):
        self.querier.orWhereLike(column, value)
        return self

    def whereBetween(self, column: str, dat1: str, dat2: str):
        self.querier.whereBetween(column, dat1, dat2)
        return self

    def orWhereBetween(self, column: str, dat1: str, dat2: str):
        self.querier.orWhereBetween(column, dat1, dat2)
        return self

    def limit(self, limit: int):
        self.querier.limit(limit)
        return self

    def offset(self, offset: int):
        self.querier.offset(offset)
        return self

    def groupBy(self, value: str | list[str]):
        self.querier.groupBy(value)
        return self

    def orderBy(self, value: str | list[str]):
        self.querier.orderBy(value)
        return self

    def json_date_serializer(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()

    def get(self):
        if self.__with_trash():
            self.querier.whereIsNull(self.__softdelete__)

        rows = self.querier.get()

        if self.__has:
            if self.__has["related_type"] == "HasMany":
                rows = HasMany().run(rows, self.__conn__, self.__has)
            elif self.__has["related_type"] == "HasOne":
                rows = HasOne().run(rows, self.__conn__, self.__has)

        rows = json.dumps(rows, default=self.json_date_serializer)
        return json.loads(rows)

    def first(self):
        if self.__with_trash():
            self.querier.whereIsNull(self.__softdelete__)

        row = self.querier.first()

        if self.__has:
            if self.__has["related_type"] == "HasMany":
                row = HasMany().run(row, self.__conn__, self.__has)
            elif self.__has["related_type"] == "HasOne":
                row = HasOne().run(row, self.__conn__, self.__has)

        row = json.dumps(row, default=self.json_date_serializer)
        return json.loads(row)

    def toSql(self, formmated: bool = True):
        return self.querier.toSql(formmated)

    def delete(self):
        if self.__with_trash():
            return self.querier.update({self.__softdelete__: dt.now()})
        return self.querier.delete()

    def active(self):
        if self.__with_trash():
            return self.querier.update({self.__softdelete__: None})

    def update(self, values: dict):
        if self.__softdelete__ is not None:
            self.querier.whereIsNull(self.__softdelete__)

        return self.querier.update(values)

    def insert(self, values: dict | list[dict]):
        return self.querier.insert(values)

    def withRelated(self, relateds: str | list[str]):

        def getRelated(d):
            method = getattr(self, d)
            method()

        if type(relateds) == str:
            getRelated(relateds)
            self.__has["related_name"] = relateds
        else:
            for i in relateds:
                getRelated(i)

        return self

    def hasMany(
        self,
        model: "Modelr",
        model_key: str,
        pivot_model_key: str,
        pivot_table: str,
        pivot_local_key: str,
        local_key: str,
    ):
        self.__has["related_type"] = "HasMany"

        self.__has["model"] = model
        self.__has["model_key"] = model_key
        self.__has["pivot_model_key"] = pivot_model_key
        self.__has["pivot_table"] = pivot_table
        self.__has["pivot_local_key"] = pivot_local_key
        self.__has["local_key"] = local_key

    def hasOne(self, model: "Modelr", model_key: str, local_key: str):
        self.__has["related_type"] = "HasOne"

        self.__has["model"] = model
        self.__has["model_key"] = model_key
        self.__has["local_key"] = local_key


#     # relashionship -----------------------------------------------------------

#     def has(self, model: str, model_key: str, intermediate_model_key: str = None, intermediate_table: str = None, intermediate_local_key: str = None, local_key: str = None, type: str = None):
#         table_local = self.__table__
#         table_model = model.__table__

#         for related in self.__has:
#             for a in related.values():
#                 check = len(a)
#                 if check == 0:
#                     key = list(related)[0]
#                     related[key] = {
#                         "type": type,
#                         "local_table": table_local,
#                         "local_key": local_key,
#                         "intermediate_table": intermediate_table,
#                         "model_table": table_model,
#                         "model_key": model_key,
#                         "intermediate_model_key": intermediate_model_key,
#                         "intermediate_table": intermediate_table,
#                         "intermediate_local_key": intermediate_local_key
#                     }

#     def hasOne(self, model, model_key, local_key):
#         self.has(
#             model=model,
#             model_key=model_key,
#             local_key=local_key,
#             type='one'
#         )

#     def hasMany(self, model, model_key, local_key):
#         self.has(
#             model=model,
#             model_key=model_key,
#             local_key=local_key,
#             type='many'
#         )

#     def hasManyToMany(self, model, model_key, intermediate_model_key, intermediate_table, intermediate_local_key, local_key):
#         self.has(
#             model=model,
#             model_key=model_key,
#             intermediate_model_key=intermediate_model_key,
#             intermediate_table=intermediate_table,
#             intermediate_local_key=intermediate_local_key,
#             local_key=local_key,
#             type='manytomany'
#         )
#         self.selected_related = model.__table__
#         return self

#     def withPivot(self, columns: list[str] | bool = True):

#         for related in self.__has:
#             for key in related.keys():
#                 if self.selected_related == key:
#                     related[key]['pivot'] = columns

#     def related(self, model: list | str):

#         def x(d):
#             method = getattr(self, d)
#             self.__has.append({method.__name__: {}})
#             method()

#         if type(model) == str:
#             x(model)
#         else:
#             for i in model:
#                 x(i)

#         return self

#     def check_relationships(self, data, first=False, onlySql=False):

#         data_json = data if type(data) == list else data
#         data_json = data_json if type(data_json) == list else [data_json]

#         for dictr in self.__has:
#             for rel, value in dictr.items():
#                 if value['type'] in ['many', 'one']:
#                     data_json = self.check_relationships_one_many(
#                         rel, value, data_json, onlySql)

#                 elif value['type'] in ['manytomany']:
#                     data_json = self.check_relationships_manytomany(
#                         rel, value, data_json, onlySql)

#         if onlySql == False:
#             return data_json[0] if first == True else data_json

#     def check_relationships_one_many(self, rel, value, data_json, onlySql):

#         all = True if value['type'] == 'many' else False

#         keys = list(set(row[value['local_key']] for row in data_json))

#         query_related = Querier(self.__conn__).table(
#             value['model_table']).whereIn(value['model_key'], keys)
#         self.__queries.append(
#             {"query": query_related.toSql(), "params": query_related.toParams()})

#         if onlySql == False:
#             data_rel = query_related.get()
#             if all:
#                 for row in data_json:
#                     row[rel] = None
#                     for relrow in data_rel:
#                         if row[value['local_key']] == relrow[value['model_key']]:
#                             if row[rel] == None:
#                                 row[rel] = []
#                             row[rel].append(relrow)

#             else:
#                 for row in data_json:
#                     for relrow in data_rel:
#                         if row[value['local_key']] == relrow[value['model_key']]:
#                             if rel not in row.keys():
#                                 row[rel] = relrow
#                             else:
#                                 row[rel] == None

#         return data_json

#     def check_relationships_manytomany(self, rel, value, data_json, onlySql):
#         local_keys = list(set(row[value['local_key']] for row in data_json))

#         # acessar intermediaria
#         query_intermediated = Querier(self.__conn__).table(
#             value['intermediate_table']).whereIn(value['intermediate_local_key'], local_keys)
#         self.__queries.append(
#             {"query": query_intermediated.toSql(), "params": query_intermediated.toParams()})

#         # resgatar ids do modelo relacionado
#         data_intermediate_json = query_intermediated.get()
#         # data_intermediate_json = json.loads(data_intermediate_json)
#         data_intermediate_json = data_intermediate_json if type(
#             data_intermediate_json) == list else [data_intermediate_json]
#         intemediate_model_keys = list(
#             set(row[value['intermediate_model_key']] for row in data_intermediate_json))

#         if intemediate_model_keys != []:
#             # acessar table do model
#             query_model = Querier(self.__conn__).table(value['model_table']).whereIn(
#                 value['model_key'], intemediate_model_keys)
#             self.__queries.append(
#                 {"query": query_model.toSql(), "params": query_model.toParams()})
#             data_rel = query_model.get()
#         else:
#             data_rel = []

#         # mesclando relacionamentos
#         # data_rel = json.loads(query_model.get())
#         local_counter = 0
#         for local_row in data_json:
#             local_counter += 1

#             if rel not in local_row:
#                 local_row[rel] = None

#             inter_counter = 0
#             for interdata_row in data_intermediate_json:
#                 inter_counter += 1

#                 # if rel not in local_row:
#                 #     local_row[rel] = None

#                 model_counter = 0
#                 for model_row in data_rel:
#                     model_counter += 1

#                     if local_row[value['local_key']] == interdata_row[value['intermediate_local_key']] and\
#                        model_row[value['model_key']] == interdata_row[value['intermediate_model_key']]:

#                         if "pivot" in value:
#                             if type(value['pivot']) == list:
#                                 model_row['pivot'] = {col: interdata_row[col] for col in interdata_row if col in value['pivot']
#                                                       and interdata_row[value['intermediate_model_key']] == model_row[value['model_key']]}
#                             else:
#                                 model_row['pivot'] = interdata_row

#                         if local_row[rel] == None:
#                             local_row[rel] = []

#                         local_row[rel].append(model_row)

#         return data_json
