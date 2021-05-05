from sqlalchemy import func
from db.models import MaxBotDB, Member, Sound

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
            member = self.database.query_by_filter(session, Member, expr, limit=1)[0]

        except IndexError:
            raise Exception('Member not found')

        return member

    def find_items_by_name(self, session, name, item_type, exact_match=False, sort=None, limit=10):
        if not exact_match:
            expr = item_type.name.ilike(f'%{name}%')
        else:
            expr = item_type.name == name
        return self.database.query_by_filter(session, item_type, expr, sort=sort, limit=limit)

    def find_items_by_member(self, session, member_id, item_type, sort=None, limit=10):
        expr = item_type.member_id == member_id
        return self.database.query_by_filter(session, item_type, expr, sort=sort, limit=limit)

    def find_item_by_id(self, session, id, item_type):
        # TODO: Finish this
        return None

    def find_sound_by_command(self, session, command):
        expr = Sound.command == command
        return self.database.query_by_filter(session, Sound, expr, sort=None, limit=1)

    def delete_item_by_id(self, session, id, item_type):
        expr = item_type.id == id
        return self.database.delete_entry(session,item_type,expr)