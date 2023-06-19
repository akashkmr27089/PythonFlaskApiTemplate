from src.integrations.metaphorpsum import Metaphorsum
from src.opensearch.dao import OpensearchDao
from src.util import ResponseModel


class GetServices:

    @staticmethod
    def generate_tokens(paragraph):
        return [x for x in paragraph.split(" ")]

    @staticmethod
    async def get_new_paragraph(nos_of_paragraph, nos_of_sentence) -> ResponseModel:
        out = ResponseModel()

        para_response = await Metaphorsum.get_paragraph(nos_of_paragraph, nos_of_sentence)
        if para_response.error:
            return para_response

        # Save the Data Onto Opensearch
        paragraph_data = para_response.data
        token_data = GetServices.generate_tokens(paragraph_data)

        if_entry_created = OpensearchDao.create(paragraph_data, token_data)
        if not if_entry_created:
            out.error = True
            out.message = "Object not created in Opensearch"
            return out

        out.data = paragraph_data
        return out
