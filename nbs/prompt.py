def generate_prompt(description):
    datasets_description = """
        1. toyota_staff_details:
        - staff_id: A unique identifier for each staff member.
        - staff_name: The name of the staff member.
        - position: The staff member's position within the company.
        - department: The department the staff member works in.
        - start_date: The date when the staff member started their employment.
        - email: The staff member's email address.

        2. toyota_car_models:
        - model_id: A unique identifier for each car model.
        - model_name: The name of the car model.
        - manufacturing_year: The year the car model was manufactured.
        - type: The type of car (e.g., Sedan, SUV).
        - market: The market where the car model is available (e.g., Thailand).

        3. toyota_spare_parts:
        - part_id: A unique identifier for each spare part.
        - model_id: The identifier of the car model the part is used for.
        - serial_number: The serial number of the spare part.
        - part_name: The name of the spare part.
        - part_type: The type of spare part (OEM or Aftermarket).
        - stock_quantity: The quantity of the part available in stock.
        - price: The price of the spare part.

        4. toyota_sales_records:
        - sale_id: A unique identifier for each sale.
        - model_id: The identifier of the car model sold.
        - staff_id: The identifier of the salesperson who made the sale.
        - sale_date: The date of the sale.
        - sale_price: The price at which the car was sold.
        - customer_name: The name of the customer who bought the car.
        - payment_method: The method used for payment (e.g., Cash, Credit Card, Bank Transfer).

        5. toyota_service_records:
        - service_id: A unique identifier for each service provided.
        - car_serial_number: The serial number of the car serviced.
        - model_id: The identifier of the car model serviced.
        - staff_id: The identifier of the technician who provided the service.
        - service_date: The date the service was provided.
        - service_type: The type of service performed (e.g., Routine Maintenance, Repair).
        - cost: The cost of the service.

        6. toyota_customer_feedback:
        - feedback_id: A unique identifier for each piece of feedback.
        - customer_name: The name of the customer providing feedback.
        - model_id: The identifier of the car model the feedback is about.
        - feedback_date: The date the feedback was provided.
        - rating: The rating given by the customer.
        - comments: Any comments provided by the customer.

        7. toyota_dealerships_showrooms:
        - dealership_id: A unique identifier for each dealership or showroom.
        - name: The name of the dealership or showroom.
        - location: The location of the dealership or showroom.
        - contact_number: The contact number for the dealership or showroom.
        - email: The email address for the dealership or showroom.
        - manager_id: The identifier of the manager of the dealership or showroom.

        8. toyota_supply_chain_data:
        - supplier_id: A unique identifier for each supplier.
        - part_id: The identifier of the spare part supplied.
        - supplier_name: The name of the supplier.
        - location: The location of the supplier.
        - delivery_times: The delivery times for the supplier.
        - contact_info: Contact information for the supplier.

        9. toyota_inventory_records:
        - inventory_id: A unique identifier for each inventory record.
        - part_id: The identifier of the part in inventory.
        - current_stock: The current stock level of the part.
        - minimum_stock_level: The minimum stock level before reordering is necessary.
        - warehouse_location: The location of the warehouse holding the part.

        10. toyota_manufacturing_schedule:
            - schedule_id: A unique identifier for each manufacturing schedule.
            - model_id: The identifier of the car model being manufactured.
            - start_date: The start date of the manufacturing process.
            - end_date: The end date of the manufacturing process.
            - quantity: The quantity of cars to be produced.
            - status: The current status of the manufacturing process (e.g., Planned, In Progress, Completed).
    Based on this information, translate the following user request into an SQL query:

    """

    prompt_message = [
        {"role": "system", "content": datasets_description + description}
    ]

    return prompt_message