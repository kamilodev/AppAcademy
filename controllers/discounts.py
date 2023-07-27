from data.connection import database as database
from fastapi import status, Response
from data.Models import DeleteDiscount, Discount


async def get_discount_by_id(id_discounts: int):
    query = f"SELECT * FROM discounts WHERE id_discounts = :id_discounts"
    values = {"id_discounts": id_discounts}
    results = await database.fetch_all(query, values)
    return results


async def get_discount(id_discounts: int, response: Response):
    """
    This endpoint allows you to get a discount by id.

    - **id**: id of the discount (mandatory)
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
    This endpoint allows you to create a new discount in the database.

    - **id**: id of the discount (mandatory)
    - **discounts**: Percentage of the discount (mandatory)
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
    This endpoint allows you to update the information of a discount in the database.

    - **id**: id of the discount (mandatory)
    - **discounts**: Percentage of the discount (mandatory)

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
    This endpoint allows you to delete a discount by id.

    - **id**: id of the discount (mandatory)
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