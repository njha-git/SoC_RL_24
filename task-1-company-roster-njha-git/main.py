"""
This is where the actual working of the program will happen!
We'll be Querying stuff for testing whether your classes were defined correctly

Whenever something inappropriate happens (like a function returning false in people.py),
raise a Value Error.
"""
from people import * # import everything!

if __name__ == "__main__":  # Equivalent to int main() {} in C++.
    last_input = 99
    while last_input != 0:
        last_input = int(input("Please enter a query number:"))

        if last_input == 1:
            name = input("Name:")
            age = input("age:")
            ID = input("ID:")
            city = input("City:")
            branchcodes = input("Branch(es):")
            position = input("Position:")
            # How will you conver this to a list, given that
            # the user will always enter a comma separated list of branch codes?
            # eg>   2,5
            branchcodes = branchcodes.split(",")
            branchcodes = [int(i) for i in branchcodes]

            salary = input("Salary: ")
            # Create a new Engineer with given details.
            engineer = Engineer(name, age, ID, city, branchcodes, position) # Change this

            engineer_roster.append(engineer) # Add him to the list! See people.py for definiton
            
        
        elif last_input == 2:
            # Gather input to create a Salesperson
            # Then add them to the roster
            name = input("Name:")
            age = input("age:")
            ID = input("ID:")
            city = input("City:")
            superior = input("Suerior:")
            branchcodes = input("Branch(es):")
            
            branchcodes = branchcodes.split(",")
            branchcodes = [int(i) for i in branchcodes]

            salary = input("Salary: ")
            salesman = Salesman(name, age, ID, city, superior, branchcodes)

            sales_roster.append(salesman)

        elif last_input == 3:
            ID = int(input("ID: "))
            # Print employee details for the given employee ID that is given. 
            
            found_employee = None
            for employee in engineer_roster + sales_roster:
                if employee.ID == int(ID):
                    found_employee = employee
                    break
            
            if not found_employee: print("No such employee")
            else:
                print(f"Name: {found_employee.name} and Age: {found_employee.age}")
                print(f"City of Work: {found_employee.city}")

                ## Write code here to list the branch names to
                ## which the employee reports as a comma separated list
                ## eg> Branches: Goregaon,Fort
                branch_names = [branchmap[i] for i in found_employee.branches]
                ## ???? what comes here??
                # print(f"Branches: " + ???? )
                print(f"Branch: " + ','.join(map(str, branch_names)))
                
                print(f"Salary: {found_employee.salary}")

        elif last_input == 4:
            ID = int(input("ID: "))
            new_branch = int(input("New branch code: "))
            
            found_employee = None
            for employee in engineer_roster + sales_roster:
                if employee.ID == int(ID):
                    found_employee = employee
                    break
            #### NO IF ELSE ZONE ######################################################
            # Change branch to new branch or add a new branch depending on class
            # Inheritance should automatically do this. 
            # There should be no IF-ELSE or ternary operators in this zone
            if not found_employee: found_employee.migrate_branch(new_branch)
            #### NO IF ELSE ZONE ENDS #################################################

        elif last_input == 5:
            ID = int(input("Enter Employee ID to promote: "))
            # promote employee to next position
            
            found_employee = None
            for employee in engineer_roster + sales_roster:
                if employee.ID == int(ID):
                    found_employee = employee
                    break
            
            next_posin = found_employee.positions.index(found_employee.position)+1
            next_pos = found_employee.positions[next_pos]
            if not found_employee: found_employee.promote(next_pos)
            

        elif last_input == 6:
            ID = int(input("Enter Employee ID to give increment: "))
            amt = float(input("Enter amount to be incremented: "))
            # Increment salary of employee.
            found_employee = None
            for employee in engineer_roster + sales_roster:
                if employee.ID == int(ID):
                    found_employee = employee
                    break
            if not found_employee: found_employee.increment(amt)
        
        elif last_input == 7:
            ID = int(input("Enter Employee ID to find superior: "))
            # Print superior of the sales employee.
            found_employee = None
            for employee in sales_roster:
                if employee.ID == int(ID):
                    found_employee = employee
                    break
            if not found_employee: print(found_employee.find_superior())
        
        elif last_input == 8:
            ID_E = int(input("Enter Employee ID to add superior: "))
            ID_S = int(input("Enter Employee ID of superior: "))
            # Add superior of a sales employee
            found_employee = None
            for employee in sales_roster:
                if employee.ID == int(ID_E):
                    found_employee = employee
                    break
            if not found_employee: found_employee.add_superior(ID_S)

        else:
            raise ValueError("No such query number defined")

            
            

            


            


        






