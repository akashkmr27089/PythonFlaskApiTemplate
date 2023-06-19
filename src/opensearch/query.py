def query_generator(conditions_with_or_operator: [str], conditions_with_and_operator: [str], field: str):
    # Sample "(text_data:*compos* OR text_data:*INSULATION*) OR (text_data:*However* AND text_data:*chopping*)"
    final_string, final_str_or, final_str_and = "", "", ""
    if len(conditions_with_or_operator) != 0:
        final_str_or = " OR ".join(["{}:*{}*".format(field, x) for x in conditions_with_or_operator])
    if len(conditions_with_and_operator) != 0:
        final_str_and = " AND ".join(["{}:*{}*".format(field, x) for x in conditions_with_and_operator])

    if final_str_or != "" or final_str_and != "":
        if final_str_or != "" and final_str_and != "":
            return "({}) OR ({})".format(final_str_or, final_str_and)
        else:
            if final_str_or == "":
                return final_str_and
            else:
                return final_str_or

    # In case there is no string passed, then the query will return query
    # to return all string
    return "*"
