from database import database
import asyncpg

from database.sql import SQL
from resources.starboard import Starboard


class StarboardService:

    @classmethod
    async def get(cls, message_or_star_id, guild_id):
        fetched = await database.connection.fetchrow('''
            select *
            from starboard
            where (message_id = $1 or id = $1) and guild_id = $2;
        ''', int(message_or_star_id), guild_id)

        return Starboard.convert(fetched) if fetched is not None else None

    @classmethod
    async def star(cls, reaction):
        message = reaction.message
        should_send = False
        try:
            should_send = True

            try:
                attachment = message.attachments[0].url
            except IndexError:
                attachment = None

            starred = await database.connection.fetchrow('''
                insert into Starboard (message_id, channel_id, guild_id, message_content, attachment, stars_count)
                values ($1, $2, $3, $4, $5, $6)
                returning *;
            ''', message.id, message.channel.id, message.guild.id, message.content if message.content != '' else None,
                                                         attachment, reaction.count)
        except asyncpg.exceptions.UniqueViolationError:
            starred = await database.connection.fetchrow('''
                update starboard
                set stars_count = $4
                where message_id = $1 and channel_id = $2 and guild_id = $3
                returning *;
            ''', message.id, message.channel.id, message.guild.id, reaction.count)

        return should_send, Starboard.convert(starred)

    @classmethod
    async def unstar(cls, reaction):
        message = reaction.message
        unstarred = await database.connection.fetchrow('''
                update starboard
                set stars_count = starboard.stars_count - 1
                where message_id = $1 and channel_id = $2 and guild_id = $3
                returning *;
            ''', message.id, message.channel.id, message.guild.id)

        if unstarred['stars_count'] == 0:
            unstarred = await database.connection.fetchrow('''
                delete from starboard
                where message_id = $1 and channel_id = $2 and guild_id = $3
                returning *;
            ''', message.id, message.channel.id, message.guild.id)

        return Starboard.convert(unstarred)

    @classmethod
    def sql(cls):
        return SQL(createTable='''
            create table if not exists Starboard
            (
                id              serial primary key,
                message_id      bigint    not null,
                guild_id        bigint    not null,
                channel_id      bigint    not null,
                started_at      timestamp not null default now(),
                message_content text,
                attachment      text,
                stars_count     int       not null
            );
            
            create unique index if not exists unique_message on Starboard (message_id);
            ''')
