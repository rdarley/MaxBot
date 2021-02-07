from sqlalchemy import func
from db.models import MaxBotDB, Member

class MaxBotDBInterface():
    def __init__(self, **kwargs):
        self.database = MaxBotDB()

    def find_member(self, session, member_id=None, member_name=None):
        if member_id:
            expr = Member.id == member_id
        elif member_name:
            expr = Member.name == member_name
        else:
            raise Exception('Member ID or Name Required')

        try:
            member = self.database.query_by_filter(session, Member, expr)[0]

        except IndexError:
            raise Exception('Member not found')

        return member