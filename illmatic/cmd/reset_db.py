import pecan
from pecan import conf
from illmatic.model import Base
import illmatic.model.models

class GetCommand(pecan.commands.BaseCommand):
    """
    Drop and recreate all database tables
    """

    def run(self, args):
        super(GetCommand, self).run(args)
        self.load_app()
        Base.metadata.drop_all(bind=conf.sqlalchemy.engine)
        Base.metadata.create_all(bind=conf.sqlalchemy.engine)
