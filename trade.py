import random
import threading
import time

# Define the AI players
class AIPlayer:
    def __init__(self, name):
        self.name = name
        self.money = 100
        self.items = []
        self.trading_unlocked = False
        self.losses = {5: 0, 10: 0, 50: 0, 100: 0}
        self.allies = []
        self.memory = []

    def reset(self):
        self.money = 100
        self.items = []
        self.trading_unlocked = False
        self.losses = {5: 0, 10: 0, 50: 0, 100: 0}
        self.memory = []

    def buy_crate(self, price):
        if self.money >= price:
            self.money -= price
            item_value = self.get_item_value(price)
            self.items.append(item_value)
            self.memory.append(('buy', price, item_value))
            if len(self.items) >= 5:
                self.trading_unlocked = True
            # Update losses
            if item_value < price:
                self.losses[price] += 1
            else:
                self.losses[price] = max(0, self.losses[price] - 1)

    def get_item_value(self, price):
        # Define item values based on crate price with varying rarities
        if price == 5:
            return random.choices([1, 2, 3, 4, 5, 10], [0.4, 0.3, 0.2, 0.1, 0.05, 0.01])[0]
        elif price == 10:
            return random.choices([5, 6, 7, 8, 10, 20], [0.4, 0.3, 0.2, 0.1, 0.05, 0.01])[0]
        elif price == 50:
            return random.choices([20, 30, 40, 50, 75, 100], [0.4, 0.3, 0.2, 0.1, 0.05, 0.01])[0]
        elif price == 100:
            return random.choices([50, 75, 100, 150, 200, 300], [0.4, 0.3, 0.2, 0.1, 0.05, 0.01])[0]

    def trade_items(self, other_player):
        if self.trading_unlocked and other_player.trading_unlocked:
            # Value-based trading
            if self.items and other_player.items:
                self_item = random.choice(self.items)
                other_item = random.choice(other_player.items)
                if self_item < other_item:
                    self.items.remove(self_item)
                    other_player.items.remove(other_item)
                    self.items.append(other_item)
                    other_player.items.append(self_item)
                    # Add money incentive
                    money_incentive = random.randint(1, 10)
                    if self.money >= money_incentive:
                        self.money -= money_incentive
                        other_player.money += money_incentive
                    # Incentive for successful trade
                    self.money += 5
                    other_player.money += 5
                    self.memory.append(('trade', self_item, other_item, money_incentive))
                else:
                    # Item bundling
                    if len(self.items) > 1 and len(other_player.items) > 1:
                        self_bundle = random.sample(self.items, 2)
                        other_bundle = random.sample(other_player.items, 2)
                        self_value = sum(self_bundle)
                        other_value = sum(other_bundle)
                        if self_value < other_value:
                            for item in self_bundle:
                                self.items.remove(item)
                            for item in other_bundle:
                                other_player.items.remove(item)
                            self.items.extend(other_bundle)
                            other_player.items.extend(self_bundle)
                            # Add money incentive
                            money_incentive = random.randint(1, 10)
                            if self.money >= money_incentive:
                                self.money -= money_incentive
                                other_player.money += money_incentive
                            # Incentive for successful trade
                            self.money += 5
                            other_player.money += 5
                            self.memory.append(('trade', self_bundle, other_bundle, money_incentive))

    def choose_crate_price(self):
        # Avoid prices that have caused losses
        prices = [5, 10, 50, 100]
        for price in prices:
            if self.losses[price] > 3:  # Threshold for avoiding a price
                prices.remove(price)
        return random.choice(prices)

    def sell_items(self):
        # Sell items if they feel it is good
        if self.items:
            item_to_sell = random.choice(self.items)
            self.items.remove(item_to_sell)
            self.money += item_to_sell
            # Incentive for selling items
            self.money += 5
            self.memory.append(('sell', item_to_sell))

    def form_alliance(self, other_player):
        if other_player not in self.allies:
            self.allies.append(other_player)
            other_player.allies.append(self)

    def net_worth(self):
        return self.money + sum(self.items)

    def evaluate_decisions(self):
        # Evaluate decisions based on memory
        for decision in self.memory:
            if decision[0] == 'buy':
                price, item_value = decision[1], decision[2]
                if item_value < price:
                    self.losses[price] += 1
                else:
                    self.losses[price] = max(0, self.losses[price] - 1)
            elif decision[0] == 'trade':
                self_item, other_item, money_incentive = decision[1], decision[2], decision[3]
                if self_item < other_item:
                    self.money += money_incentive
                else:
                    self.money -= money_incentive
            elif decision[0] == 'sell':
                item_to_sell = decision[1]
                self.money += item_to_sell

# Initialize AI players with names
player_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
players = [AIPlayer(name) for name in player_names]

# Form alliances
def form_alliances():
    for player in players:
        potential_allies = [p for p in players if p != player and p not in player.allies]
        if potential_allies:
            ally = random.choice(potential_allies)
            player.form_alliance(ally)

# Simulate the game
def simulate_game():
    form_alliances()
    for player in players:
        player.reset()
    for _ in range(100):  # Simulate 100 rounds
        for player in players:
            crate_price = player.choose_crate_price()
            player.buy_crate(crate_price)
            if player.trading_unlocked:
                other_player = random.choice(players)
                if other_player != player:
                    player.trade_items(other_player)
            player.sell_items()
            player.evaluate_decisions()

# Generate leaderboard
def generate_leaderboard():
    leaderboard = sorted(players, key=lambda x: x.net_worth(), reverse=True)
    return leaderboard

# Display leaderboard
def display_leaderboard():
    leaderboard = generate_leaderboard()
    print("\nLeaderboard:")
    print("{:<10} {:<10} {:<10}".format("Rank", "Player", "Net Worth"))
    for rank, player in enumerate(leaderboard, 1):
        print("{:<10} {:<10} {:<10}".format(rank, player.name, player.net_worth()))

# Update leaderboard every 3 seconds
def update_leaderboard():
    while True:
        simulate_game()
        display_leaderboard()
        time.sleep(3)

if __name__ == '__main__':
    leaderboard_thread = threading.Thread(target=update_leaderboard)
    leaderboard_thread.start()
