import sqlalchemy
import inspect
print(dir(sqlalchemy.sql.sqltypes.Uuid))
print('\nsource:\n')
print(inspect.getsource(sqlalchemy.sql.sqltypes.Uuid))
