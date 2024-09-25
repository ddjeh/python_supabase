from postgrest.types import CountMethod

from supabase_service.config import SupabaseClient
from supabase_service.types import GenericResponse
from supabase_service.utils import join_strings


class SupabaseDatabase(SupabaseClient):

    def __init__(self):
        super().__init__()
        self.__client_database = self._get_client

    def select_all(self, table_name: str, table_columns: list = ['*'], count: CountMethod = CountMethod["exact"],
                   where: dict = None) -> GenericResponse:
        """
        :param table_name: str
        :param table_columns: str
        :param count: CountMethod = CountMethod["exact"]
        :param where: dict
        :return: GenericResponse
        """
        if not table_name or not table_name.strip():
            return GenericResponse(status=400, message="Table name is required")

        if not table_columns or not table_columns:
            return GenericResponse(status=400, message="Table columns are required")

        try:
            query = (self.__client_database.from_(table_name)
                     .select(join_strings(strings=table_columns),
                             count=count))

            if where:
                for k, v in where.items():
                    query = query.eq(k, v)

            response = query.execute()

            return GenericResponse(status=200, message="Select successful", data=response.data, count=response.count)
        except Exception as e:
            return GenericResponse(status=500, message=str(e))

    def select_by_id(self, table_name: str, table_columns: list = ['*'], id: int = None) -> GenericResponse:
        """
        :param table_name: str
        :param table_columns: list
        :param id: int
        :return: GenericResponse
        """
        if not id:
            return GenericResponse(status=400, message="ID is required")

        return self.select_all(table_name=table_name, table_columns=table_columns, count=CountMethod["none"],
                               where={"id": id})

    def update(self, table_name: str, set: dict[str, str], where: dict) -> GenericResponse:
        """
        :param table_name: str
        :param set: dict
        :param where: dict
        :return: GenericResponse
        """
        if not table_name or not table_name.strip():
            return GenericResponse(status=400, message="Table name is required")

        if not set or not set:
            return GenericResponse(status=400, message="Set is required")

        if not where or not where:
            return GenericResponse(status=400, message="Where is required")

        try:
            query = (self.__client_database.from_(table_name)
                     .update(json=set))

            if where:
                for k, v in where.items():
                    query = query.eq(k, v)

            response = query.execute()

            return GenericResponse(status=200, message="Update successful", data=response)
        except Exception as e:
            return GenericResponse(status=500, message=str(e))

    def insert(self, table_name: str, values: dict) -> GenericResponse:
        """
        :param table_name: str
        :param values: dict
        :return: GenericResponse
        """
        if not table_name or not table_name.strip():
            return GenericResponse(status=400, message="Table name is required")

        if not values or not values:
            return GenericResponse(status=400, message="Values are required")

        try:
            query = (self.__client_database.from_(table_name)
                     .insert(json=values))

            response = query.execute()

            return GenericResponse(status=201, message="Insert successful", data=response)
        except Exception as e:
            return GenericResponse(status=500, message=str(e))

    def delete(self, table_name: str, where: dict) -> GenericResponse:
        """
        :param table_name: str
        :param where: dict
        :return: GenericResponse
        """
        if not table_name or not table_name.strip():
            return GenericResponse(status=400, message="Table name is required")

        if not where or not where:
            return GenericResponse(status=400, message="Where is required")

        try:
            query = (self.__client_database.from_(table_name)
                     .delete())

            if where:
                for k, v in where.items():
                    query = query.eq(k, v)

            response = query.execute()

            return GenericResponse(status=200, message="Delete successful", data=response)
        except Exception as e:
            return GenericResponse(status=500, message=str(e))
