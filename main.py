import yaml
import os
import sys
from collections import defaultdict
from typing import Dict, List, Any, Optional

class CricketScoreboard:
    def __init__(self, yaml_file_path: str = None):
        self.data = None
        self.batting_stats = {}
        self.bowling_stats = {}
        self.team_totals = {}
        self.partnership_stats = {}
        
        if yaml_file_path:
            self.load_match_data(yaml_file_path)
    
    def load_match_data(self, file_path: str) -> bool:
        """Load cricket match data from YAML file with comprehensive error handling"""
        try:
            if not os.path.exists(file_path):
                return False, f"File '{file_path}' not found!"
            
            with open(file_path, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)
                
            if not self.data:
                return False, "YAML file is empty or invalid!"
            
            # Validate basic structure
            valid, error_msg = self.validate_yaml_structure()
            if not valid:
                return False, error_msg
            
            self.analyze_match_data()
            return True, "Successfully loaded match data"
            
        except yaml.YAMLError as e:
            return False, f"Error parsing YAML: {e}"
        except Exception as e:
            return False, f"Unexpected error loading file: {e}"
    
    def validate_yaml_structure(self) -> tuple:
        """Validate the YAML structure for required cricket data"""
        if not isinstance(self.data, dict):
            return False, "YAML root must be a dictionary"
        
        # Check for essential sections
        if 'innings' not in self.data:
            return False, "No 'innings' section found in YAML"
        
        if not isinstance(self.data['innings'], list):
            return False, "'innings' must be a list"
        
        if len(self.data['innings']) == 0:
            return False, "No innings data found"
        
        # Check info section
        info = self.data.get('info', {})
        if not info.get('teams'):
            # This is just a warning, not an error
            pass
        
        return True, "YAML structure validation passed"
    
    def analyze_match_data(self):
        """Comprehensive analysis of match data to calculate all statistics"""
        if not self.data or 'innings' not in self.data:
            return
        
        # Initialize stats dictionaries
        all_teams = set()
        
        # First pass: identify all teams
        for innings_data in self.data['innings']:
            for innings_key, innings_info in innings_data.items():
                team = innings_info.get('team', 'Unknown Team')
                all_teams.add(team)
        
        # Initialize stats for all teams
        for team in all_teams:
            self.batting_stats[team] = defaultdict(lambda: {
                'runs': 0, 'balls': 0, 'fours': 0, 'sixes': 0, 
                'out': False, 'how_out': '', 'position': 0
            })
            self.bowling_stats[team] = defaultdict(lambda: {
                'overs': 0, 'runs': 0, 'wickets': 0, 'maidens': 0, 'dots': 0
            })
            self.team_totals[team] = {
                'runs': 0, 'wickets': 0, 'overs': 0, 'extras': 0,
                'run_rate': 0, 'required_rate': 0
            }
            self.partnership_stats[team] = []
        
        # Second pass: analyze innings data
        for innings_index, innings_data in enumerate(self.data['innings']):
            for innings_key, innings_info in innings_data.items():
                self._analyze_innings(innings_info, innings_index)
    
    def _analyze_innings(self, innings_info: Dict, innings_index: int):
        """Analyze individual innings data"""
        team = innings_info.get('team', 'Unknown Team')
        deliveries = innings_info.get('deliveries', [])
        
        # Determine bowling team (opposite team)
        all_teams = list(self.batting_stats.keys())
        bowling_team = None
        for t in all_teams:
            if t != team:
                bowling_team = t
                break
        
        if not bowling_team:
            bowling_team = "Bowling Team"  # Fallback
        
        total_runs = 0
        total_wickets = 0
        total_balls = 0
        extras = 0
        
        current_over_runs = 0
        current_over_balls = 0
        last_over = -1
        last_bowler = None
        
        batting_order = {}
        order_counter = 1
        
        for delivery in deliveries:
            for ball_key, ball_data in delivery.items():
                # Handle both string and float ball keys
                ball_key_str = str(ball_key)
                try:
                    over_num = float(ball_key_str.split('.')[0])
                    ball_num = float(ball_key_str.split('.')[1]) if '.' in ball_key_str else 0
                except (ValueError, IndexError):
                    continue
                
                # Track overs and maiden detection
                if over_num != last_over:
                    if last_over != -1 and current_over_balls == 6 and current_over_runs == 0 and last_bowler:
                        self.bowling_stats[bowling_team][last_bowler]['maidens'] += 1
                    last_over = over_num
                    current_over_runs = 0
                    current_over_balls = 0
                
                # Extract ball data
                batsman = ball_data.get('batsman', 'Unknown')
                bowler = ball_data.get('bowler', 'Unknown')
                runs = ball_data.get('runs', {})
                
                # Track batting order
                if batsman not in batting_order:
                    batting_order[batsman] = order_counter
                    self.batting_stats[team][batsman]['position'] = order_counter
                    order_counter += 1
                
                batsman_runs = runs.get('batsman', 0)
                total_runs_this_ball = runs.get('total', 0)
                extras_this_ball = runs.get('extras', 0)
                
                # Update batting stats for batting team
                self.batting_stats[team][batsman]['runs'] += batsman_runs
                
                # Only count legal deliveries for balls faced
                if extras_this_ball == 0 or not ball_data.get('extras', {}):
                    self.batting_stats[team][batsman]['balls'] += 1
                    current_over_balls += 1
                    total_balls += 1
                
                # Count boundaries
                if batsman_runs == 4:
                    self.batting_stats[team][batsman]['fours'] += 1
                elif batsman_runs == 6:
                    self.batting_stats[team][batsman]['sixes'] += 1
                
                # Update bowling stats for bowling team
                if extras_this_ball == 0 or not ball_data.get('extras', {}):
                    self.bowling_stats[bowling_team][bowler]['overs'] += 1/6
                
                self.bowling_stats[bowling_team][bowler]['runs'] += total_runs_this_ball
                
                # Count dot balls
                if total_runs_this_ball == 0:
                    self.bowling_stats[bowling_team][bowler]['dots'] += 1
                
                # Handle wickets - update bowling team's wicket count
                if 'wicket' in ball_data:
                    wicket_info = ball_data['wicket']
                    player_out = wicket_info.get('player_out', batsman)
                    how_out = wicket_info.get('kind', 'Unknown')
                    fielders = wicket_info.get('fielders', [])
                    
                    # Update batting team's dismissal info
                    self.batting_stats[team][player_out]['out'] = True
                    
                    # Format dismissal details properly
                    if how_out == 'caught':
                        if fielders:
                            self.batting_stats[team][player_out]['how_out'] = f"c {', '.join(fielders)} b {bowler}"
                        else:
                            self.batting_stats[team][player_out]['how_out'] = f"c & b {bowler}"
                    elif how_out == 'bowled':
                        self.batting_stats[team][player_out]['how_out'] = f"b {bowler}"
                    elif how_out == 'lbw':
                        self.batting_stats[team][player_out]['how_out'] = f"lbw b {bowler}"
                    elif how_out == 'stumped':
                        if fielders:
                            self.batting_stats[team][player_out]['how_out'] = f"st {', '.join(fielders)} b {bowler}"
                        else:
                            self.batting_stats[team][player_out]['how_out'] = f"st b {bowler}"
                    elif how_out == 'run out':
                        if fielders:
                            self.batting_stats[team][player_out]['how_out'] = f"run out ({', '.join(fielders)})"
                        else:
                            self.batting_stats[team][player_out]['how_out'] = "run out"
                    else:
                        self.batting_stats[team][player_out]['how_out'] = f"{how_out}"
                        if fielders:
                            self.batting_stats[team][player_out]['how_out'] += f" ({', '.join(fielders)})"
                    
                    # Update bowling team's wicket count
                    self.bowling_stats[bowling_team][bowler]['wickets'] += 1
                    total_wickets += 1
                
                total_runs += total_runs_this_ball
                extras += extras_this_ball
                current_over_runs += total_runs_this_ball
                last_bowler = bowler
        
        # Calculate final statistics
        final_overs = int(last_over) + (current_over_balls / 6) if last_over >= 0 else 0
        run_rate = (total_runs / final_overs) if final_overs > 0 else 0
        
        self.team_totals[team].update({
            'runs': total_runs,
            'wickets': total_wickets,
            'overs': final_overs,
            'extras': extras,
            'run_rate': run_rate
        })
    
    def get_match_header_data(self) -> Dict[str, Any]:
        """Get match header information as structured data"""
        if not self.data:
            return {}
        
        info = self.data.get('info', {})
        meta = self.data.get('meta', {})
        
        header_data = {
            'match_type': info.get('match_type', 'Unknown').upper(),
            'venue': info.get('venue', 'Unknown Venue'),
            'city': info.get('city', ''),
            'date': info.get('dates', ['Unknown'])[0] if info.get('dates') else 'Unknown',
            'teams': info.get('teams', []),
            'toss': info.get('toss', {}),
            'outcome': info.get('outcome', {}),
            'player_of_match': info.get('player_of_match', [])
        }
        
        return header_data
    
    def get_batting_stats_for_team(self, team: str) -> List[Dict[str, Any]]:
        """Get batting statistics for a specific team"""
        if team not in self.batting_stats:
            return []
        
        stats = []
        for player, data in self.batting_stats[team].items():
            if data['runs'] > 0 or data['balls'] > 0 or data['out']:
                strike_rate = (data['runs'] / data['balls'] * 100) if data['balls'] > 0 else 0
                stats.append({
                    'position': data['position'],
                    'player': player,
                    'runs': data['runs'],
                    'balls': data['balls'],
                    'fours': data['fours'],
                    'sixes': data['sixes'],
                    'strike_rate': round(strike_rate, 2),
                    'out': data['out'],
                    'how_out': data['how_out'] if data['out'] else 'not out'
                })
        
        # Sort by batting position
        stats.sort(key=lambda x: x['position'])
        return stats
    
    def get_bowling_stats_for_team(self, team: str) -> List[Dict[str, Any]]:
        """Get bowling statistics for a specific team"""
        if team not in self.bowling_stats:
            return []
        
        stats = []
        for bowler, data in self.bowling_stats[team].items():
            if data['overs'] > 0 or data['runs'] > 0 or data['wickets'] > 0:
                economy = (data['runs'] / data['overs']) if data['overs'] > 0 else 0
                overs_str = f"{int(data['overs'])}.{int((data['overs'] % 1) * 6)}"
                
                stats.append({
                    'bowler': bowler,
                    'overs': overs_str,
                    'maidens': data['maidens'],
                    'runs': data['runs'],
                    'wickets': data['wickets'],
                    'economy': round(economy, 2),
                    'dots': data['dots']
                })
        
        # Sort by wickets (descending) then by economy (ascending)
        stats.sort(key=lambda x: (-x['wickets'], x['economy']))
        return stats
    
    def get_team_totals(self) -> Dict[str, Dict[str, Any]]:
        """Get team totals for all teams"""
        return self.team_totals.copy()

if __name__ == "__main__":
    # Command line interface for testing
    if len(sys.argv) > 1:
        scoreboard = CricketScoreboard()
        success, message = scoreboard.load_match_data(sys.argv[1])
        if success:
            print("Match data loaded successfully!")
            print(f"Teams: {list(scoreboard.team_totals.keys())}")
        else:
            print(f"Error: {message}")
    else:
        print("Usage: python main.py <yaml_file_path>")
