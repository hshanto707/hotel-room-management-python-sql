# Sign In Page
    -> Email should be valid (accept all type of valid mail [Check digiprodpass codebase])
    -> If the email doesn't found or the password doesn't match, an error message should be shown: "Email and password doesn't match"


# Sign UP Page
    -> email should be valid (accept all type of valid mail [Check digiprodpass codebase])


# Customers Page
    -> email should be valid (accept all type of valid mail [Check digiprodpass codebase])





# prompt



You'll generate the billing module now (view, controller & model files). The design will be exactly the same as the reservation module. add edit functionality & skip delete functionality for this module.

Id: primaryKey (auto generated) 
reservationId: foreign key 
amount: int [add valid integer validation] 
discount: int [add valid integer validation] 
paymentDate: string [format validation: dd/mm/yyyy]
status: string [one of these 3 options: Confirmed, Cancelled, Pending]
createdBy: userId


follow the table design from reservation module
the form design will be following:
reservation: dropdown where all the reservations will be shown. when clicked on the reservation, in the payload the reservationId (primary key) will be saved.
amount: input field. add valid integer validation.
discount: input field. add valid integer validation.
paymentDate: input field. add validation so that the string should be in dd/mm/yyyy format
status: radio. one of these 3 options can be selected; Confirmed, Cancelled, Pending. by default Confirmed will be selected.

functionality flow:
when user select an reservation, it should hit a function which will get the amount & set it as "amount" in the payload. since we have the reservation id, we have the "totalAmount" in the reservation object. this will be "amount" in the payments table.