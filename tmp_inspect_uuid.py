from app.models.auths.user import User
print('column type:', User.__table__.c.id.type, type(User.__table__.c.id.type))
import sqlalchemy
print('sqlalchemy.uuid class:', getattr(sqlalchemy.sql.sqltypes, 'UUID', None))
