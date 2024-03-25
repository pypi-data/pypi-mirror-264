from sqlalchemy import Engine, Select


class QueryUtils:

    @staticmethod
    def get_sql(engine: Engine, select: Select) -> str:
        return str(
            select.compile(
                dialect=engine.dialect, compile_kwargs={"literal_binds": True}
            )
        )
