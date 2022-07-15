import pymysql

class database:
    def __init__(self,host,user,password,schema):
        self.connection = pymysql.connect(host=host,
                        user=user,
                        password=password,
                        database=schema)
        self.cursor = self.connection.cursor()

class table(database):
    def __init__(self,host,user,password,schema,table):
        database.__init__(self,host,user,password,schema)
        self.table = table

    def __makeQuote(self,string):
        return '"' + string + '"'

    def __makeInsert(self, valDict):
        sql = 'INSERT INTO ' + self.table
        field = ' ('
        value = 'VALUES ('
        for key in valDict:
            if valDict[key] != "":
                field += str(key) + ','
                if type(valDict[key]) == str:
                    value += self.__makeQuote(str(valDict[key]))+ ','
                else:
                    value += str(valDict[key])+ ','
        field = field[:-1] + ") "
        value = value[:-1] + ")"
        sql += field + value
        return sql

    def __makeDelete(self,condition):
        return 'DELETE FROM ' + self.table + ' WHERE ' + condition

    def __makeUpdate(self,valDict,condition):
        sql = 'UPDATE ' + self.table + ' SET '
        for key in valDict:
            if type(valDict[key]) == str:
                val = self.__makeQuote(valDict[key])
            else:
                val = valDict[key]
            sql += key + '=' + str(val) + ','
        return sql[:-1] + ' WHERE ' + condition

    def __makeSelect(self,fields,condition):
        sql = 'SELECT '
        for field in fields:
            sql += field + ', '
        sql = sql[:-2] + ' FROM ' + self.table
        if condition == "":
            return sql 
        else:
            return sql + ' WHERE ' + condition

    def __executeSqlAndCommit(self,sql):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            return 0
        except:
            self.connection.rollback()
            return -1

    def insert(self,valDict):
        sql = self.__makeInsert(valDict)
        return self.__executeSqlAndCommit(sql)

    def delete(self,condition):
        sql = self.__makeDelete(condition)
        return self.__executeSqlAndCommit(sql)

    def update(self,valDict,condition):
        sql = self.__makeUpdate(valDict,condition)
        return self.__executeSqlAndCommit(sql)

    def select(self,fields,condition):
        sql = self.__makeSelect(fields,condition)
        self.cursor.execute(sql)
        return self.cursor.fetchall()


# t1 = table('localhost','root','root','mydatabase','student') # student table

# res = t1.select('*','')

# print(res)