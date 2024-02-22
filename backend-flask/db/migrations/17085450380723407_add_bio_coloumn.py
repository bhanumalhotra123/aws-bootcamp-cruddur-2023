from lib.db import db

class AddBioColoumnMigration:
  def migrate_sql():
    # Placeholder for SQL statements to migrate the database
    data = """
    ALTER TABLE public.users ADD COLUMN bio text;
    """
    return data

  def rollback_sql():
    # Placeholder for SQL statements to rollback changes in the database
    data = """
    ALTER TABLE public.users DROP COLUMN bio;
    """
    return data

  def migrate():
    # Executes the SQL migration queries
    db.query_commit(AddBioColoumnMigration.migrate_sql(),{
    })

  def rollback():
    # Executes the SQL rollback queries
    db.query_commit(AddBioColoumnMigration.rollback_sql(),{
    })

migration = AddBioColoumnMigration