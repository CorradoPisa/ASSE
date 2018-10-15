class Poll():

    def __init__(self, id, title, options):
        self.id = id
        self.title = title
        self.options = {op: [] for op in options}
        print(self.options)

    def vote(self, person, vote):
        if vote in self.options:
            if not(person in self.options[vote]):
                self.options[vote].append(person)
            else:
                msg = person + "has already voted."
                raise UserAlreadyVotedException(msg)
        else:
            msg = vote + " is not a valid option for the poll."
            raise NonExistingOptionException(msg)  

        result = self.get_winners()  

        return result

    def get_winners(self):
        winners = []
        max_votes = 0

        for o in self.options.keys():
            if len(self.options[o]) > max_votes:
                max_votes = len(self.options[o])
                winners = [o]
            elif len(self.options[o]) == max_votes:
                winners.append(o)
        
        return winners 

    def get_voted_options(self, person):
        return [o for o, voters in self.options.items() if person in voters]

    def delete_voted_options(self, person):
        found = False
        for o in self.options.keys():
            if person in self.options[o]:
                found = True
                self.options[o].remove(person)
        return found

    def serialize(self):
        winners = self.get_winners()
        return {'id':self.id, 
                'title': self.title, 
                'options': self.options,
                'winners' : winners}


class UserAlreadyVotedException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NonExistingOptionException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
