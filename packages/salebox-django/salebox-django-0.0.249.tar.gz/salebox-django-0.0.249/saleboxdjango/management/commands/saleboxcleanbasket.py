from django.core.management.base import BaseCommand, CommandError
from rawquery import RawQuery

# run this command immediately AFTER running django's clearsessions


class Command(BaseCommand):
    def handle(self, *args, **options):
        rq = RawQuery()
        MAX_SESSIONS = 5000
        total_sessions_deleted = 0

        while True:
            oldest_sessions = rq.multiple_values(
                f"""
                SELECT      session
                FROM        saleboxdjango_basketwishlist
                WHERE       user_id IS NULL
                GROUP BY    session
                ORDER BY    MIN(last_update)
                LIMIT       {MAX_SESSIONS}
                """
            )

            active_sessions = rq.multiple_values(
                f"""
                SELECT      session_key
                FROM        django_session
                WHERE       session_key IN ({self.make_sql_list(oldest_sessions)})
                """
            )

            sessions_to_delete = [
                s for s in oldest_sessions if s not in active_sessions
            ]

            if len(sessions_to_delete) > 0:
                total_sessions_deleted += len(sessions_to_delete)
                rq.run(
                    f"""
                    DELETE FROM     saleboxdjango_basketwishlist
                    WHERE           user_id IS NULL
                    AND             session IN ({self.make_sql_list(sessions_to_delete)})
                    """
                )
            else:
                break

        print(f"Total sessions deleted: {total_sessions_deleted}")

    def make_sql_list(self, id_list):
        return ",".join(["'" + s + "'" for s in id_list])
