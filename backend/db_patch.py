from django.db.backends.mysql.features import DatabaseFeatures


original_version_property = DatabaseFeatures.minimum_database_version

@property
def patched_minimum_database_version(self):
    if self.connection.mysql_is_mariadb:
        return (10, 4)  
    

DatabaseFeatures.minimum_database_version = patched_minimum_database_version


original_returning_property = DatabaseFeatures.can_return_columns_from_insert

@property 
def patched_can_return_columns_from_insert(self):
    return False

DatabaseFeatures.can_return_columns_from_insert = patched_can_return_columns_from_insert