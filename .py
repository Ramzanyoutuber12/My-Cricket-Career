import random
from enum import Enum
import json
from datetime import datetime, timedelta

# Enums for game elements
class PlayerRole(Enum):
    BATTER = "Batter"
    BOWLER = "Bowler"
    ALL_ROUNDER = "All-Rounder"
    WICKETKEEPER = "Wicket-Keeper"

class Background(Enum):
    STREET_CRICKET = "Street Cricket"
    ACADEMY = "Cricket Academy"
    CLUB = "Local Club"
    UNIVERSITY = "University Team"

class MatchType(Enum):
    T20 = "T20"
    ODI = "ODI"
    TEST = "Test"

# Player class
class Player:
    def __init__(self, name, role, background):
        self.name = name
        self.role = role
        self.background = background
        self.age = random.randint(16, 22)
        self.skills = {
            "batting": random.randint(30, 70),
            "bowling": random.randint(30, 70),
            "fielding": random.randint(40, 80),
            "fitness": random.randint(50, 90),
            "mental": random.randint(40, 80)
        }
        self.experience = 0
        self.reputation = 1
        self.fatigue = 0
        self.injured = False
        self.career_stats = {
            "matches": 0,
            "runs": 0,
            "wickets": 0,
            "centuries": 0,
            "five_wkts": 0
        }
        self.traits = self.generate_traits()
        self.current_form = 0  # -10 to +10
        self.team = None
        self.career_choices = []
        
    def generate_traits(self):
        traits = {
            "confidence": random.randint(1, 10),
            "discipline": random.randint(1, 10),
            "aggression": random.randint(1, 10),
            "leadership": random.randint(1, 10)
        }
        # Background modifiers
        if self.background == Background.ACADEMY:
            traits["discipline"] = min(10, traits["discipline"] + 2)
        elif self.background == Background.STREET_CRICKET:
            traits["aggression"] = min(10, traits["aggression"] + 2)
        return traits
    
    def train(self, skill, intensity):
        if self.injured:
            return "Cannot train while injured"
        
        if skill not in self.skills:
            return "Invalid skill"
        
        improvement = random.randint(1, 3) * intensity
        self.skills[skill] = min(100, self.skills[skill] + improvement)
        
        # Risk of injury
        injury_risk = random.randint(1, 20)
        if injury_risk == 1 and intensity > 1:
            self.injured = True
            return f"Improved {skill} by {improvement} but suffered an injury!"
        
        self.fatigue += intensity
        return f"Improved {skill} by {improvement} points"
    
    def rest(self):
        self.fatigue = max(0, self.fatigue - 3)
        if self.injured and random.random() > 0.7:
            self.injured = False
            return "Recovered from injury and reduced fatigue"
        return "Reduced fatigue"
    
    def update_form(self, performance):
        # Performance from -5 (terrible) to +5 (excellent)
        self.current_form = max(-10, min(10, self.current_form + performance))
        
    def play_match(self, match_type):
        if self.injured:
            return None
        
        self.fatigue += match_type.value * 2  # TEST matches are more taxing
        
        # Base performance based on skills
        batting_perf = self.skills["batting"] / 10 + random.randint(-5, 5) + self.current_form
        bowling_perf = self.skills["bowling"] / 10 + random.randint(-5, 5) + self.current_form
        
        # Role modifiers
        if self.role == PlayerRole.BATTER:
            batting_perf += 5
        elif self.role == PlayerRole.BOWLER:
            bowling_perf += 5
        
        # Generate match stats
        runs = max(0, int(batting_perf * (5 if match_type == MatchType.T20 else 10)))
        wickets = min(10, int(bowling_perf * (0.5 if match_type == MatchType.TEST else 1)))
        
        # Update career stats
        self.career_stats["matches"] += 1
        self.career_stats["runs"] += runs
        self.career_stats["wickets"] += wickets
        
        if runs >= 100:
            self.career_stats["centuries"] += 1
        if wickets >= 5:
            self.career_stats["five_wkts"] += 1
        
        # Update experience and reputation
        self.experience += match_type.value
        self.reputation = min(10, self.reputation + (runs / 100) + (wickets / 5))
        
        # Update form
        perf_score = (runs / 50) + (wickets / 3) - 1  # 0 = average
        self.update_form(perf_score)
        
        return {
            "runs": runs,
            "wickets": wickets,
            "performance": perf_score
        }

# Team class
class Team:
    def __init__(self, name, level):
        self.name = name
        self.level = level  # 1-10
        self.players = []
        self.coach = {
            "strictness": random.randint(3, 8),
            "preference": random.choice(["youth", "experience", "balance"])
        }
    
    def add_player(self, player):
        player.team = self
        self.players.append(player)
    
    def select_squad(self, match_type):
        # Simple selection logic
        squad = sorted(
            self.players,
            key=lambda p: (p.skills["batting"] + p.skills["bowling"] + p.reputation),
            reverse=True
        )[:11]
        return squad

# Game World class
class CricketWorld:
    def __init__(self):
        self.teams = []
        self.current_date = datetime(2023, 1, 1)
        self.events = []
        self.news = []
        
    def advance_time(self, days=1):
        self.current_date += timedelta(days=days)
        
        # Random events
        if random.random() < 0.1:
            event = self.generate_event()
            self.events.append(event)
            self.news.append(f"{self.current_date.strftime('%Y-%m-%d')}: {event}")
    
    def generate_event(self):
        events = [
            "New T20 league announced",
            "Scandal rocks national team",
            "Pitch conditions debate heats up",
            "Legendary player retires",
            "New cricket technology unveiled"
        ]
        return random.choice(events)

# Main game class
class CricketCareerGame:
    def __init__(self):
        self.world = CricketWorld()
        self.player = None
        self.team = None
        
    def create_player(self):
        print("\n=== Create Your Cricketer ===")
        name = input("Enter player name: ")
        
        print("\nChoose your role:")
        for i, role in enumerate(PlayerRole):
            print(f"{i+1}. {role.value}")
        role_choice = int(input("Select (1-4): ")) - 1
        role = list(PlayerRole)[role_choice]
        
        print("\nChoose your background:")
        for i, bg in enumerate(Background):
            print(f"{i+1}. {bg.value}")
        bg_choice = int(input("Select (1-4): ")) - 1
        background = list(Background)[bg_choice]
        
        self.player = Player(name, role, background)
        
        # Starting team based on background
        team_level = {
            Background.STREET_CRICKET: 2,
            Background.CLUB: 3,
            Background.ACADEMY: 4,
            Background.UNIVERSITY: 3
        }[background]
        
        self.team = Team(f"{name}'s Starting Team", team_level)
        self.team.add_player(self.player)
        self.world.teams.append(self.team)
        
        print(f"\nWelcome, {name}! You begin your career at {self.team.name}")
    
    def main_menu(self):
        while True:
            print(f"\n=== {self.player.name}'s Career === "
                  f"(Day: {self.world.current_date.strftime('%Y-%m-%d')})")
            print(f"Age: {self.player.age} | Reputation: {self.player.reputation:.1f}/10")
            print(f"Form: {'↑' if self.player.current_form > 0 else '↓' if self.player.current_form < 0 else '→'} "
                  f"Fatigue: {self.player.fatigue}/10")
            if self.player.injured:
                print("!!! INJURED !!!")
            
            print("\n1. View Skills")
            print("2. Train")
            print("3. Rest")
            print("4. Play Match")
            print("5. View Stats")
            print("6. View News")
            print("7. Advance Time (7 days)")
            print("8. Quit")
            
            choice = input("Select option: ")
            
            if choice == "1":
                self.view_skills()
            elif choice == "2":
                self.train()
            elif choice == "3":
                print(self.player.rest())
                self.world.advance_time(3)
            elif choice == "4":
                self.play_match()
            elif choice == "5":
                self.view_stats()
            elif choice == "6":
                self.view_news()
            elif choice == "7":
                self.world.advance_time(7)
            elif choice == "8":
                break
    
    def view_skills(self):
        print("\n=== Skills ===")
        for skill, value in self.player.skills.items():
            print(f"{skill.capitalize()}: {value}/100")
        print("\n=== Traits ===")
        for trait, value in self.player.traits.items():
            print(f"{trait.capitalize()}: {value}/10")
    
    def train(self):
        print("\n=== Training ===")
        print("1. Batting")
        print("2. Bowling")
        print("3. Fielding")
        print("4. Fitness")
        print("5. Mental Toughness")
        skill_choice = input("Select skill to train: ")
        
        skills_map = {
            "1": "batting",
            "2": "bowling",
            "3": "fielding",
            "4": "fitness",
            "5": "mental"
        }
        
        if skill_choice in skills_map:
            intensity = int(input("Intensity (1-3): "))
            print(self.player.train(skills_map[skill_choice], intensity))
            self.world.advance_time(1)
    
    def play_match(self):
        if self.player.injured:
            print("Cannot play while injured!")
            return
        
        print("\n=== Match Type ===")
        for i, match_type in enumerate(MatchType):
            print(f"{i+1}. {match_type.value}")
        choice = int(input("Select match type: ")) - 1
        match_type = list(MatchType)[choice]
        
        result = self.player.play_match(match_type)
        self.world.advance_time(match_type.value)  # Days passed
        
        print(f"\nMatch Result - {match_type.value}:")
        print(f"Runs: {result['runs']}")
        if self.player.role != PlayerRole.BATTER:
            print(f"Wickets: {result['wickets']}")
        print(f"Performance: {'Good' if result['performance'] > 0 else 'Poor' if result['performance'] < 0 else 'Average'}")
        
        # Random news event
        if result['runs'] > 80 or result['wickets'] > 3:
            headline = f"{self.player.name} shines in {match_type.value} match!"
            self.world.news.append(f"{self.world.current_date.strftime('%Y-%m-%d')}: {headline}")
    
    def view_stats(self):
        print("\n=== Career Statistics ===")
        for stat, value in self.player.career_stats.items():
            print(f"{stat.replace('_', ' ').title()}: {value}")
    
    def view_news(self):
        print("\n=== Cricket World News ===")
        for news_item in self.world.news[-5:]:  # Show last 5 news items
            print(news_item)

# Start the game
if __name__ == "__main__":
    game = CricketCareerGame()
    game.create_player()
    game.main_menu()
