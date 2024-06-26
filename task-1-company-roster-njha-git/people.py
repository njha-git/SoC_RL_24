"""
We'll try to understand classes in python. 
Check the resources on google classroom to ensure you have gone through everything expected.

"""
###### THESE LISTS HAVE ALREADY BEEN DEFINED FOR YOU ###############
engineer_roster = [] # A list of all instantiated engineer objects
sales_roster = [] # List of all instantiated sales objects
branchmap = {  # A dictionary of dictionaries -> Maps branchcodes to cities and branch names
    0:  { "city": "NYC", "name": "Hudson Yards"},
    1:  { "city": "NYC" , "name": "Silicon Alley"},
    2:  { "city": "Mumbai", "name": "BKC"},
    3:  { "city": "Tokyo", "name": "Shibuya"},
    4:  { "city": "Mumbai", "name": "Goregaon"},
    5:  { "city": "Mumbai", "name": "Fort"}
}
####################################################################

class Employee:
    name : str 
    age : int
    ID : int
    city : str
    branches : list[int] # This is a list of branches (as branch codes) to which the employee may report
    salary : int 

    def __init__(self, name, age, ID, city,\
                 branchcodes, salary = None):
        self.name = name
        self.age = age 
        self.ID = ID
        self.city = city
        self.branches = branchcodes
        if salary is not None: self.salary = salary
        else: self.salary = 10_000 
    
    def change_city(self, new_city:str) -> bool:
        # Change the city 
        # Return true if city change, successful, return false if city same as old city
        if self.city != new_city:
            self.city = new_city
            return True
        else:
            return False

    def migrate_branch(self, new_code:int) -> bool:
        # Should work only on those employees who have a single 
        # branch to report to. Fail for others.
        # Change old branch to new if it is in the same city, else return false.
        if len(self.branches) == 1:
            if branchmap[self.branches]["city"] == branchmap[new_code]["city"]:
                self.branches[0] = new_code
        
        else: return False

    def increment(self, increment_amt: int) -> None:
        # Increment salary by amount specified.
        self.salary += increment_amt





class Engineer(Employee):
    position : str # Position in organization Hierarchy
    positions = ["Junior", "Senior", "Team Lead", "Director"]

    def __init__(self, name, age, ID, city,\
                 branchcodes, position= "Junior", salary = None):
        # Call the parent's constructor
        super().__init__(name, age, ID, city, branchcodes, salary)
        
        # Check if position is one of  "Junior", "Senior", "Team Lead", or "Director" 
        # Only then set the position.
        if position in self.positions:
            self.position = position
    
    def increment(self, amt:int) -> None:
        # While other functions are the same for and engineer,
        # and increment to an engineer's salary should add a 10% bonus on to "amt"
        self.salary += 1.1*amt
        
    def promote(self, position:str) -> bool:
        # Return false for a demotion or an invalid promotion
        # Promotion can only be to a higher position and
        # it should call the increment function with 30% of the present salary
        # as "amt". Thereafter return True.
        if self.positions.index(position) > self.positions.index(self.position):
            self.position = position
            self.salary += 0.3*self.salary
            return True
        else:
            return False
        



class Salesman(Employee):
    """ 
    This class is to be entirely designed by you.

    Add increment (this time only a 5% bonus) and a promotion function
    This time the positions are: Rep -> Manager -> Head.

    Add an argument in init which tracks who is the superior
    that the employee reports to. This argument should be the ID of the superior
    It should be None for a "Head" and so, the argument should be optional in init.
    """
    
    # An extra member variable!
    superior : int # EMPLOYEE ID of the superior this guy reports to
    position : str # Position in organization Hierarchy
    positions = ["Junior", "Senior", "Team Lead", "Director"]

    def __init__(self, name, age, ID, city,\
                 branchcodes, superior=None, position="Junior", salary = None): # Complete all this! Add arguments

        super().__init__(name, age, ID, city, branchcodes, salary)
        self.superior = superior
    
    # def promote
    def promote(self, position:str) -> bool:
        if self.positions.index(position) > self.positions.index(self.position):
            self.position = position
            self.salary += 0.3*self.salary
            return True
        else:
            return False

    # def increment

    def find_superior(self) -> tuple[int, str]:
        # Return the employee ID and name of the superior
        # Report a tuple of None, None if no superior.
        find_superior = None
        for employee in engineer_roster + sales_roster:
            if employee.ID == self.superior:
                find_superior = (self.superior, employee.name)
                break
        return find_superior
    

    def add_superior(self, ID) -> bool:
        # Add superior of immediately higher rank.
        # If superior doesn't exist return false,
        found_superior = None
        for superior in engineer_roster + sales_roster:
                if superior.ID == int(ID):
                    found_superior = superior
                    break
        
        if not found_superior:
            self.superior = found_superior
            return True
        else:
            return False

    def migrate_branch(self, new_code: int) -> bool:
        # This should simply add a branch to the list; even different cities are fine
        self.branches.append(new_code)

    





    
    