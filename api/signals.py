from django.db.backends.signals import connection_created
from django.dispatch import receiver
from django.db import connection

@receiver(connection_created)
def drop_tables_on_startup(sender,signal, **kwargs):
    if(signal.disconnect(dispatch_uid="drop_tables_on_startup")):
        tables_to_drop = ['db_gameroom', 'db_gamemember', 'db_bingo']
        print("Droping tables: ",tables_to_drop)
        with connection.cursor() as cursor:
            for collection in tables_to_drop:
                try:
                    cursor.db.connection[collection].drop()
                except Exception as e:
                    print(e)
    

connection_created.connect(drop_tables_on_startup,dispatch_uid="drop_tables_on_startup")
