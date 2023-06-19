from src.opensearch.dao import OpensearchDao
from src.util import ResponseModel


class SearchServices:

    @staticmethod
    async def search(conditions_with_or_operator: [str], conditions_with_and_operator: [str]) -> ResponseModel:
        search_results = OpensearchDao.search_with_params(conditions_with_or_operator, conditions_with_and_operator)
        if search_results.error:
            return search_results

        return search_results
