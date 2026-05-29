from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DWMySQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_column_types(self, table_name) -> dict[str, str]:
        sql = f"show columns from {table_name}"
        result = await self.session.execute(text(sql))
        result_dict = result.mappings().fetchall()
        result_now = {row["Field"]: row["Type"] for row in result_dict}

        return result_now


    async def get_column_values(self, table_name, column_name, limit=100) -> list[str]:
        sql = f"select distinct {column_name} from {table_name} limit {limit}"
        result = await self.session.execute(text(sql))
        result = result.fetchall()
        result_now = [row[0] for row in result]

        return result_now

    async def get_db_info(self):
        sql = "select version()"
        result = await self.session.execute(text(sql))
        version = result.scalar()
        dialect = self.session.bind.dialect.name

        return {"dialect": dialect, "version": version}

    async def validate_sql(self, sql: str):
        sql = f"explain {sql}"
        await self.session.execute(text(sql))

    async def run(self, sql: str) -> list[dict]:
        result = await self.session.execute(text(sql))
        result = [dict(row) for row in result.mappings().fetchall()]

        return result