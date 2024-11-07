# Features:
  - User management:
    - User can login
    - User can register
    - User can update their profile informations
  - Room management:
    - User can view all rooms
    - User can view a room details
      - Room features
    - User can create/update/delete a room
  - Customer management:
    - User can view all customers
    - User can view a customer details
      - Can check if they have any current reservation
        - Reservation details (when they booked it, the room number & for how many days)
    - User can create/update/delete a customer
  - Reservation management:
    - User can view all rooms (filters: reserve, bed count [how many person can stay in that room. e.g. 1 - 4])
      - Deafult view: rooms that are available for reservation
      - Filter view: rooms that are reserved
    - User can view a room details
      - Room features
  - Billing System:
    - User can view all bills & bill details
    - User can update/modify the bill
    - User can create a bill by selecting an customer. Note: need brainstorming


# How to make this project better
  - Make it responsive
  - Add forget password feature








rewrite view/dashboard_view.py. build a clean, modern-looking dashboard with an default homepage. the homepage will show a welcome message. background will be secondary & all text will be primary.
In the dashboard, you'll have a header & a sidebar.

In the header, left end will be project title (get it from config.py in the root folder), right end will have a profile icon. header background color will be primary, text will have secondary color. give a border after header of secondary color.
when we click on the title it'll return to the dashboard homepage. and by clicking the profile icon a dropdown will show where we'll have two options: profile & logout

In the sidebar we'll have few options named: Rooms, Customers, Reservations & Billing. sidebar background color will be primary, text will have secondary color
give an hover border in each option. add a little divider between the options. the divider color will be secondary color.

each page for the options will have separate files in view folder. all pages background will be secondary & all text will be primary.

