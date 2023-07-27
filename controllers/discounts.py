from data.connection import database as database
from fastapi import status, Response
from data.Models import DeleteDiscount, Discount


async def get_discount_by_id(id_discounts: int):
    """
    The function `get_discount_by_id` retrieves discount information from a database based on the
    provided discount ID.

    :param id_discounts: The parameter `id_discounts` is an integer that represents the ID of the
    discount you want to retrieve from the database
    :type id_discounts: int
    :return: the results of a database query for a discount with a specific ID.
    """
    query = f"SELECT * FROM discounts WHERE id_discounts = :id_discounts"
    values = {"id_discounts": id_discounts}
    results = await database.fetch_all(query, values)
    return results


async def get_discount(id_discounts: int, response: Response):
    """
    The function `get_discount` retrieves a discount by its ID and returns a response with the discount
    data or a not found message.

    :param id_discounts: The `id_discounts` parameter is an integer that represents the ID of the
    discount you want to retrieve
    :type id_discounts: int
    :param response: The `response` parameter is an instance of the `Response` class. It is used to set
    the status code of the HTTP response and return the response data
    :type response: Response
    :return: either a string or a dictionary, depending on the condition. If the length of the results
    is 0, it returns a string indicating that the discount with the given id was not found. If the
    length of the results is not 0, it returns a dictionary with a message indicating that the discount
    was found and the data of the first result.
    """
    results = await get_discount_by_id(id_discounts)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Discount with id: {id_discounts} not found"
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": "Discount found", "data": results[0]}


async def get_all_discounts():
    """
    This endpoint allows you to get all discounts in the database.
    """
    query = "SELECT * FROM discounts ORDER BY id_discounts ASC"
    results = await database.fetch_all(query)
    return {"message": "All discounts", "data": results}


async def create_discount(discount: Discount, response: Response):
    """
    The function `create_discount` creates a new discount in a database table, checking for empty fields
    and duplicate discounts.

    :param discount: The `discount` parameter is an instance of the `Discount` class, which contains the
    data for creating a discount. It has two attributes: `id_discounts` and `discounts`
    :type discount: Discount
    :param response: The `response` parameter is an instance of the `Response` class. It is used to set
    the HTTP status code and return error messages if necessary
    :type response: Response
    :return: either a string message or a dictionary object. If there is an error or validation failure,
    a string message is returned. If the discount is created successfully, a dictionary object with the
    message "Discount created successfully" is returned.
    """
    default_values = ["string", "", 0]

    for field in discount.__fields__:
        if discount.__getattribute__(field) in default_values:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Field {field} cannot be empty"

    query = f"INSERT INTO discounts (id_discounts, discounts) VALUES (:id_discounts, :discounts)"
    values = {
        "id_discounts": discount.id_discounts,
        "discounts": discount.discounts,
    }
    duplicate_user = await get_discount_by_id(discount.id_discounts)
    if len(duplicate_user) > 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Discount with id: {discount.id_discounts} already exists"

    await database.execute(query=query, values=values)

    return {"message": "Discount created successfully"}


async def update_discount(discount: Discount, response: Response):
    """
    The function `update_discount` updates a discount in a database based on the provided discount
    object and returns a success message.

    :param discount: The `discount` parameter is an instance of the `Discount` class, which represents a
    discount object. It contains various fields that can be updated, such as `id_discounts` (the
    discount ID) and other fields specific to the discount
    :type discount: Discount
    :param response: The `response` parameter is an instance of the `Response` class. It is used to set
    the status code of the HTTP response
    :type response: Response
    :return: a string message indicating the result of the update operation. The message can be one of
    the following:
    """
    results = await get_discount_by_id(discount.id_discounts)

    if discount.id_discounts == "":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Discount id cannot be empty"

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Discount with id: {discount.id_discounts} not found"

    update_fields = {}

    default_values = [0]

    for field in discount.__fields__:
        if field == "id_discounts":
            continue
        if discount.__getattribute__(field) in default_values:
            continue

        update_fields[field] = discount.__getattribute__(field)

    if len(update_fields) == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"No fields to update for discount with id: {discount.id_discounts}"

    set_query = ", ".join(f"{field} = :{field}" for field in update_fields)
    values = {"id_discounts": discount.id_discounts, **update_fields}

    query = f"UPDATE discounts SET {set_query} WHERE id_discounts = :id_discounts"
    await database.execute(query=query, values=values)

    return f"Discount with id {discount.id_discounts} updated successfully"


async def delete_discount(discount: DeleteDiscount, response: Response):
    """
    The `delete_discount` function deletes a discount from a database based on its ID.

    :param discount: The `discount` parameter is an instance of the `DeleteDiscount` class. It contains
    the information needed to identify the discount that needs to be deleted. The `DeleteDiscount` class
    likely has a property called `id_discounts` which represents the ID of the discount to be deleted
    :type discount: DeleteDiscount
    :param response: The `response` parameter is an instance of the `Response` class, which is used to
    send HTTP responses. It allows you to set the status code and return a response message
    :type response: Response
    :return: a string message indicating the result of the delete operation. The possible return
    messages are:
    - "Discount id cannot be empty" if the discount id is empty or a string.
    - "Discount with id: {discount.id_discounts} not found" if no discount with the given id is found in
    the database.
    - "Discount with id {discount.id_discounts} deleted"
    """
    results = await get_discount_by_id(discount.id_discounts)

    if discount.id_discounts == "" or discount.id_discounts == "string":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Discount id cannot be empty"

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Discount with id: {discount.id_discounts} not found"

    delete_query = f"DELETE FROM discounts WHERE id_discounts = :id_discounts"
    values = {"id_discounts": discount.id_discounts}

    await database.execute(delete_query, values)
    response.status_code = status.HTTP_200_OK
    return f"Discount with id {discount.id_discounts} deleted"
