from resources import Resource


class Activity(Resource):
    def __init__(self, **kwargs):
        self.guild = kwargs.pop('guild')
        self.user = kwargs.pop('user')
        self.points = kwargs.pop('points')
        self.last_updated_time = kwargs.pop('last_updated_time')
        self.position = kwargs.pop('position')

    @classmethod
    def convert(cls, record):
        return cls(
            points=record['points'],
            user=record['user_id'],
            guild=record['guild_id'],
            last_updated_time=record['last_time_updated'],
            position=record['position']
        )

    @classmethod
    def convertMany(cls, records):
        return [cls.convert(activity) for activity in records]
