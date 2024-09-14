import random
import time

class Country:
    def __init__(self, name, economy, resources, population, military_units, morale, technology):
        self.name = name
        self.economy = economy
        self.resources = resources  # Dictionary to store different types of resources
        self.population = population
        self.military_units = military_units  # Dictionary to store different types of military units
        self.morale = morale
        self.technology = technology
        self.diplomacy_score = 50  # Neutral diplomacy score
        self.history = ["I am the leader of a country in Oompaloompaville."]  # Initialize memory with the fact
        self.learning_rate = 0.1  # Learning rate for reinforcement learning
        self.q_table = {}  # Initialize Q-table
        self.exploration_rate = 0.1  # Exploration rate for decision making
        self.discount_factor = 0.9  # Discount factor for Q-learning

    def get_state(self):
        return (self.economy, self.resources, self.population, self.military_units, self.morale, self.technology, self.diplomacy_score)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(['trade', 'war', 'alliance', 'espionage', 'sabotage'])
        else:
            return max(self.q_table.get(state, {}), key=self.q_table.get(state, {}).get, default='trade')

    def update_q_table(self, state, action, reward, next_state):
        old_value = self.q_table.get(state, {}).get(action, 0)
        next_max = max(self.q_table.get(next_state, {}).values(), default=0)
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = new_value

    def make_decision(self, other_country):
        state = self.get_state()
        action = self.choose_action(state)
        reward, next_state = self.respond_to_decision(action, other_country)
        self.update_q_table(state, action, reward, next_state)
        return action

    def respond_to_decision(self, decision, other_country):
        if decision == 'trade':
            return self.trade(other_country)
        elif decision == 'war':
            return self.war(other_country)
        elif decision == 'alliance':
            return self.alliance(other_country)
        elif decision == 'espionage':
            return self.espionage(other_country)
        elif decision == 'sabotage':
            return self.sabotage(other_country)

    def generate_dynamic_response(self, action, other_country):
        # Generate a response based on the current state and context
        if action == 'trade':
            return f"{self.name} proposes a trade deal with {other_country.name} to improve both economies."
        elif action == 'war':
            return f"{self.name} declares war on {other_country.name} due to rising tensions and resource disputes."
        elif action == 'alliance':
            return f"{self.name} suggests forming an alliance with {other_country.name} to strengthen diplomatic ties."
        elif action == 'espionage':
            return f"{self.name} conducts espionage against {other_country.name} to gather intelligence."
        elif action == 'sabotage':
            return f"{self.name} attempts to sabotage {other_country.name}'s infrastructure."

    def trade(self, other_country):
        response = self.generate_dynamic_response('trade', other_country)
        print(response)
        
        # Advanced trade system
        trade_value = min(self.resources['gold'], other_country.resources['gold']) // 2
        tariff = random.randint(1, 10)  # Random tariff value
        demand_factor = random.uniform(0.5, 1.5)  # Random demand factor
        economic_growth = random.uniform(0.01, 0.05)  # Random economic growth factor

        self.resources['gold'] += trade_value * demand_factor - tariff
        other_country.resources['gold'] += trade_value * demand_factor - tariff
        self.economy += self.economy * economic_growth
        other_country.economy += other_country.economy * economic_growth
        self.diplomacy_score += 10
        other_country.diplomacy_score += 10

        self.learn_from_interaction('trade', True)
        return f"{self.name} and {other_country.name} traded resources worth {trade_value} with a tariff of {tariff} and demand factor of {demand_factor}."

    def war(self, other_country):
        response = self.generate_dynamic_response('war', other_country)
        print(response)
        war_outcome = self.determine_war_outcome(other_country)
        if war_outcome == 'win':
            self.resources['gold'] += other_country.resources['gold'] // 2
            other_country.resources['gold'] //= 2
            self.population += other_country.population // 10
            other_country.population -= other_country.population // 10
            self.military_units['infantry'] -= 10
            other_country.military_units['infantry'] -= 20
            self.morale += 10
            other_country.morale -= 10
            self.diplomacy_score -= 20
            other_country.diplomacy_score -= 20
            self.learn_from_interaction('war', True)
            return f"{self.name} won the war and gained resources and population."
        else:
            other_country.resources['gold'] += self.resources['gold'] // 2
            self.resources['gold'] //= 2
            other_country.population += self.population // 10
            self.population -= self.population // 10
            self.military_units['infantry'] -= 20
            other_country.military_units['infantry'] -= 10
            self.morale -= 10
            other_country.morale += 10
            self.diplomacy_score -= 20
            other_country.diplomacy_score -= 20
            self.learn_from_interaction('war', False)
            return f"{self.name} lost the war and lost resources and population."

    def determine_war_outcome(self, other_country):
        # Determine the outcome of the war based on military units, morale, technology, terrain, and strategy
        self_strength = (self.military_units['infantry'] + self.military_units['tanks'] * 2 + self.military_units['aircraft'] * 3) + self.morale + self.technology + random.randint(-10, 10)
        other_strength = (other_country.military_units['infantry'] + other_country.military_units['tanks'] * 2 + other_country.military_units['aircraft'] * 3) + other_country.morale + other_country.technology + random.randint(-10, 10)
        terrain_factor = random.uniform(0.8, 1.2)  # Random terrain factor
        self_strength *= terrain_factor
        other_strength *= terrain_factor
        if self_strength > other_strength:
            return 'win'
        else:
            return 'lose'

    def espionage(self, other_country):
        response = self.generate_dynamic_response('espionage', other_country)
        print(response)
        success = random.choice([True, False])
        if success:
            intelligence_gathered = random.randint(10, 50)
            self.technology += intelligence_gathered
            self.diplomacy_score -= 10
            other_country.diplomacy_score -= 10
            return f"{self.name} successfully gathered intelligence worth {intelligence_gathered} technology points from {other_country.name}."
        else:
            self.diplomacy_score -= 20
            other_country.diplomacy_score -= 20
            return f"{self.name}'s espionage attempt failed and relations with {other_country.name} worsened."

    def sabotage(self, other_country):
        response = self.generate_dynamic_response('sabotage', other_country)
        print(response)
        success = random.choice([True, False])
        if success:
            damage = random.randint(10, 50)
            other_country.economy -= damage
            self.diplomacy_score -= 10
            other_country.diplomacy_score -= 10
            return f"{self.name} successfully sabotaged {other_country.name}'s infrastructure, causing {damage} economic damage."
        else:
            self.diplomacy_score -= 20
            other_country.diplomacy_score -= 20
            return f"{self.name}'s sabotage attempt failed and relations with {other_country.name} worsened."

    def alliance(self, other_country):
        response = self.generate_dynamic_response('alliance', other_country)
        print(response)
        self.diplomacy_score += 20
        other_country.diplomacy_score += 20
        self.learn_from_interaction('alliance', True)
        return f"{self.name} and {other_country.name} formed an alliance."

    def learn_from_interaction(self, action, success):
        # Adjust the decision-making process based on the outcome
        if success:
            self.diplomacy_score += self.learning_rate * 10
        else:
            self.diplomacy_score -= self