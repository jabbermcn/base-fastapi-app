from src.database.abc_uow import UnitOfWork


class AlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_maker):
        self.session_maker = session_maker

    async def __aenter__(self):
        async with self.session_maker() as session:
            self.session = session
            return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
