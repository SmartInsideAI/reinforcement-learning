"""
TODO : 
- How to set and reload data ?
- What's the relation between agents and data ?

"""


import pandas as pd
import numpy as np
import uuid



#======================================================================================
# ENVIRONMENT CLASSES
#======================================================================================


class Environment:
    def __init__(self):

        SCHEMA = ["agent_id","agent_type","agent"]
        self._data = pd.DataFrame(columns = SCHEMA).set_index("agent_id")


    @property
    def agents(self):
        return self._data["agent"].tolist()

    @property
    def data(self):
        return self._data.drop(columns = "agent")
    
    def __getitem__(self,key):
        if isinstance(key,int):
            return self._data.iloc[key].loc["agent"]
        else:
            return self.get_agent(key)

    def __iter__(self):
        return iter(self.agents)


    def _repr_html_(self):
        return self.data.head(20)._repr_html_()

    def add_agent(self,agent,agent_data):
        agent_data["agent"] = agent
        agent_data = pd.DataFrame([agent_data]).set_index("agent_id")
        self._data = self._data.append(agent_data,verify_integrity = True,sort = False)

    def remove_agent(self,agent_id):
        self._data.drop(agent_id,inplace = True)

    def get_agent(self,agent_id):
        return self._data.loc[agent_id,"agent"]

    def step(self):
        reward = 0
        for agent in self.agents:
            reward_agent = agent.step()
            reward += reward_agent
        return reward

    def run(self,n):
        rewards = []
        for i in range(n):
            reward = self.step()
            rewards.append(reward)
        return rewards





class Environment2D(Environment):
    def __init__(self):
        super().__init__()

    def show(self):
        self.data["coords"].apply(pd.Series).rename(columns = {0:"x",1:"y"}).plot(kind = "scatter",x=0,y=1,figsize = (6,6))


        

#======================================================================================
# AGENT CLASSES
#======================================================================================


class Agent:
    def __init__(self,env,agent_data = {}):

        # Base parameters
        self.agent_id = str(uuid.uuid1())
        self.agent_type = self.__class__.__name__
        self.internal_clock = 0

        # Base agent data
        agent_data = {
            "agent_id":self.agent_id,
            "agent_type":self.agent_type,
            **agent_data
        }

        # Prepare data as argument        
        self.env = env
        self.env.add_agent(self,agent_data)


    def step(self):
        self.internal_clock += 1


    def __getitem__(self,key):
        return self.get(key)

    def __repr__(self):
        return f"{self.agent_type}(id={self.agent_id})"

    def get_data(self):
        return self.env[self.agent_id].to_dict()

    def get(self,key):
        return self.env._data.loc[self.agent_id,key]

    def set(self,key,value):
        self.env._data.loc[self.agent_id,key] = value

    def add(self,key,value):
        self.env._data.loc[self.agent_id,key] += value

    def multiply(self,key,value):
        self.env._data.loc[self.agent_id,key] *= value

    def sub(self,key,value):
        self.env._data.loc[self.agent_id,key] -= value

    def divide(self,key,value):
        self.env._data.loc[self.agent_id,key] /= value







#======================================================================================
# SUGARSCAPE CLASSES
#======================================================================================



class Rabbit(Agent):
    def __init__(self,env,**kwargs):

        # Prepare agent parameters
        agent_data = {
            "life":np.random.randint(10,20),
            "coords":(np.random.randint(0,10),np.random.randint(0,10)),
        }
        agent_data["life_left"] = agent_data["life"]

        # Init
        super().__init__(env,agent_data)



    def step(self):
        super().step()

        self.sub("life_left",1)
        
        if self["life_left"] == 0:
            self.env.remove_agent(self.agent_id)
            return -1
        else:
            return 0








class Sugarscape(Environment2D):
    def __init__(self):
        pass