from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        self.decision_stack = []

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 
        assignment = {}
       

        #X = sd_spots
       
        # TODO: implement backtracking search. 
        while True:
            conflict, assignment, domains = self.propagate(assignment, domains)
            
            if not conflict:
                if self.all_assigned(domains):
                    return self.solution(assignment)
                else:
                    assignment, spot = self.make_decision(assignment, domains)
                    self.decision_stack.append((copy.deepcopy(assignment), spot, copy.deepcopy(domains)))
                    
            else:
                if len(self.decision_stack) == 0: 
                    return None
                else:
                    assignment, domains = self.backtrack()
       
    # TODO: add any supporting function you need
    def propagate(self, assignment, domains): 
        conflict = False
        while True:
            # synchronizing assignment and domains
            for spot in domains.keys():
                if len(domains[spot]) == 1 and spot not in assignment.keys():
                    assignment[spot] = domains[spot]
            for spot in domains.keys():    
                if len(domains[spot]) > 1 and spot in assignment.keys():
                    domains[spot] = assignment[spot]
            for spot in domains.keys():
                if len(domains[spot]) == 0:
                    conflict = True
                    return conflict, assignment, domains
        
            return_flag = True
            #inference using arc-consistency
            incons_doms = [spot for spot in sd_spots if spot not in assignment.keys()]
            for spot in incons_doms:
                for peer_spot in sd_peers[spot]:
                    if len(domains[peer_spot]) == 1:
                        ele = domains[peer_spot][0] 
                        if ele in domains[spot]:
                            #remove that element from domain of spot
                            domains[spot].remove(ele)
                            return_flag = False

       
            if return_flag == True: # all domains are arc-consistent
                #print("consistent")      
                return conflict, assignment, domains
   
    def make_decision(self, assignment, domains):
        #pick x in assignment that's unassigned
        #x = self.select_unassigned_variable(domains) 
        
        # use heuristic
        x = self.heuristic(domains)
       
        #make one decision i.e pick an element,a, in D(x)
        a = random.choice(domains[x])
       
        #add (x,a) to assignment
        assignment[x] = [a]
        
        return assignment, x
    
    def backtrack(self):

        assignment, x, domains = self.decision_stack.pop()
        a = assignment[x][0] 
        del assignment[x]
        domains[x].remove(a)

        return  assignment, domains

    def all_assigned(self, domains):
        unassigned_spots = [spot for spot in domains.keys() if len(domains[spot]) > 1]
        if not unassigned_spots: 
            return True
        return False
    
    def solution(self, assignment):
        # Convert assignment to the domains format
        sol_domains = {}
        for spot, value in assignment.items():
            sol_domains[spot] = value
        return sol_domains
    
    def select_unassigned_variable(self, domains):
        unassigned_spots = [spot for spot in domains.keys() if len(domains[spot]) > 1]
        return random.choice(unassigned_spots)
    
    def heuristic(self, domains):
        unassigned_spots = [spot for spot in domains.keys() if len(domains[spot]) > 1]
        if not unassigned_spots:
            return None
        # Find the spot with the smallest domain
        min_domain_size = float('inf')
        selected_spot = None
        for spot in unassigned_spots:
            domain_size = len(domains[spot])
            if domain_size < min_domain_size:
                min_domain_size = domain_size
                selected_spot = spot

        return selected_spot
                

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
