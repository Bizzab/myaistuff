import random
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class Leader:
    def __init__(self, name, country):
        self.name = name
        self.country = country
        self.personality = np.random.rand(5)  # Big Five personality traits
        self.opinions = {}  # Personal opinions of other leaders

    def form_opinion(self, other_leader):
        personality_diff = np.linalg.norm(self.personality - other_leader.personality)
        compatibility = 1 / (1 + personality_diff)  # Higher when personalities are similar
        opinion = int((compatibility * 50 + random.randint(0, 50)) * 2)  # Scale to 0-100
        self.opinions[other_leader.name] = max(0, min(100, opinion))

    def update_opinion(self, other_leader, change):
        if other_leader.name in self.opinions:
            self.opinions[other_leader.name] = max(0, min(100, self.opinions[other_leader.name] + change))

class Country:
    def __init__(self, leader_name):
        self.leader = Leader(leader_name, self)
        self.name = None  # Will be set by the leader
        self.economy = random.randint(30, 70)
        self.approval = random.randint(30, 70)
        self.relations = {}
        self.resources = {
            "oil": random.randint(0, 100),
            "minerals": random.randint(0, 100),
            "agriculture": random.randint(0, 100),
            "technology": random.randint(0, 100)
        }
        self.money = random.randint(1000, 5000)
        self.alliances = []
        self.treaties = []
        self.secret_info = {}

    def update(self, global_resources):
        pass

    def propose_trade(self, other_country, global_resources):
        pass

    def evaluate_trade(self, trade_offer, global_resources, other_leader):
        offer_value = trade_offer["offer_amount"] * global_resources[trade_offer["offer_resource"]].current_value
        request_value = trade_offer["request_amount"] * global_resources[trade_offer["request_resource"]].current_value
        
        risk_tolerance = self.leader.personality[0]  # Use the first personality trait as risk tolerance
        opinion_factor = self.leader.opinions.get(other_leader.name, 50) / 100  # Normalize opinion to 0-1
        
        value_threshold = 0.9 + (risk_tolerance * 0.2) - (opinion_factor * 0.1)
        
        if offer_value >= request_value * value_threshold:
            return "accept"
        elif offer_value >= request_value * (value_threshold - 0.1):
            return "counter"
        else:
            return "reject"

    def generate_speech(self, target_country, tokenizer, model, context, audience="public"):
        opinion = self.leader.opinions.get(target_country.leader.name, 50)
        opinion_context = "positive" if opinion > 60 else "negative" if opinion < 40 else "neutral"
        
        if audience == "public":
            prompt = f"As {self.leader.name}, leader of {self.name}, I want to publicly address {target_country.leader.name} of {target_country.name} about {context}. My opinion of them is {opinion_context}. "
        elif audience == "private":
            prompt = f"As {self.leader.name}, leader of {self.name}, I want to privately tell {target_country.leader.name} of {target_country.name} about {context}. My opinion of them is {opinion_context}. "
        else:  # secret
            prompt = f"As {self.leader.name}, leader of {self.name}, I want to secretly whisper to {target_country.leader.name} of {target_country.name} about {context}. My opinion of them is {opinion_context}. "
        
        input_ids = tokenizer.encode(prompt, return_tensors='pt')
        output = model.generate(input_ids, max_length=100, max_new_tokens=70, num_return_sequences=1, no_repeat_ngram_size=2)
        speech = tokenizer.decode(output[0], skip_special_tokens=True)
        return speech

def initialize_countries(num_countries, tokenizer, model):
    countries = []
    for i in range(num_countries):
        leader_name = generate_name(tokenizer, model)
        country = Country(leader_name)
        country.name = generate_country_name(tokenizer, model, leader_name)
        countries.append(country)
    
    for country in countries:
        for other_country in countries:
            if country != other_country:
                country.leader.form_opinion(other_country.leader)
                country.relations[other_country.name] = random.randint(20, 80)
    
    return countries

def generate_name(tokenizer, model):
    prompt = "Generate a random leader name: "
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids, max_length=30, max_new_tokens=20, num_return_sequences=1, no_repeat_ngram_size=2)
    name = tokenizer.decode(output[0], skip_special_tokens=True).strip()
    return name

def generate_country_name(tokenizer, model, leader_name):
    prompt = f"As {leader_name}, generate a name for my country: "
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids, max_length=30, max_new_tokens=20, num_return_sequences=1, no_repeat_ngram_size=2)
    name = tokenizer.decode(output[0], skip_special_tokens=True).strip()
    return name

def simulate_interaction(country1, country2, tokenizer, model, global_resources, all_countries):
    interaction_type = random.choice(["diplomacy", "trade", "treaty", "secret"])
    
    opinion_change = random.randint(-3, 3)
    country1.leader.update_opinion(country2.leader, opinion_change)
    country2.leader.update_opinion(country1.leader, opinion_change)
    
    if interaction_type == "diplomacy":
        context = "improving our diplomatic relations"
        speech = country1.generate_speech(country2, tokenizer, model, context, "public")
        relation_change = random.randint(-5, 5)
        country1.relations[country2.name] += relation_change
        country2.relations[country1.name] += relation_change
        return f"Public: {country1.leader.name} of {country1.name} to {country2.leader.name} of {country2.name}: {speech}"
    
    elif interaction_type == "trade":
        trade_offer = country1.propose_trade(country2, global_resources)
        context = f"proposing a trade of {trade_offer['offer_amount']} {trade_offer['offer_resource']} for {trade_offer['request_amount']} {trade_offer['request_resource']}"
        speech = country1.generate_speech(country2, tokenizer, model, context, "public")
        
        evaluation = country2.evaluate_trade(trade_offer, global_resources, country1.leader)
        
        if evaluation == "accept":
            country1.resources[trade_offer['offer_resource']] -= trade_offer['offer_amount']
            country2.resources[trade_offer['offer_resource']] += trade_offer['offer_amount']
            country2.resources[trade_offer['request_resource']] -= trade_offer['request_amount']
            country1.resources[trade_offer['request_resource']] += trade_offer['request_amount']
            
            if trade_offer['money_difference'] > 0:
                country1.money -= trade_offer['money_difference']
                country2.money += trade_offer['money_difference']
            else:
                country2.money += abs(trade_offer['money_difference'])
                country1.money -= abs(trade_offer['money_difference'])
            
            return f"Public: {country1.leader.name} of {country1.name} and {country2.leader.name} of {country2.name} agreed on a trade. Speech: {speech}"
        
        elif evaluation == "counter":
            counter_offer = country2.propose_trade(country1, global_resources)
            counter_context = f"proposing a counter-offer of {counter_offer['offer_amount']} {counter_offer['offer_resource']} for {counter_offer['request_amount']} {counter_offer['request_resource']}"
            counter_speech = country2.generate_speech(country1, tokenizer, model, counter_context, "public")
            return f"Public: {country1.leader.name} of {country1.name} proposed a trade, but {country2.leader.name} of {country2.name} made a counter-offer. Speech: {counter_speech}"
        
        else:  # reject
            return f"Public: {country1.leader.name} of {country1.name} proposed a trade to {country2.leader.name} of {country2.name}, but it was rejected. Speech: {speech}"
    
    elif interaction_type == "treaty":
        pass
    
    else:  # secret communication
        context = random.choice(["a potential alliance", "shared concerns about a neighbor", "a covert operation"])
        speech = country1.generate_speech(country2, tokenizer, model, context, "secret")
        country2.receive_secret(country1, speech