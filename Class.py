class member:
    count_members = 0

    def __init__(self,name,rasa):
        self.name = name
        self.rasa = rasa
        self.relationship = 0
        member.count_members += 1
        self.goal = 0
        self.otvet = -1
    
    def win_vict(self):
        self.goal += 1
    
    def get_dict(self) -> dict:
        state = {}
        state["name"]=self.name
        state["rasa"]=self.name
        state["relationship"]=self.name
        state["goal"]=self.name
        return state
    
    def get_count():
        return member.count_members

    


    