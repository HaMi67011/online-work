import mesa 
import random

NUMBER_OF_CELLS = 50

FREE=1
BUSY=0
UNDONE=0
DONE=1
IN_TRANSIT_SAFE = 2
IN_TRANSIT_DEAD = 3

class FirstAidRobot(mesa.Agent):
    def __init__(self, id, pos, model, init_state=FREE):
        super().__init__(id, model)

        self.x, self.y = pos 
        
        self.lane = self.y
        
        self.safe_zone = 0
        
        if (self.unique_id + 1) % 2 == 0:
                self.safe_zone = self.model.grid.height -1
        else:
            self.safe_zone = 1
        
        self.next_x, self.next_y = None, None

        self.state = init_state
        
        self.payload = []

    def isBusy(self):
        return self.state == BUSY 

    def step(self):
        str_action = self.make_decision()
        action = getattr(self,str_action)
        action()
        
    def move_sz(self):
        """
        Move the agent to the safe zone
        """
        self.move_to([self.x,self.safe_zone])
        self.move_payload()

    def make_decision(self):
        action="wait"
        
        if self.state != FREE and (self.pos[1]+1 == 49 or self.pos[1]-1 == 0):
                action = "drop_off"
     
        elif self.state == FREE:
            next_position = (self.x+1,  self.y)
            if not self.model.grid.is_cell_empty(next_position):
                action = "pick"
            elif next_position[0] < NUMBER_OF_CELLS -1 :
                action = "move_fw"
        else:
            if self.pos[0]-1 == 0:
                action = "drop_off"
            else:
                if not self.is_payload_safe():
                    action  = "move_sz"
                else:
                    action = "move_bw"
        print("ag_",self.unique_id, "action:", action)
        return action

    def move_to(self, dest):
        d_y = 0
        d_x = 0

        if self.y > dest[1] and self.pos[1]>=2:
            d_y =-1
        elif self.y< dest[1] and self.pos[1]<= NUMBER_OF_CELLS-1:
            d_y=1

        if self.x > dest[0] and self.pos[0]>=2:
            d_x =-1
        elif self.x< dest[0] and self.pos[0]<=NUMBER_OF_CELLS-1:
            d_x=1

        self.next_x= self.x+d_x
        self.next_y= self.y+d_y
        self.move()

    def move(self):
        self.model.grid.move_agent(self, (self.next_x,self.next_y))
        
        
    def move_payload(self):
        """
        * Obtains the person whose id is in the payload 
        * move the agent together with the person
        """
        person = [ a for a in self.model.schedule.agents if isinstance(a,Person) and a.unique_id == self.payload ]
        if len(person)>0:
            self.model.grid.move_agent(person[0],(self.x,self.y))


    def wait(self):
        """
        Keep the same position as the current one.
        """
        self.next_x = self.x
        self.next_y = self.y

    def move_fw(self):
        self.next_x = self.x+1
        self.next_y = self.y
        self.move()
        
    def move_bw(self):
        self.next_x = self.x-1
        self.next_y = self.y 
        self.move()
        self.move_payload()

    def move_lane(self):
        self.move_to([self.x, self.lane])

    def advance(self):
        self.x=self.next_x
        self.y=self.next_y
        
    def pick(self):
        """
        * change first aid state to Busy
        * find out the id of the person next to the first aid
        * store the person id in the payload of the first aid
        """
        self.state = BUSY  
        nbs = [nb for nb in self.model.grid.neighbor_iter((self.x, self.y), False)]

        for i in range(len(nbs)):
            if isinstance(nbs[i], Person):
                person = nbs[0]
                person.set_state(IN_TRANSIT_SAFE)
                self.payload = person.unique_id
    def drop_off(self):
        """
        * change state of the first aid to Free
        * Get the person whose id is in the payload and remove it from the grid and change its state to Done.
        * Remove payload from first aid
        * move agent to next position ahead of the person
        """
        self.state = FREE 
        person = [ a for a in self.model.schedule.agents if isinstance(a,Person) and a.unique_id == self.payload ]
        if len(person)>0:
            person[0].state = DONE
            self.model.grid.remove_agent(person[0])
        self.payload = None
        self.next_x = self.next_x + 1
        self.move()
        
    def get_payload(self):
        """
        Returns the agent object for the person being transported.
        """
        return [ a for a in self.model.schedule.agents if  a.unique_id == self.payload ][0]
        

    def is_payload_safe(self):
        """
        Checks whether the person is safe.
        """
        person = self.get_payload()
        return person.isSafe

class ExplorerDrones(mesa.Agent):
    def __init__(self, id, pos, model, init_state=FREE):
        super().__init__(id, model)

        self.x, self.y = pos 
        
        self.lane = self.y
        
        self.safe_zone = 0
        if (self.unique_id + 1) % 2 == 0:
            self.safe_zone = self.model.grid.height -1
        else:
            self.safe_zone = 1

        self.next_x, self.next_y = None, None
        
        self.state = init_state
        
        self.payload = []

    def calculate_urgency_to_person(self):
        person = ""
        # three categories -> low, mid, high risk 
        lowRisk = "low"
        midRisk = "mid"
        highRisk = "high"
        

        if person.age > 60 or person.age < 18:
            return highRisk
        elif person.age >= 18 and person.age <= 60 and person.health <= 60:
            return midRisk
        elif person.age >= 18 and person.age <= 60 and person.health == 100:
            return lowRisk


    def step(self):
        str_action = self.make_decision()
        action = getattr(self,str_action)
        action()


    def move_sz(self):
        """
        Move the agent to the safe zone
        """
        self.move_to([self.x,self.safe_zone])
        self.move_payload()
    def make_decision(self):
        
        action="wait"
        
        if self.state != FREE and (self.pos[1]+1 == 49 or self.pos[1]-1 == 0):
                action = "drop_off"
     
        elif self.state == FREE:
            next_position = (self.x+1,  self.y)
            if not self.model.grid.is_cell_empty(next_position):
                action = "pick"
            elif next_position[0] < NUMBER_OF_CELLS -1 :
                action = "move_fw"
        else:
            if self.pos[0]-1 == 0:
                action = "drop_off"
            else:
                if not self.is_payload_safe():
                    action  = "move_sz"
                else:
                    action = "move_bw"
        print("ag_",self.unique_id, "action:", action)
        return action

    def move_to(self, dest):
        d_y = 0
        d_x = 0

        if self.y > dest[1] and self.pos[1]>=2:
            d_y =-1
        elif self.y< dest[1] and self.pos[1]<= NUMBER_OF_CELLS-1:
            d_y=1

        if self.x > dest[0] and self.pos[0]>=2:
            d_x =-1
        elif self.x< dest[0] and self.pos[0]<=NUMBER_OF_CELLS-1:
            d_x=1

        self.next_x= self.x+d_x
        self.next_y= self.y+d_y
        self.move()

    def move(self):
        self.model.grid.move_agent(self, (self.next_x,self.next_y))
        
        
    def move_payload(self):
        """
        * Obtains the person whose id is in the payload 
        * move the person together with the person
        """
        person = [ a for a in self.model.schedule.agents if isinstance(a,Person) and a.unique_id == self.payload ]
        if len(person)>0:
            self.model.grid.move_agent(person[0],(self.x,self.y))


    def wait(self):
        """
        Keep the same position as the current one.
        """
        self.next_x = self.x
        self.next_y = self.y

    def move_fw(self):
        self.next_x = self.x+1
        self.next_y = self.y
        self.move()
        
    def move_bw(self):
        self.next_x = self.x-1
        self.next_y = self.y 
        self.move()
        self.move_payload()

    def move_lane(self):
        self.move_to([self.x, self.lane])

    def advance(self):
        self.x=self.next_x
        self.y=self.next_y
        
    def pick(self):
        """
        * change first aid state to Busy
        * find out the id of the person next to the first aid
        * store the person id in the payload of the first aid
        """
        self.state = BUSY  
        nbs = [nb for nb in self.model.grid.neighbor_iter((self.x, self.y), False)]

        for i in range(len(nbs)):
            if isinstance(nbs[i], Person):
                person = nbs[0]
                person.set_state(IN_TRANSIT_SAFE)
                self.payload = person.unique_id
                
    def drop_off(self):
        """
        * change state of the first aid to Free
        * Get the person whose id is in the payload and remove it from the grid and change its state to Done.
        * Remove payload from first aid
        * move agent to next position ahead of the person
        """
        self.state = FREE 
        person = [ a for a in self.model.schedule.agents if isinstance(a,Person) and a.unique_id == self.payload ]
        if len(person)>0:
            person[0].state = DONE
            self.model.grid.remove_agent(person[0])
        self.payload = None
        self.next_x = self.next_x + 1
        self.move()
        
    def get_payload(self):
        """
        Returns the agent object for the person being transported.
        """
        return [ a for a in self.model.schedule.agents if  a.unique_id == self.payload ][0]
        

    def is_payload_safe(self):
        """
        Checks whether the person is safe.
        """
        person = self.get_payload()
        return person.isSafe
    
    
    @property
    def isBusy(self):
        return self.state == BUSY
    
class Person(mesa.Agent):
    def __init__(self, id, pos, model, init_state=UNDONE):
        super().__init__(id, model)
        
        self.state = UNDONE

        self.next_state = UNDONE
        
        self.x, self.y = pos 

        # assuming in our game age 1-100
        self.age = random.randint(1, 100)

        # assuming health points (hp) 1-100
        self.health = random.randint(1, 100)
    

    def set_state(self, new_state):
        self.state = new_state
    
    @property
    def isSafe(self):
        return self.state != IN_TRANSIT_DEAD

    def step(self):
        """
        It changes state of the person
        """
        broken_chance = self.random.random()
        if self.state == IN_TRANSIT_SAFE and broken_chance < 0.02:
            self.state = IN_TRANSIT_DEAD
        