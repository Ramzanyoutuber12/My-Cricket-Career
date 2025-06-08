import random
import uuid
import json
import os
import datetime
import math # For math.ceil

# --- Player Class ---
class Player:
    def __init__(self, name, age, country, batting_hand, bowling_hand, bowling_type, is_user=False):
        self.name = name
        self.age = age
        self.country = country
        self.batting_hand = batting_hand
        self.bowling_hand = bowling_hand
        self.bowling_type = bowling_type
        self.is_user = is_user

        self.batting_skill = random.randint(30, 60)
        self.bowling_skill = random.randint(30, 60)
        self.fitness = 100
        self.form = 0
        self.experience = 0

        # Overall Career Stats
        self.matches_played = 0
        self.runs_scored = 0
        self.balls_faced = 0
        self.wickets_taken = 0
        self.balls_bowled = 0
        self.runs_conceded = 0
        self.fifties = 0
        self.centuries = 0
        self.five_wicket_hauls = 0
        self.player_of_the_match_awards = 0

        # Format-specific performance stats
        self.performance_stats = {
            'T20': self._new_format_stats(),
            'ODI': self._new_format_stats(),
            'Test': self._new_format_stats(),
        }
        self.trophies_won = {
            'T20 Cup': 0,
            'ODI Cup': 0,
            'Test Championship': 0,
        }

        # Temporary stats for current innings (reset at start of each innings)
        self.current_innings_runs = 0
        self.current_innings_balls_faced = 0
        self.current_innings_wickets = 0
        self.current_innings_runs_conceded = 0
        self.current_innings_balls_bowled = 0
        self.current_innings_status = 'NOT OUT' # e.g., 'OUT', 'NOT OUT', 'RETIRED'


    def _new_format_stats(self):
        return {
            'matches_played': 0,
            'runs_scored': 0,
            'balls_faced': 0,
            'wickets_taken': 0,
            'balls_bowled': 0,
            'runs_conceded': 0,
            'highest_score': 0,
            'fifties': 0,
            'centuries': 0,
            'five_wicket_hauls': 0,
            'best_batting_figures': {'runs': 0, 'balls_faced': 0},
            'best_bowling_figures': {'wickets': 0, 'runs': 0},
        }

    def display_profile(self):
        print(f"\n--- Player Profile: {self.name} ---")
        print(f"Age: {self.age}")
        print(f"Country: {self.country}")
        print(f"Batting Hand: {self.batting_hand}")
        print(f"Bowling Hand: {self.bowling_hand}")
        print(f"Bowling Type: {self.bowling_type}")
        print(f"Batting Skill: {self.batting_skill}/100")
        print(f"Bowling Skill: {self.bowling_skill}/100")
        print(f"Fitness: {self.fitness}%")
        print(f"Form: {self.form}")
        print(f"Experience: {self.experience}")
        print("\n--- Overall Career Stats ---")
        print(f"Matches Played: {self.matches_played}")
        print(f"Runs Scored: {self.runs_scored} (Balls Faced: {self.balls_faced})")
        # Calculate overall strike rate
        overall_sr = (self.runs_scored / self.balls_faced * 100) if self.balls_faced > 0 else 0
        print(f"Strike Rate: {overall_sr:.2f}")
        print(f"Wickets Taken: {self.wickets_taken} (Balls Bowled: {self.balls_bowled}, Runs Conceded: {self.runs_conceded})")
        print(f"Fifties: {self.fifties}")
        print(f"Centuries: {self.centuries}")
        print(f"5-Wicket Hauls: {self.five_wicket_hauls}")
        print(f"Player of the Match Awards: {self.player_of_the_match_awards}")
        print("--------------------")

    def display_performance_by_format(self):
        print(f"\n--- {self.name}'s Performance by Format ---")
        for format_name, stats in self.performance_stats.items():
            print(f"\n--- {format_name} Stats ---")
            print(f"Matches Played: {stats['matches_played']}")
            print(f"Total Runs: {stats['runs_scored']}")
            print(f"Total Wickets: {stats['wickets_taken']}")
            print(f"Highest Score: {stats['highest_score']} (Best Figures: {stats['best_batting_figures']['runs']} runs off {stats['best_batting_figures']['balls_faced']} balls)")
            strike_rate = (stats['runs_scored'] / stats['balls_faced'] * 100) if stats['balls_faced'] > 0 else 0
            print(f"Strike Rate: {strike_rate:.2f}")
            print(f"Fifties: {stats['fifties']}")
            print(f"Centuries: {stats['centuries']}")
            print(f"5-Wicket Hauls: {stats['five_wicket_hauls']} (Best Figures: {stats['best_bowling_figures']['wickets']}/{stats['best_bowling_figures']['runs']})")
            print("-------------------------")

        print("\n--- Trophies Won ---")
        for trophy_type, count in self.trophies_won.items():
            print(f"{trophy_type}: {count}")
        print("--------------------")


    def train(self, skill_type):
        if skill_type == 'batting':
            self.batting_skill = min(100, self.batting_skill + random.randint(1, 5))
            print(f"{self.name} trained batting. Batting skill is now {self.batting_skill}")
        elif skill_type == 'bowling':
            self.bowling_skill = min(100, self.bowling_skill + random.randint(1, 5))
            print(f"{self.name} trained bowling. Bowling skill is now {self.bowling_skill}")
        self.fitness = max(0, self.fitness - random.randint(2, 8))
        print(f"Fitness is now {self.fitness}%")

    def recover_fitness(self):
        self.fitness = min(100, self.fitness + random.randint(10, 25))
        print(f"{self.name} rested. Fitness is now {self.fitness}%")

    def get_effective_batting_skill(self):
        return max(1, min(100, self.batting_skill + self.form + (self.fitness - 50) // 10))

    def get_effective_bowling_skill(self):
        return max(1, min(100, self.bowling_skill + self.form + (self.fitness - 50) // 10))

    # --- Serialization Method ---
    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'country': self.country,
            'batting_hand': self.batting_hand,
            'bowling_hand': self.bowling_hand,
            'bowling_type': self.bowling_type,
            'is_user': self.is_user,
            'batting_skill': self.batting_skill,
            'bowling_skill': self.bowling_skill,
            'fitness': self.fitness,
            'form': self.form,
            'experience': self.experience,
            'matches_played': self.matches_played,
            'runs_scored': self.runs_scored,
            'balls_faced': self.balls_faced,
            'wickets_taken': self.wickets_taken,
            'balls_bowled': self.balls_bowled,
            'runs_conceded': self.runs_conceded,
            'fifties': self.fifties,
            'centuries': self.centuries,
            'five_wicket_hauls': self.five_wicket_hauls,
            'player_of_the_match_awards': self.player_of_the_match_awards,
            'performance_stats': self.performance_stats,
            'trophies_won': self.trophies_won
        }

    # --- Deserialization Static Method ---
    @staticmethod
    def from_dict(data):
        player = Player(
            data['name'], data['age'], data['country'],
            data['batting_hand'], data['bowling_hand'], data['bowling_type'],
            data['is_user']
        )
        player.batting_skill = data['batting_skill']
        player.bowling_skill = data['bowling_skill']
        player.fitness = data['fitness']
        player.form = data['form']
        player.experience = data['experience']
        player.matches_played = data['matches_played']
        player.runs_scored = data['runs_scored']
        player.balls_faced = data['balls_faced']
        player.wickets_taken = data['wickets_taken']
        player.balls_bowled = data['balls_bowled']
        player.runs_conceded = data['runs_conceded']
        player.fifties = data['fifties']
        player.centuries = data['centuries']
        player.five_wicket_hauls = data['five_wicket_hauls']
        player.player_of_the_match_awards = data['player_of_the_match_awards']
        # Load new format-specific stats, handling potential missing key for old saves
        player.performance_stats = data.get('performance_stats', player._new_format_stats())
        # Ensure all formats exist if loading from old save
        for f in ['T20', 'ODI', 'Test']:
            if f not in player.performance_stats:
                player.performance_stats[f] = player._new_format_stats()
            # Ensure new best figures keys exist if loading from old save (nested dictionary)
            if 'best_batting_figures' not in player.performance_stats[f]:
                player.performance_stats[f]['best_batting_figures'] = {'runs': 0, 'balls_faced': 0}
            if 'best_bowling_figures' not in player.performance_stats[f]:
                player.performance_stats[f]['best_bowling_figures'] = {'wickets': 0, 'runs': 0}

        player.trophies_won = data.get('trophies_won', {
            'T20 Cup': 0,
            'ODI Cup': 0,
            'Test Championship': 0,
        })
        return player

# --- Team Class ---
class Team:
    def __init__(self, name, players=None, is_user_team=False, team_id=None):
        self.id = team_id if team_id else str(uuid.uuid4())[:8] # Unique ID for saving/loading
        self.name = name
        self.players = players if players is not None else []
        self.is_user_team = is_user_team
        self.points = 0
        self.matches_played = 0
        self.matches_won = 0
        self.matches_lost = 0
        self.matches_drawn = 0
        self.net_run_rate = 0.0

    def add_player(self, player):
        self.players.append(player)

    def generate_random_squad(self, num_players=11):
        countries = ["Australia", "India", "England", "South Africa", "New Zealand", "Pakistan", "Sri Lanka", "West Indies"]
        batting_hands = ['Left', 'Right']
        bowling_hands = ['Left', 'Right']
        bowling_types = ['Fast', 'Medium Fast', 'Slow', 'Off Spin', 'Leg Spin', 'Googly', 'Offbreak']

        for i in range(num_players):
            name = f"AI Player {i+1} {self.name}"
            age = random.randint(20, 35)
            country = self.name if self.name in countries else random.choice(countries)
            bat_hand = random.choice(batting_hands)
            bowl_hand = random.choice(bowling_hands)
            bowl_type = random.choice(bowling_types)
            self.add_player(Player(name, age, country, bat_hand, bowl_hand, bowl_type, is_user=False))

    def display_squad(self):
        print(f"\n--- {self.name} Squad ---")
        for i, player in enumerate(self.players):
            print(f"{i+1}. {player.name} ({player.age}) - Bat: {player.batting_hand}, Bowl: {player.bowling_type}")
        print("------------------------")

    def get_batsmen(self):
        return self.players

    def get_bowlers(self):
        return self.players

    # --- Serialization Method ---
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'players': [player.to_dict() for player in self.players],
            'is_user_team': self.is_user_team,
            'points': self.points,
            'matches_played': self.matches_played,
            'matches_won': self.matches_won,
            'matches_lost': self.matches_lost,
            'matches_drawn': self.matches_drawn,
            'net_run_rate': self.net_run_rate
        }

    # --- Deserialization Static Method ---
    @staticmethod
    def from_dict(data):
        players = [Player.from_dict(p_data) for p_data in data['players']]
        team = Team(
            data['name'], players, data['is_user_team'], data['id']
        )
        team.points = data['points']
        team.matches_played = data['matches_played']
        team.matches_won = data['matches_won']
        team.matches_lost = data['matches_lost']
        team.matches_drawn = data['matches_drawn']
        team.net_run_rate = data['net_run_rate']
        return team

# --- Match Class ---
class Match:
    def __init__(self, team1, team2, match_type):
        self.team1 = team1
        self.team2 = team2
        self.match_type = match_type
        self.team1_score = {'runs': 0, 'wickets': 0, 'overs': 0}
        self.team2_score = {'runs': 0, 'wickets': 0, 'overs': 0}
        self.winner = None
        self.is_drawn = False
        self.super_over_needed = False

        self.overs_per_innings = {
            'T20': 20,
            'ODI': 50,
            'Test': 'Unlimited' # Test matches will be simulated over multiple "sessions" or days
        }

    def _display_scoreboard(self, current_runs, wickets_fallen, balls_bowled, target, current_batsman_obj, non_striker_obj, current_over_details):
        overs_completed = balls_bowled // 6
        balls_in_current_over = balls_bowled % 6
        print("\n--- Scoreboard ---")
        print(f"Score: {current_runs}/{wickets_fallen} (Overs: {overs_completed}.{balls_in_current_over}{f' | Target: {target}' if target > 0 else ''})")
        print(f"Current Bat: {current_batsman_obj.name} - {current_batsman_obj.current_innings_runs} runs ({current_batsman_obj.current_innings_balls_faced} balls)")
        print(f"Non-Striker: {non_striker_obj.name} - {non_striker_obj.current_innings_runs} runs ({non_striker_obj.current_innings_balls_faced} balls)")
        if current_over_details:
             print(f"Last Over: {current_over_details}")
        print("------------------")

    def _user_batting_input(self, user_player, bowler_skill, current_runs, wickets_fallen, balls_bowled, target, non_striker_obj):
        print(f"\n--- Your Turn to Bat: {user_player.name} ({user_player.current_innings_runs} runs, {user_player.current_innings_balls_faced} balls) ---")
        self.runs_this_over = 0 # Track runs for the current over
        self.wickets_this_over = 0 # Track wickets for the current over
        self.balls_this_over = 0 # Track balls for the current over

        while self.balls_this_over < 6 and wickets_fallen < 10:
            if target > 0 and current_runs >= target:
                break

            self._display_scoreboard(current_runs, wickets_fallen, balls_bowled, target, user_player, non_striker_obj, f"{self.runs_this_over} runs, {self.wickets_this_over} wickets")

            print("\nChoose your shot:")
            print("1. Swipe (Play a shot: Straight, Left, Right, Defensive)")
            print("2. Run (Attempt a quick single if ball is fielded close)")
            print("0. Retire (End your innings - not recommended unless stuck!)") # For testing/quitting
            
            action = input("Enter your choice: ")

            if action == '1':
                print("Swipe Direction:")
                print("1. Straight (Forward Defense, Straight Drive)")
                print("2. Left (Leg Side, Pull, Hook)")
                print("3. Right (Off Side, Cut, Cover Drive)")
                print("4. Defensive (Block, Leave)")
                swipe_choice = input("Enter swipe choice: ")

                if swipe_choice == '1':
                    shot_type = 'straight'
                elif swipe_choice == '2':
                    shot_type = 'left'
                elif swipe_choice == '3':
                    shot_type = 'right'
                elif swipe_choice == '4':
                    shot_type = 'defensive'
                else:
                    print("Invalid swipe choice. Playing defensive.")
                    shot_type = 'defensive'

                runs_this_ball = 0
                is_wicket = False

                # Simulate outcome based on batting skill, bowling skill, and shot choice
                batting_success_chance = user_player.get_effective_batting_skill() / 100
                bowling_success_chance = bowler_skill / 100

                # Chance of a wicket
                wicket_prob = (bowling_success_chance * (1 - batting_success_chance) * 0.15) # Increased difficulty for user
                if random.random() < wicket_prob:
                    is_wicket = True
                else:
                    # Determine runs
                    if shot_type == 'defensive':
                        runs_this_ball = random.choice([0, 0, 0, 1]) # Mostly dots/singles
                        if random.random() < 0.1: # Small chance of boundary on defensive
                            runs_this_ball = random.choice([0,0,0,0,0,0,4])
                    elif batting_success_chance > random.random(): # Good shot
                        if random.random() < 0.2: # Boundary chance
                            runs_this_ball = random.choice([4, 6])
                        else:
                            runs_this_ball = random.choice([0, 1, 2, 3])
                    else: # Poorly timed/executed shot
                        runs_this_ball = random.choice([0, 0, 1])

                user_player.current_innings_balls_faced += 1
                self.balls_this_over += 1

                if is_wicket:
                    wickets_fallen += 1
                    user_player.current_innings_status = 'OUT'
                    print(f"You are OUT! {user_player.name} departs after scoring {user_player.current_innings_runs} runs.")
                    self.wickets_this_over += 1
                    return runs_this_ball, True, wickets_fallen # Runs this ball, is_out, updated wickets
                else:
                    current_runs += runs_this_ball
                    user_player.current_innings_runs += runs_this_ball
                    self.runs_this_over += runs_this_ball
                    print(f"You scored {runs_this_ball} runs.")
                    return runs_this_ball, False, wickets_fallen

            elif action == '2':
                # Attempt a run, higher risk if opposition skill is high
                risk = (bowler_skill / 100) * 0.3 # Higher risk for better bowlers
                if random.random() < risk:
                    print("Run out attempt! Oh no, you are run out!")
                    is_wicket = True
                    wickets_fallen += 1
                    user_player.current_innings_balls_faced += 1 # Still counts as a ball faced
                    self.balls_this_over += 1
                    self.wickets_this_over += 1
                    user_player.current_innings_status = 'OUT'
                    return 0, True, wickets_fallen
                else:
                    runs_this_ball = 1
                    current_runs += runs_this_ball
                    user_player.current_innings_runs += runs_this_ball
                    user_player.current_innings_balls_faced += 1
                    self.balls_this_over += 1
                    self.runs_this_over += runs_this_ball
                    print(f"You took a quick single!")
                    # In a real game, you'd swap strikers here. For simplicity, we assume AI handles it.
                    return runs_this_ball, False, wickets_fallen

            elif action == '0':
                print(f"{user_player.name} has retired hurt/out. Current score: {user_player.current_innings_runs}")
                user_player.current_innings_status = 'RETIRED'
                return 0, True, wickets_fallen # Essentially out for simulation purposes
            else:
                print("Invalid action. Please choose again.")
                # Don't increment balls faced/bowled for invalid input
                continue
        return 0, False, wickets_fallen # If loop ends, user is not out

    def _user_bowling_input(self, user_player, batsman_skill, current_runs, wickets_fallen, balls_bowled, target, current_batsman_obj, non_striker_obj):
        print(f"\n--- Your Turn to Bowl: {user_player.name} ({user_player.current_innings_wickets} wickets, {user_player.current_innings_runs_conceded} runs) ---")
        self.runs_this_over = 0
        self.wickets_this_over = 0
        self.balls_this_over = 0

        # AI Batsmen for current over
        current_batsman = current_batsman_obj
        # Non-striker is passed directly for display

        while self.balls_this_over < 6 and wickets_fallen < 10:
            if target > 0 and current_runs >= target:
                break
            self._display_scoreboard(current_runs, wickets_fallen, balls_bowled, target, current_batsman, non_striker_obj, f"{self.runs_this_over} runs, {self.wickets_this_over} wickets")

            print("\nChoose your delivery:")
            print("1. Pitch (Full, Good Length, Short)")
            print("2. Type (Fast, Medium, Spin)") # This is mostly for user guidance, actual type from player.bowling_type
            print("3. Variation (e.g., Yorker, Bouncer, Leg Break, Googly, Off Break, Doosra, Arm Ball)")

            # Get pitch
            while True:
                pitch_choice = input("Where do you want to pitch the ball? (1. Full, 2. Good Length, 3. Short): ")
                if pitch_choice == '1': pitch = 'full'
                elif pitch_choice == '2': pitch = 'good length'
                elif pitch_choice == '3': pitch = 'short'
                else: print("Invalid pitch. Try again."); continue
                break

            # Get bowling type (based on player's bowling_type, but allow user choices)
            selected_bowl_type = user_player.bowling_type
            if 'Spin' in selected_bowl_type: # User is a spinner
                print("Choose spin type (1. Stock, 2. Googly/Doosra, 3. Top Spin/Arm Ball):")
                spin_type_choice = input("Enter choice: ")
                if user_player.bowling_hand == 'Right': # Right-arm spinner
                    if 'Leg Spin' in selected_bowl_type: # Right-arm Leg Spinner
                        if spin_type_choice == '1': variation = 'leg_break' # Away from RHB
                        elif spin_type_choice == '2': variation = 'googly' # Into RHB
                        elif spin_type_choice == '3': variation = 'top_spin' # Skids on
                        else: print("Invalid variation. Defaulting to Leg Break."); variation = 'leg_break'
                    elif 'Off Spin' in selected_bowl_type: # Right-arm Off Spinner
                        if spin_type_choice == '1': variation = 'off_break' # Into RHB
                        elif spin_type_choice == '2': variation = 'doosra' # Away from RHB (simplified)
                        elif spin_type_choice == '3': variation = 'arm_ball' # Skids on
                        else: print("Invalid variation. Defaulting to Off Break."); variation = 'off_break'
                    else: # Other spin types (e.g., Googly, Offbreak directly selected)
                        variation = 'stock_spin' # General stock spin
                else: # Left-arm spinner (wrist or orthodox)
                    if 'Leg Spin' in selected_bowl_type or 'Chinaman' in selected_bowl_type: # Left-arm Wrist Spin / Chinaman (turns away from RHB)
                        if spin_type_choice == '1': variation = 'chinaman' # Away from RHB
                        elif spin_type_choice == '2': variation = 'googly' # Into RHB
                        elif spin_type_choice == '3': variation = 'top_spin' # Skids on
                        else: print("Invalid variation. Defaulting to Chinaman."); variation = 'chinaman'
                    elif 'Off Spin' in selected_bowl_type or 'Orthodox' in selected_bowl_type: # Left-arm Orthodox (turns into RHB)
                        if spin_type_choice == '1': variation = 'left_arm_orthodox' # Into RHB
                        elif spin_type_choice == '2': variation = 'arm_ball' # Skids on/straightens
                        else: print("Invalid variation. Defaulting to Left-arm Orthodox."); variation = 'left_arm_orthodox'
                    else:
                        variation = 'stock_spin' # General stock spin
            else: # User is a pace bowler
                print("Choose pace variation (1. Fast, 2. Medium, 3. Yorker, 4. Bouncer, 5. Slower Ball):")
                pace_type_choice = input("Enter choice: ")
                if pace_type_choice == '1': variation = 'fast'
                elif pace_type_choice == '2': variation = 'medium'
                elif pace_type_choice == '3': variation = 'yorker'
                elif pace_type_choice == '4': variation = 'bouncer'
                elif pace_type_choice == '5': variation = 'slower_ball'
                else: print("Invalid variation. Defaulting to Fast."); variation = 'fast'

            runs_this_ball = 0
            is_wicket = False

            # Bowling outcome based on skill and variation
            bowling_success_chance = user_player.get_effective_bowling_skill() / 100
            wicket_prob = (bowling_success_chance * (1 - batsman_skill / 100) * 0.2) # Adjusted difficulty for user
            if pitch == 'yorker' or pitch == 'bouncer': # Yorker/Bouncer are technically pitches too
                # Increase wicket chance for yorker/bouncer slightly if bowler is good
                if user_player.bowling_skill > 60: wicket_prob *= 1.2

            if random.random() < wicket_prob:
                is_wicket = True
            else:
                # Runs conceded based on pitch and variation
                if pitch == 'full' or variation == 'yorker': # Full/Yorker can go for 4s or be dot
                    runs_this_ball = random.choice([0, 0, 0, 1, 2, 4])
                elif pitch == 'good length' or variation == 'stock_spin' or variation == 'fast': # Good length is often dot/single
                    runs_this_ball = random.choice([0, 0, 1, 1, 2])
                elif pitch == 'short' or variation == 'bouncer': # Short/Bouncer can go for 6 or be dot
                    runs_this_ball = random.choice([0, 0, 1, 4, 6])
                else: # Other variations might have specific run outcomes
                    runs_this_ball = random.choice([0, 1, 2])


            user_player.current_innings_balls_bowled += 1
            user_player.current_innings_runs_conceded += runs_this_ball
            self.balls_this_over += 1
            self.runs_this_over += runs_this_ball

            if is_wicket:
                wickets_fallen += 1
                user_player.current_innings_wickets += 1
                self.wickets_this_over += 1
                print(f"OUT! {current_batsman.name} is dismissed by {user_player.name}! Score: {current_runs}/{wickets_fallen}")
                return 0, True, wickets_fallen # Runs this ball, is_out, updated wickets
            else:
                current_runs += runs_this_ball
                print(f"{runs_this_ball} runs conceded by {user_player.name}. Score: {current_runs}/{wickets_fallen}")
                return runs_this_ball, False, wickets_fallen

        return 0, False, wickets_fallen


    def _simulate_innings(self, batting_team, bowling_team, overs_limit, user_player_global_ref, target_score=0):
        current_runs = 0
        wickets_fallen = 0
        balls_bowled = 0
        
        innings_player_performance = {} # {player_obj: {'runs': 0, 'balls_faced': 0, 'wickets': 0, 'runs_conceded': 0, 'balls_bowled': 0}}
        
        # Reset current innings stats for all players before the innings starts
        for p in batting_team.players + bowling_team.players:
            p.current_innings_runs = 0
            p.current_innings_balls_faced = 0
            p.current_innings_wickets = 0
            p.current_innings_runs_conceded = 0
            p.current_innings_balls_bowled = 0
            p.current_innings_status = 'NOT OUT' # For tracking if user player is out or retired

        print(f"\n--- {batting_team.name} Batting ({'Unlimited Overs' if isinstance(overs_limit, str) else f'Overs: {overs_limit}'}{f' | Target: {target_score}' if target_score > 0 else ''}) ---")

        batting_order = list(batting_team.players)
        random.shuffle(batting_order)

        user_player_is_batting_team = batting_team.is_user_team and user_player_global_ref in batting_team.players
        user_player_is_bowling_team = bowling_team.is_user_team and user_player_global_ref in bowling_team.players

        # Ensure user player is present in the batting_order list if they are in the batting team
        user_player_batting_instance = None
        if user_player_is_batting_team:
            user_player_idx = next((i for i, p in enumerate(batting_order) if p.is_user), -1)
            if user_player_idx != -1:
                # Move user player to a more common batting position (e.g., 3rd or 4th)
                if user_player_idx > 3 and len(batting_order) >= 4:
                    user_player_batting_instance = batting_order.pop(user_player_idx)
                    batting_order.insert(3, user_player_batting_instance)
                elif user_player_idx != 0: # If not already opening, put them as opener if fewer than 4 players
                    user_player_batting_instance = batting_order.pop(user_player_idx)
                    batting_order.insert(0, user_player_batting_instance)
                else: # user player is already opener (idx 0)
                    user_player_batting_instance = batting_order[user_player_idx]
            else: # User player not in batting order, should not happen if added to user team
                user_player_is_batting_team = False # Cannot bat as user

        # Initialize current batsmen (AI controlled unless user is one of them)
        striker_index = 0
        non_striker_index = 1
        
        current_striker = batting_order[striker_index]
        current_non_striker = batting_order[non_striker_index]
        
        # Display stats for the first two batsmen coming in
        print(f"\n--- New Batsman: {current_striker.name} ---")
        format_key = self.match_type
        print(f"Career {format_key} Runs: {current_striker.performance_stats[format_key]['runs_scored']} (Matches: {current_striker.performance_stats[format_key]['matches_played']})")
        
        print(f"\n--- New Batsman: {current_non_striker.name} ---")
        print(f"Career {format_key} Runs: {current_non_striker.performance_stats[format_key]['runs_scored']} (Matches: {current_non_striker.performance_stats[format_key]['matches_played']})")

        while wickets_fallen < 10 and (isinstance(overs_limit, str) or balls_bowled < overs_limit * 6):
            if target_score > 0 and current_runs >= target_score:
                print(f"{batting_team.name} reached the target!")
                break
            if striker_index >= len(batting_order):
                print(f"All batsmen out or no more batsmen to play for {batting_team.name}.")
                break
            
            # Select bowler for the over
            bowler = random.choice([p for p in bowling_team.get_bowlers() if p != current_striker and p != current_non_striker]) # Ensure bowler is not one of the batsmen
            if user_player_is_bowling_team and user_player_global_ref.name == bowler.name:
                active_bowler = user_player_global_ref # Use the user's actual player object if they are bowling
            else:
                active_bowler = bowler # AI bowler

            over_runs = 0
            over_wickets = 0
            
            # Simulate each ball of the over
            for ball in range(6):
                if target_score > 0 and current_runs >= target_score:
                    break
                if wickets_fallen >= 10:
                    break
                if striker_index >= len(batting_order):
                    break

                current_striker = batting_order[striker_index] # Update striker at start of each ball
                # Ensure the actual user_player_global_ref is used if it's their turn to bat
                if user_player_is_batting_team and current_striker.is_user:
                    current_striker = user_player_global_ref

                # User interaction for batting or bowling
                if user_player_is_batting_team and current_striker.is_user:
                    runs_this_ball, is_wicket, updated_wickets = self._user_batting_input(
                        current_striker, active_bowler.get_effective_bowling_skill(),
                        current_runs, wickets_fallen, balls_bowled, target_score, current_non_striker
                    )
                    wickets_fallen = updated_wickets
                elif user_player_is_bowling_team and active_bowler.is_user:
                     runs_this_ball, is_wicket, updated_wickets = self._user_bowling_input(
                        active_bowler, current_striker.get_effective_batting_skill(),
                        current_runs, wickets_fallen, balls_bowled, target_score, current_striker, current_non_striker
                    )
                     wickets_fallen = updated_wickets
                else: # AI vs AI simulation
                    runs_this_ball = 0
                    is_wicket = False

                    wicket_chance = (active_bowler.get_effective_bowling_skill() / 100) * (1 - current_striker.get_effective_batting_skill() / 100) * 0.1
                    if random.random() < wicket_chance:
                        is_wicket = True
                    else:
                        runs_this_ball = random.choice([0, 1, 1, 2, 4, 6])

                    current_striker.current_innings_runs += runs_this_ball
                    current_striker.current_innings_balls_faced += 1
                    active_bowler.current_innings_runs_conceded += runs_this_ball
                    active_bowler.current_innings_balls_bowled += 1
                    if is_wicket:
                        active_bowler.current_innings_wickets += 1

                current_runs += runs_this_ball
                balls_bowled += 1
                over_runs += runs_this_ball

                if is_wicket:
                    over_wickets += 1
                    print(f"Ball {balls_bowled % 6 if balls_bowled % 6 != 0 else 6}/{balls_bowled // 6 + 1} - {current_striker.name} OUT! Score: {current_runs}/{wickets_fallen}")
                    current_striker.current_innings_status = 'OUT' # Mark player as out
                    striker_index += 1
                    if striker_index < len(batting_order):
                        current_striker = batting_order[striker_index]
                        print(f"\n--- New Batsman: {current_striker.name} ---")
                        # Display career stats for the new batsman
                        print(f"Career {format_key} Runs: {current_striker.performance_stats[format_key]['runs_scored']} (Matches: {current_striker.performance_stats[format_key]['matches_played']})")

                # If odd runs taken or a wicket, swap strikers (for AI simulation)
                # For user batting, the _user_batting_input will handle runs and not swap automatically
                if (runs_this_ball % 2 != 0 and not is_wicket and not (user_player_is_batting_team and current_striker.is_user)) or (is_wicket and (user_player_is_batting_team and current_striker.is_user)):
                    # Swap current striker and non-striker for AI
                    temp = current_striker
                    current_striker = current_non_striker
                    current_non_striker = temp
                    striker_index = batting_order.index(current_striker) # Update striker index to reflect swap
                    non_striker_index = batting_order.index(current_non_striker)

                # End of ball updates for AI
                if not user_player_is_batting_team and not user_player_is_bowling_team:
                    print(f"Ball {balls_bowled % 6 if balls_bowled % 6 != 0 else 6}/{balls_bowled // 6 + 1} - {runs_this_ball} runs. Score: {current_runs}/{wickets_fallen}")
            
            # After each over (or innings end)
            if balls_bowled % 6 == 0 and balls_bowled > 0:
                self._display_scoreboard(current_runs, wickets_fallen, balls_bowled, target_score, current_striker, current_non_striker, f"{over_runs} runs, {over_wickets} wickets in over")
                # Swap strikers at the end of every over
                temp = current_striker
                current_striker = current_non_striker
                current_non_striker = temp
                striker_index = batting_order.index(current_striker)
                non_striker_index = batting_order.index(current_non_striker)


        innings_overs = balls_bowled / 6
        print(f"\n--- {batting_team.name} Innings Finished ---")
        print(f"Score: {current_runs}/{wickets_fallen} in {innings_overs:.1f} overs")

        # Compile final player performance for this innings
        for player in batting_team.players:
            if player.current_innings_balls_faced > 0 or player.current_innings_wickets > 0: # Only include if they played
                innings_player_performance[player.name] = {
                    'runs': player.current_innings_runs,
                    'balls_faced': player.current_innings_balls_faced,
                    'wickets': player.current_innings_wickets,
                    'runs_conceded': player.current_innings_runs_conceded,
                    'balls_bowled': player.current_innings_balls_bowled,
                    'status': player.current_innings_status # Track if user player retired or out
                }
        for player in bowling_team.players:
             if player.current_innings_balls_bowled > 0 or player.current_innings_wickets > 0: # Only include if they played
                innings_player_performance[player.name] = {
                    'runs': player.current_innings_runs, # This would be 0 for a bowler's batting stats
                    'balls_faced': player.current_innings_balls_faced, # This would be 0 for a bowler's batting stats
                    'wickets': player.current_innings_wickets,
                    'runs_conceded': player.current_innings_runs_conceded,
                    'balls_bowled': player.current_innings_balls_bowled,
                    'status': player.current_innings_status
                }


        return {'runs': current_runs, 'wickets': wickets_fallen, 'overs': innings_overs, 'player_performance': innings_player_performance}

    def simulate_super_over(self, team1, team2, user_player_global_ref):
        print("\n--- SUPER OVER! ---")
        print(f"{team1.name} will bat first in the Super Over.")

        team1_so_score = self._simulate_innings(team1, team2, 1, user_player_global_ref) # 1 over
        print(f"{team1.name} Super Over Score: {team1_so_score['runs']}/{team1_so_score['wickets']}")
        target_so = team1_so_score['runs'] + 1

        print(f"\n{team2.name} needs {target_so} to win in the Super Over.")
        team2_so_score = self._simulate_innings(team2, team1, 1, user_player_global_ref, target_so) # 1 over
        print(f"{team2.name} Super Over Score: {team2_so_score['runs']}/{team2_so_score['wickets']}")

        if team2_so_score['runs'] >= target_so:
            print(f"\n--- {team2.name} wins the Super Over! ---")
            return team2
        elif team1_so_score['runs'] > team2_so_score['runs']:
            print(f"\n--- {team1.name} wins the Super Over! ---")
            return team1
        else:
            print("\n--- Super Over is also a DRAW! Another Super Over will be played. ---")
            return self.simulate_super_over(team1, team2, user_player_global_ref)

    def play_match(self, user_player_global_ref):
        print(f"\n--- Match Start: {self.team1.name} vs {self.team2.name} ({self.match_type}) ---")

        toss_winner_team = random.choice([self.team1, self.team2])
        print(f"Toss won by {toss_winner_team.name}.")

        batting_first = None
        bowling_first = None

        if toss_winner_team.is_user_team:
            while True:
                toss_decision = input("You won the toss. Do you want to (bat/bowl)? ").lower()
                if toss_decision == 'bat':
                    batting_first = self.team1 if self.team1.is_user_team else self.team2
                    bowling_first = self.team2 if self.team1.is_user_team else self.team1
                    break
                elif toss_decision == 'bowl':
                    batting_first = self.team2 if self.team1.is_user_team else self.team1
                    bowling_first = self.team1 if self.team1.is_user_team else self.team2
                    break
                else:
                    print("Invalid choice. Please enter 'bat' or 'bowl'.")
        else:
            if random.choice([True, False]):
                batting_first = toss_winner_team
                bowling_first = self.team1 if toss_winner_team != self.team1 else self.team2
                print(f"{toss_winner_team.name} elected to bat.")
            else:
                batting_first = self.team2 if self.team1.is_user_team else self.team1
                bowling_first = toss_winner_team
                print(f"{toss_winner_team.name} elected to bowl.")

        # Innings 1
        print(f"\n--- First Innings ---")
        innings1_result = self._simulate_innings(batting_first, bowling_first, self.overs_per_innings[self.match_type], user_player_global_ref)
        self.team1_score = {'runs': innings1_result['runs'], 'wickets': innings1_result['wickets'], 'overs': innings1_result['overs']}
        target = self.team1_score['runs'] + 1

        # Innings 2
        print(f"\n--- Second Innings ---")
        print(f"{bowling_first.name} needs {target} runs to win.")
        innings2_result = self._simulate_innings(bowling_first, batting_first, self.overs_per_innings[self.match_type], user_player_global_ref, target)
        self.team2_score = {'runs': innings2_result['runs'], 'wickets': innings2_result['wickets'], 'overs': innings2_result['overs']}

        # Determine Match Result
        if self.team2_score['runs'] >= target:
            self.winner = bowling_first
            print(f"\n--- {self.winner.name} wins the match! ---")
        elif self.team1_score['runs'] > self.team2_score['runs']:
            self.winner = batting_first
            print(f"\n--- {self.winner.name} wins the match! ---")
        elif self.team1_score['runs'] == self.team2_score['runs']:
            if self.match_type != 'Test':
                self.super_over_needed = True
                print("\n--- Match Tied! Initiating Super Over. ---")
                super_over_winner = self.simulate_super_over(self.team1, self.team2, user_player_global_ref)
                self.winner = super_over_winner
                print(f"\n--- {self.winner.name} wins after Super Over! ---")
            else:
                self.is_drawn = True
                print("\n--- Test Match Drawn! ---")
        else:
            self.winner = None
            self.is_drawn = True

        # Update player fitness and form for ALL players in both teams after the match
        for team in [self.team1, self.team2]:
            for player in team.players:
                player.matches_played += 1
                player.fitness = max(0, player.fitness - random.randint(5, 15)) # Reduce fitness
                if self.winner == team: # Winner team players get form boost
                    player.form = min(10, player.form + random.randint(0, 2))
                elif self.winner and self.winner != team: # Loser team players get form drop
                    player.form = max(-10, player.form - random.randint(0, 2))
                else: # Draw, slight random form change
                    player.form += random.randint(-1, 1)
                    player.form = max(-10, min(10, player.form))

        # --- Update format-specific stats for relevant players ---
        format_key = self.match_type # 'T20', 'ODI', 'Test'
        all_players_in_match = self.team1.players + self.team2.players

        for player_obj in all_players_in_match:
            # Get performance for this player from both innings if they participated
            # Use .get() with a default empty dict to avoid KeyError if player didn't participate in an innings
            p_i1_batting = innings1_result['player_performance'].get(player_obj.name, {})
            p_i2_batting = innings2_result['player_performance'].get(player_obj.name, {})

            player_innings_runs = p_i1_batting.get('runs', 0) + p_i2_batting.get('runs', 0)
            player_innings_balls_faced = p_i1_batting.get('balls_faced', 0) + p_i2_batting.get('balls_faced', 0)

            p_i1_bowling = innings1_result['player_performance'].get(player_obj.name, {})
            p_i2_bowling = innings2_result['player_performance'].get(player_obj.name, {})

            player_innings_wickets = p_i1_bowling.get('wickets', 0) + p_i2_bowling.get('wickets', 0)
            player_innings_runs_conceded = p_i1_bowling.get('runs_conceded', 0) + p_i2_bowling.get('runs_conceded', 0)
            player_innings_balls_bowled = p_i1_bowling.get('balls_bowled', 0) + p_i2_bowling.get('balls_bowled', 0)

            # Update format-specific stats
            if format_key in player_obj.performance_stats:
                stats = player_obj.performance_stats[format_key]
                stats['matches_played'] += 1
                stats['runs_scored'] += player_innings_runs
                stats['balls_faced'] += player_innings_balls_faced
                stats['wickets_taken'] += player_innings_wickets
                stats['runs_conceded'] += player_innings_runs_conceded
                stats['balls_bowled'] += player_innings_balls_bowled

                # Update highest score (batting)
                if player_innings_runs > stats['highest_score']:
                    stats['highest_score'] = player_innings_runs
                # Update best batting figures
                if player_innings_runs > stats['best_batting_figures']['runs'] or \
                   (player_innings_runs == stats['best_batting_figures']['runs'] and player_innings_balls_faced < stats['best_batting_figures']['balls_faced']):
                    stats['best_batting_figures'] = {'runs': player_innings_runs, 'balls_faced': player_innings_balls_faced}

                # Update best bowling figures
                if player_innings_wickets > stats['best_bowling_figures']['wickets'] or \
                   (player_innings_wickets == stats['best_bowling_figures']['wickets'] and player_innings_runs_conceded < stats['best_bowling_figures']['runs']):
                    stats['best_bowling_figures'] = {'wickets': player_innings_wickets, 'runs': player_innings_runs_conceded}


                # Update 50s/100s/200s logic for batting performance in this match
                temp_runs = player_innings_runs # Use a temporary variable for calculation
                if temp_runs >= 50:
                    while temp_runs >= 100:
                        stats['centuries'] += 1
                        temp_runs -= 100
                    if temp_runs >= 50:
                        stats['fifties'] += 1


                # Update 5-wicket hauls
                if player_innings_wickets >= 5:
                    stats['five_wicket_hauls'] += 1


        # Check if user player got Player of the Match (random for simplicity)
        if user_player_global_ref.is_user:
            # We need to find the specific user_player object instance from the teams to update it
            actual_user_player_in_match = next((p for p in all_players_in_match if p.is_user), None)
            if actual_user_player_in_match and random.random() < 0.2: # 20% chance
                actual_user_player_in_match.player_of_the_match_awards += 1
                print(f"\n{actual_user_player_in_match.name} has been awarded Player of the Match!")

        return self.winner, self.is_drawn

# --- Tournament Class ---
class Tournament:
    def __init__(self, name, tournament_type, teams, current_fixture_index=0, standings=None, tourney_id=None):
        self.id = tourney_id if tourney_id else str(uuid.uuid4())[:8]
        self.name = name
        self.tournament_type = tournament_type
        self.teams = teams # Store actual team objects here
        self.current_fixture_index = current_fixture_index
        self.standings = standings if standings else {team.id: {'name': team.name, 'points': 0, 'played': 0, 'won': 0, 'lost': 0, 'drawn': 0} for team in teams}
        if not self.fixtures: # Generate fixtures only if not loading from existing data
            self._generate_fixtures()

    @property # Use property to generate fixtures dynamically based on current teams
    def fixtures(self):
        _fixtures = []
        if len(self.teams) >= 2:
            sorted_teams = sorted(self.teams, key=lambda t: t.name) # Ensure consistent fixture generation
            for i in range(len(sorted_teams)):
                for j in range(i + 1, len(sorted_teams)):
                    team1 = sorted_teams[i]
                    team2 = sorted_teams[j]
                    _fixtures.append({'team1_id': team1.id, 'team2_id': team2.id, 'match_type': self.tournament_type.split(' ')[0]})
        return _fixtures


    def _generate_fixtures(self):
        # This is primarily for printing on new tournament creation.
        # The `fixtures` property handles the actual list.
        if len(self.teams) < 2:
            print("Need at least two teams for a tournament.")
            return

        print(f"\n--- Generating Fixtures for {self.name} ---")
        sorted_teams = sorted(self.teams, key=lambda t: t.name)
        for i in range(len(sorted_teams)):
            for j in range(i + 1, len(sorted_teams)):
                team1 = sorted_teams[i]
                team2 = sorted_teams[j]
                print(f"Fixture: {team1.name} vs {team2.name} ({self.tournament_type.split(' ')[0]})")
        print("------------------------------------------")


    def display_fixtures(self):
        if not self.fixtures:
            print("No fixtures generated yet.")
            return

        print(f"\n--- {self.name} Fixtures ---")
        team_id_map = {team.id: team.name for team in self.teams}
        for i, fixture_data in enumerate(self.fixtures):
            team1_name = team_id_map.get(fixture_data['team1_id'], "Unknown Team")
            team2_name = team_id_map.get(fixture_data['team2_id'], "Unknown Team")
            status = "Upcoming" if i >= self.current_fixture_index else "Played"
            print(f"{i+1}. {team1_name} vs {team2_name} ({fixture_data['match_type']}) - {status}")
        print("----------------------------")

    def display_standings(self):
        print(f"\n--- {self.name} Standings ---")
        print(f"{'Team':<20} {'P':<4} {'W':<4} {'L':<4} {'D':<4} {'Pts':<5}")
        sorted_standings = sorted(self.standings.items(), key=lambda item: item[1]['points'], reverse=True)
        for team_id, stats in sorted_standings:
            print(f"{stats['name']:<20} {stats['played']:<4} {stats['won']:<4} {stats['lost']:<4} {stats['drawn']:<4} {stats['points']:<5}")
        print("-----------------------------")

    def play_next_fixture(self, user_player):
        if self.current_fixture_index >= len(self.fixtures):
            print(f"All matches in {self.name} have been played.")
            return None

        fixture_data = self.fixtures[self.current_fixture_index]
        team_map = {team.id: team for team in self.teams} # Map IDs back to objects
        team1 = team_map[fixture_data['team1_id']]
        team2 = team_map[fixture_data['team2_id']]
        match_type = fixture_data['match_type']

        print(f"\n--- Playing Match {self.current_fixture_index + 1}/{len(self.fixtures)} ---")
        print(f"Match: {team1.name} vs {team2.name} ({match_type})")

        match = Match(team1, team2, match_type)
        winner, is_drawn = match.play_match(user_player) # Pass user_player for stats update

        # Update standings
        self.standings[team1.id]['played'] += 1
        self.standings[team2.id]['played'] += 1

        if winner:
            self.standings[winner.id]['points'] += 2
            self.standings[winner.id]['won'] += 1
            if winner.id == team1.id:
                self.standings[team2.id]['lost'] += 1
            else:
                self.standings[team1.id]['lost'] += 1
        elif is_drawn:
            self.standings[team1.id]['points'] += 1 # Draw gets 1 point
            self.standings[team2.id]['points'] += 1 # Draw gets 1 point
            self.standings[team1.id]['drawn'] += 1
            self.standings[team2.id]['drawn'] += 1

        self.current_fixture_index += 1
        return winner

    # --- Serialization Method ---
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tournament_type': self.tournament_type,
            'teams': [team.to_dict() for team in self.teams], # Save full team data for tournament to ensure all players are included
            'current_fixture_index': self.current_fixture_index,
            'standings': self.standings
        }

    # --- Deserialization Static Method ---
    @staticmethod
    def from_dict(data):
        teams = [Team.from_dict(t_data) for t_data in data['teams']] # Load teams first
        tournament = Tournament(
            data['name'], data['tournament_type'], teams, # Pass loaded team objects
            data['current_fixture_index'], data['standings'], data['id']
        )
        return tournament

# --- Helper Functions for Game Setup and Save/Load ---
SAVE_FILE = 'cricket_career_save.json'

def create_player():
    print("\n--- Create Your Cricket Player ---")
    name = input("Enter your player's name: ")
    while True:
        try:
            age = int(input("Enter your player's age (16-35): "))
            if 16 <= age <= 35:
                break
            else:
                print("Age must be between 16 and 35.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    country = input("Enter your player's country (e.g., England, Australia): ")

    while True:
        batting_hand = input("Batting hand (Left/Right): ").capitalize()
        if batting_hand in ['Left', 'Right']:
            break
        else:
            print("Invalid input. Please enter 'Left' or 'Right'.")

    while True:
        bowling_hand = input("Bowling hand (Left/Right): ").capitalize()
        if bowling_hand in ['Left', 'Right']:
            break
        else:
            print("Invalid input. Please enter 'Left' or 'Right'.")

    bowling_types = ['Fast', 'Medium Fast', 'Off Spin', 'Leg Spin'] # Simplified for input
    print("\nChoose your bowling type:")
    for i, b_type in enumerate(bowling_types):
        print(f"{i+1}. {b_type}")

    while True:
        try:
            choice = int(input("Enter the number for your bowling type: "))
            if 1 <= choice <= len(bowling_types):
                bowling_type = bowling_types[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    return Player(name, age, country, batting_hand, bowling_hand, bowling_type, is_user=True)

def save_game(user_player, user_team, all_teams, current_tournament):
    game_state = {
        'user_player': user_player.to_dict(), # User player's actual object
        'user_team': user_team.to_dict(),     # User team's actual object
        'all_teams': [team.to_dict() for team in all_teams], # All teams in the game
        'current_tournament': current_tournament.to_dict() if current_tournament else None
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(game_state, f, indent=4)
    print("\nGame saved successfully!")

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None

    try:
        with open(SAVE_FILE, 'r') as f:
            game_state = json.load(f)
    except json.JSONDecodeError:
        print("Error loading save file. It might be corrupted. Starting new game.")
        return None

    # Load all teams first, as Player and Tournament will reference them
    loaded_all_teams_data = game_state['all_teams']
    loaded_teams_map = {t_data['id']: Team.from_dict(t_data) for t_data in loaded_all_teams_data}

    # Identify the user's specific player object within the loaded user team
    # We load the user_team from the map to ensure it's the same object as in all_teams
    user_team_data = game_state['user_team']
    user_team = loaded_teams_map[user_team_data['id']] # Get the user_team object from the loaded_teams_map
    user_player = next((p for p in user_team.players if p.is_user), None)

    if not user_player:
        print("Error: User player not found in loaded user team. Starting new game.")
        return None

    all_teams = list(loaded_teams_map.values()) # Convert map values to list

    current_tournament = None
    if game_state['current_tournament']:
        # For tournament, we need to ensure its teams are references to the
        # actual Team objects already loaded in loaded_teams_map
        tourney_teams_data = game_state['current_tournament']['teams']
        tourney_teams_objs = []
        for team_data in tourney_teams_data:
            # Get the team object from the already loaded and mapped teams
            if team_data['id'] in loaded_teams_map:
                tourney_teams_objs.append(loaded_teams_map[team_data['id']])
            else:
                # Fallback: if a team was in tournament data but not in main all_teams,
                # recreate it. This should ideally not happen if all_teams is correctly saved.
                print(f"Warning: Team ID {team_data['id']} not found in loaded all_teams. Recreating.")
                tourney_teams_objs.append(Team.from_dict(team_data))

        current_tournament = Tournament.from_dict({**game_state['current_tournament'], 'teams': tourney_teams_objs})

    print("\nGame loaded successfully!")
    return user_player, user_team, all_teams, current_tournament

# --- Main Game Loop ---
def game_main():
    print("Welcome to the Text-Based Cricket Career Game!")
    print(f"Current time: {datetime.datetime.now().strftime('%A, %B %d, %Y at %H:%M:%S %Z')}")

    user_player = None
    user_team = None
    all_teams = []
    current_tournament = None

    if os.path.exists(SAVE_FILE):
        load_choice = input("Save game found. Do you want to load it? (yes/no): ").lower()
        if load_choice == 'yes':
            loaded_data = load_game()
            if loaded_data:
                user_player, user_team, all_teams, current_tournament = loaded_data
            else:
                print("Starting a new game.")
                # Existing new game creation logic
                user_player = create_player()
                user_team = Team(f"{user_player.country} (Player's Team)", is_user_team=True)
                user_team.add_player(user_player)
                for i in range(10): user_team.add_player(Player(f"Teammate {i+1} {user_team.name}", random.randint(20, 30), user_player.country, random.choice(['Left', 'Right']), random.choice(['Left', 'Right']), random.choice(['Fast', 'Off Spin', 'Leg Spin'])))
                opponent_countries = [c for c in ["Australia", "India", "England", "South Africa", "New Zealand", "Pakistan"] if c != user_player.country]
                random.shuffle(opponent_countries)
                for country in opponent_countries[:5]:
                    team = Team(country)
                    team.generate_random_squad()
                    all_teams.append(team)
                all_teams = [user_team] + all_teams # Ensure user team is always part of all_teams
        else:
            print("Starting a new game.")
            # Existing new game creation logic
            user_player = create_player()
            user_team = Team(f"{user_player.country} (Player's Team)", is_user_team=True)
            user_team.add_player(user_player)
            for i in range(10): user_team.add_player(Player(f"Teammate {i+1} {user_team.name}", random.randint(20, 30), user_player.country, random.choice(['Left', 'Right']), random.choice(['Left', 'Right']), random.choice(['Fast', 'Off Spin', 'Leg Spin'])))
            opponent_countries = [c for c in ["Australia", "India", "England", "South Africa", "New Zealand", "Pakistan"] if c != user_player.country]
            random.shuffle(opponent_countries)
            for country in opponent_countries[:5]:
                team = Team(country)
                team.generate_random_squad()
                all_teams.append(team)
            all_teams = [user_team] + all_teams # Ensure user team is always part of all_teams

    else:
        print("No save game found. Creating a new career.")
        user_player = create_player()
        user_team = Team(f"{user_player.country} (Player's Team)", is_user_team=True)
        user_team.add_player(user_player)
        for i in range(10):
            user_team.add_player(Player(f"Teammate {i+1} {user_team.name}", random.randint(20, 30), user_player.country,
                                        random.choice(['Left', 'Right']), random.choice(['Left', 'Right']),
                                        random.choice(['Fast', 'Off Spin', 'Leg Spin'])))
        opponent_countries = [c for c in ["Australia", "India", "England", "South Africa", "New Zealand", "Pakistan"] if c != user_player.country]
        random.shuffle(opponent_countries)
        for country in opponent_countries[:5]:
            team = Team(country)
            team.generate_random_squad()
            all_teams.append(team)
        all_teams = [user_team] + all_teams # Ensure user team is always part of all_teams

    while True:
        print("\n--- Cricket Career Game Menu ---")
        print("1. View Player Profile (Overall)")
        print("2. View My Performance (By Format)")
        print("3. Train Player")
        print("4. Rest Player (Recover Fitness)")
        if not current_tournament:
            print("5. Join/Create Tournament")
        else:
            print(f"5. Continue {current_tournament.name}")

        print("6. View Current Tournament Fixtures")
        print("7. View Current Tournament Standings")
        print("8. Play Next Match in Tournament")
        print("9. Save Game") # New option
        print("10. Retire Player")
        print("0. Exit Game (without saving)")

        choice = input("Enter your choice: ")

        if choice == '1':
            user_player.display_profile()
        elif choice == '2':
            user_player.display_performance_by_format()
        elif choice == '3':
            skill_choice = input("Train (batting/bowling)? ").lower()
            if skill_choice in ['batting', 'bowling']:
                user_player.train(skill_choice)
            else:
                print("Invalid skill type.")
        elif choice == '4':
            user_player.recover_fitness()
        elif choice == '5': # Join/Continue Tournament
            if current_tournament:
                print(f"You are already in the {current_tournament.name}. Select option 8 to continue.")
                continue

            print("\n--- Choose Tournament Type ---")
            print("1. T20 Cup")
            print("2. ODI Cup")
            print("3. Test Championship")
            tourney_choice = input("Enter choice: ")

            tournament_type_map = {
                '1': 'T20 Cup',
                '2': 'ODI Cup',
                '3': 'Test Championship'
            }
            selected_tournament_type = tournament_type_map.get(tourney_choice)

            if selected_tournament_type:
                # Ensure the teams passed to the tournament are the same actual objects
                # from the all_teams list, so changes reflect across the game state.
                current_tournament = Tournament(f"{selected_tournament_type} (Season {random.randint(1, 5)})",
                                                selected_tournament_type, list(all_teams))
                print(f"You have joined the {current_tournament.name}!")
            else:
                print("Invalid tournament choice.")
        elif choice == '6':
            if current_tournament:
                current_tournament.display_fixtures()
            else:
                print("No active tournament. Join one first!")
        elif choice == '7':
            if current_tournament:
                current_tournament.display_standings()
            else:
                print("No active tournament. Join one first!")
        elif choice == '8':
            if current_tournament:
                result = current_tournament.play_next_fixture(user_player)
                if current_tournament.current_fixture_index >= len(current_tournament.fixtures):
                    print(f"\n--- {current_tournament.name} Concluded! ---")
                    current_tournament.display_standings()
                    final_standings = sorted(current_tournament.standings.items(), key=lambda item: item[1]['points'], reverse=True)
                    if final_standings:
                        tournament_winner_id = final_standings[0][0]
                        tournament_winner_name = final_standings[0][1]['name']
                        print(f"\nCongratulations to {tournament_winner_name} for winning the {current_tournament.name}!")
                        # If user's team won, add trophy to user player
                        if user_team.id == tournament_winner_id:
                            user_player.trophies_won[current_tournament.tournament_type] += 1
                            print(f"You won the {current_tournament.tournament_type}!")
                    current_tournament = None
            else:
                print("No active tournament. Join one first!")
        elif choice == '9': # Save Game
            save_game(user_player, user_team, all_teams, current_tournament)
        elif choice == '10': # Retire Player
            confirm = input("Are you sure you want to retire? (yes/no): ").lower()
            if confirm == 'yes':
                print(f"\n{user_player.name} has retired from cricket. What a career!")
                user_player.display_profile()
                save_game(user_player, user_team, all_teams, current_tournament) # Save on retire
                break
        elif choice == '0': # Exit Game (without saving)
            print("Exiting game. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    game_main()
