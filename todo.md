# Room Page
    -> Edit & delete button should have pointer cursor


# Profile Page
    -> Change the input fields & button (follow room_view)
    -> Get the user data & show them in the fields
    -> Make sure the user data is updating properly


# Auth
    -> Logged in user data should be stored. Use the user name in the dashboard header


# Sign In Page
    -> Email should be valid (accept all type of valid mail [Check digiprodpass codebase])
    -> If the email doesn't found or the password doesn't match, an error message should be shown: "Email and password doesn't match"


# Sign UP Page
    -> email should be valid (accept all type of valid mail [Check digiprodpass codebase])


# Customers Page
    -> email should be valid (accept all type of valid mail [Check digiprodpass codebase])










# prompt



You'll generate the reservation module now (view, controller & model). The design will be exactly the same as the customer module. add edit functionality & skip delete functionality for this module.

Id: primaryKey (auto generated) 
roomId: foreign key 
customerId: foreign key 
checkIn: string [format validation: dd/mm/yyyy] 
checkOut: string [format validation: dd/mm/yyyy] 
status: string [one of these 3 options: Confirmed, Cancelled, Pending]
totalAmount: int [add valid integer validation] 
createdBy: userId


follow the table design from customer module
the form design will be following:
room: dropdown where all the roomId will be shown. when clicked on the roomId in the payload the Id (primary key) will be saved.
customer: dropdown where all the customer name will be shown. when clicked on the name in the payload the Id (primary key) will be saved.
checkIn: input field. add validation so that the string should be in dd/mm/yyyy format
checkOut: input field. add validation so that the string should be in dd/mm/yyyy format
status: radio. one of these 3 options can be selected; Confirmed, Cancelled, Pending. by default Confirmed will be selected.
totalAmount: input field. add valid integer validation.