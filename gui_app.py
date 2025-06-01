import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from main import CricketScoreboard

class CricketScoreboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Scoreboard Analyzer")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set the application icon
        try:
            self.root.iconbitmap("app_icon.ico")
        except:
            pass  # Icon file not found, continue without it
        
        self.scoreboard = CricketScoreboard()
        self.current_file = None
        
        self.setup_styles()
        self.create_widgets()
        self.show_welcome_screen()
    
    def setup_styles(self):
        """Configure ttk styles for better appearance"""
        style = ttk.Style()
        
        # Configure notebook tabs
        style.configure('Tab.TNotebook.Tab', padding=[10, 5])
        
        # Configure treeview
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Treeview", font=('Arial', 9))
        
        # Configure buttons
        style.configure("Action.TButton", font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Top frame for file operations
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        top_frame.columnconfigure(1, weight=1)
        
        # File selection button
        self.load_button = ttk.Button(
            top_frame, 
            text="Load YAML File", 
            command=self.load_file,
            style="Action.TButton"
        )
        self.load_button.grid(row=0, column=0, padx=(0, 10))
        
        # File path label
        self.file_label = ttk.Label(top_frame, text="No file loaded", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Progress bar (hidden initially)
        self.progress = ttk.Progressbar(
            top_frame, 
            mode='indeterminate', 
            length=200
        )
        self.progress.grid(row=0, column=2, padx=(10, 0))
        self.progress.grid_remove()
        
        # Main content area
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # Create notebook for tabs (hidden initially)
        self.notebook = ttk.Notebook(self.content_frame, style='Tab.TNotebook')
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.notebook.grid_remove()
        
        # Create tab frames
        self.create_tab_frames()
    
    def create_tab_frames(self):
        """Create frames for different tabs"""
        # Match Info Tab
        self.match_info_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.match_info_frame, text="Match Info")
        
        # Batting Stats Tab
        self.batting_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.batting_frame, text="Batting Stats")
        
        # Bowling Stats Tab
        self.bowling_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.bowling_frame, text="Bowling Stats")
        
        # Team Totals Tab
        self.totals_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.totals_frame, text="Team Totals")
    
    def show_welcome_screen(self):
        """Show welcome screen when no file is loaded"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.grid_remove()
        
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        welcome_frame.columnconfigure(0, weight=1)
        welcome_frame.rowconfigure(0, weight=1)
        
        inner_frame = ttk.Frame(welcome_frame)
        inner_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Welcome message
        welcome_label = ttk.Label(
            inner_frame, 
            text="🏏 Cricket Scoreboard Analyzer", 
            font=('Arial', 24, 'bold')
        )
        welcome_label.pack(pady=(0, 20))
        
        description = ttk.Label(
            inner_frame,
            text="Load a cricket match YAML file to analyze comprehensive statistics\nincluding batting, bowling, and team performance data.",
            font=('Arial', 12),
            justify=tk.CENTER
        )
        description.pack(pady=(0, 30))
        
        load_btn = ttk.Button(
            inner_frame,
            text="Load YAML File",
            command=self.load_file,
            style="Action.TButton"
        )
        load_btn.pack()
        
        self.welcome_frame = welcome_frame
    
    def load_file(self):
        """Load a YAML file with cricket match data"""
        file_path = filedialog.askopenfilename(
            title="Select Cricket Match YAML File",
            filetypes=[
                ("YAML files", "*.yaml *.yml"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.current_file = file_path
            self.file_label.config(text=f"Loading: {os.path.basename(file_path)}")
            
            # Show progress bar
            self.progress.grid()
            self.progress.start()
            self.load_button.config(state='disabled')
            
            # Load file in background thread
            thread = threading.Thread(target=self.load_file_worker, args=(file_path,))
            thread.daemon = True
            thread.start()
    
    def load_file_worker(self, file_path):
        """Worker thread for loading file"""
        try:
            success, message = self.scoreboard.load_match_data(file_path)
            
            # Update GUI in main thread
            self.root.after(0, self.load_file_complete, success, message, file_path)
            
        except Exception as e:
            self.root.after(0, self.load_file_complete, False, str(e), file_path)
    
    def load_file_complete(self, success, message, file_path):
        """Complete file loading process"""
        # Hide progress bar
        self.progress.stop()
        self.progress.grid_remove()
        self.load_button.config(state='normal')
        
        if success:
            self.file_label.config(
                text=f"Loaded: {os.path.basename(file_path)}",
                foreground="green"
            )
            self.show_match_data()
        else:
            self.file_label.config(
                text=f"Error loading: {os.path.basename(file_path)}",
                foreground="red"
            )
            messagebox.showerror("Load Error", f"Failed to load file:\n{message}")
    
    def show_match_data(self):
        """Show the loaded match data in tabs"""
        # Hide welcome screen
        if hasattr(self, 'welcome_frame'):
            self.welcome_frame.grid_remove()
        
        # Show notebook
        self.notebook.grid()
        
        # Populate all tabs
        self.populate_match_info()
        self.populate_batting_stats()
        self.populate_bowling_stats()
        self.populate_team_totals()
    
    def populate_match_info(self):
        """Populate match information tab"""
        # Clear existing widgets
        for widget in self.match_info_frame.winfo_children():
            widget.destroy()
        
        header_data = self.scoreboard.get_match_header_data()
        
        if not header_data:
            ttk.Label(self.match_info_frame, text="No match information available").pack()
            return
        
        # Create scrollable frame
        canvas = tk.Canvas(self.match_info_frame)
        scrollbar = ttk.Scrollbar(self.match_info_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Match details
        ttk.Label(scrollable_frame, text="Match Information", font=('Arial', 16, 'bold')).pack(pady=(0, 15))
        
        info_frame = ttk.Frame(scrollable_frame)
        info_frame.pack(fill=tk.X, padx=20)
        
        # Basic match info
        self.add_info_row(info_frame, "Match Type:", header_data.get('match_type', 'Unknown'))
        self.add_info_row(info_frame, "Venue:", header_data.get('venue', 'Unknown'))
        
        if header_data.get('city'):
            self.add_info_row(info_frame, "City:", header_data['city'])
        
        self.add_info_row(info_frame, "Date:", header_data.get('date', 'Unknown'))
        
        # Teams
        teams = header_data.get('teams', [])
        if len(teams) >= 2:
            self.add_info_row(info_frame, "Teams:", f"{teams[0]} vs {teams[1]}")
        
        # Toss information
        toss = header_data.get('toss', {})
        if toss:
            toss_winner = toss.get('winner', 'Unknown')
            toss_decision = toss.get('decision', 'unknown')
            self.add_info_row(info_frame, "Toss:", f"{toss_winner} won and chose to {toss_decision}")
        
        # Match result
        outcome = header_data.get('outcome', {})
        if 'winner' in outcome:
            winner = outcome['winner']
            result_text = f"{winner} won"
            
            if 'by' in outcome:
                by = outcome['by']
                if 'runs' in by:
                    result_text += f" by {by['runs']} runs"
                elif 'wickets' in by:
                    result_text += f" by {by['wickets']} wickets"
            
            self.add_info_row(info_frame, "Result:", result_text)
        elif 'result' in outcome:
            self.add_info_row(info_frame, "Result:", outcome['result'])
        
        # Player of the match
        pom = header_data.get('player_of_match', [])
        if pom:
            if isinstance(pom, list):
                self.add_info_row(info_frame, "Player of the Match:", ', '.join(pom))
            else:
                self.add_info_row(info_frame, "Player of the Match:", pom)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_info_row(self, parent, label, value):
        """Add an information row to the match info"""
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(row_frame, text=label, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, anchor=tk.W)
        ttk.Label(row_frame, text=str(value)).pack(side=tk.LEFT, anchor=tk.W, padx=(10, 0))
    
    def populate_batting_stats(self):
        """Populate batting statistics tab"""
        # Clear existing widgets
        for widget in self.batting_frame.winfo_children():
            widget.destroy()
        
        teams = list(self.scoreboard.team_totals.keys())
        
        if not teams:
            ttk.Label(self.batting_frame, text="No batting statistics available").pack()
            return
        
        # Create notebook for teams
        team_notebook = ttk.Notebook(self.batting_frame)
        team_notebook.pack(fill=tk.BOTH, expand=True)
        
        for team in teams:
            team_frame = ttk.Frame(team_notebook, padding="10")
            team_notebook.add(team_frame, text=team)
            
            # Get batting stats for this team
            batting_stats = self.scoreboard.get_batting_stats_for_team(team)
            
            if not batting_stats:
                ttk.Label(team_frame, text=f"No batting statistics available for {team}").pack()
                continue
            
            # Create treeview for batting stats
            columns = ("Player", "Runs", "Balls", "4s", "6s", "SR", "Status")
            tree = ttk.Treeview(team_frame, columns=columns, show="headings", height=15)
            
            # Configure columns
            tree.heading("Player", text="Player")
            tree.heading("Runs", text="Runs")
            tree.heading("Balls", text="Balls")
            tree.heading("4s", text="4s")
            tree.heading("6s", text="6s")
            tree.heading("SR", text="Strike Rate")
            tree.heading("Status", text="Status")
            
            tree.column("Player", width=150)
            tree.column("Runs", width=80, anchor=tk.CENTER)
            tree.column("Balls", width=80, anchor=tk.CENTER)
            tree.column("4s", width=60, anchor=tk.CENTER)
            tree.column("6s", width=60, anchor=tk.CENTER)
            tree.column("SR", width=100, anchor=tk.CENTER)
            tree.column("Status", width=200)
            
            # Add data
            for stats in batting_stats:
                tree.insert("", tk.END, values=(
                    stats['player'],
                    stats['runs'],
                    stats['balls'],
                    stats['fours'],
                    stats['sixes'],
                    f"{stats['strike_rate']:.2f}",
                    stats['how_out']
                ))
            
            # Add scrollbars
            v_scrollbar = ttk.Scrollbar(team_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=v_scrollbar.set)
            
            h_scrollbar = ttk.Scrollbar(team_frame, orient=tk.HORIZONTAL, command=tree.xview)
            tree.configure(xscrollcommand=h_scrollbar.set)
            
            tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
            
            team_frame.columnconfigure(0, weight=1)
            team_frame.rowconfigure(0, weight=1)
    
    def populate_bowling_stats(self):
        """Populate bowling statistics tab"""
        # Clear existing widgets
        for widget in self.bowling_frame.winfo_children():
            widget.destroy()
        
        teams = list(self.scoreboard.team_totals.keys())
        
        if not teams:
            ttk.Label(self.bowling_frame, text="No bowling statistics available").pack()
            return
        
        # Create notebook for teams
        team_notebook = ttk.Notebook(self.bowling_frame)
        team_notebook.pack(fill=tk.BOTH, expand=True)
        
        for team in teams:
            team_frame = ttk.Frame(team_notebook, padding="10")
            team_notebook.add(team_frame, text=team)
            
            # Get bowling stats for this team
            bowling_stats = self.scoreboard.get_bowling_stats_for_team(team)
            
            if not bowling_stats:
                ttk.Label(team_frame, text=f"No bowling statistics available for {team}").pack()
                continue
            
            # Create treeview for bowling stats
            columns = ("Bowler", "Overs", "Maidens", "Runs", "Wickets", "Economy", "Dots")
            tree = ttk.Treeview(team_frame, columns=columns, show="headings", height=15)
            
            # Configure columns
            tree.heading("Bowler", text="Bowler")
            tree.heading("Overs", text="Overs")
            tree.heading("Maidens", text="Maidens")
            tree.heading("Runs", text="Runs")
            tree.heading("Wickets", text="Wickets")
            tree.heading("Economy", text="Economy")
            tree.heading("Dots", text="Dot Balls")
            
            tree.column("Bowler", width=150)
            tree.column("Overs", width=80, anchor=tk.CENTER)
            tree.column("Maidens", width=80, anchor=tk.CENTER)
            tree.column("Runs", width=80, anchor=tk.CENTER)
            tree.column("Wickets", width=80, anchor=tk.CENTER)
            tree.column("Economy", width=100, anchor=tk.CENTER)
            tree.column("Dots", width=100, anchor=tk.CENTER)
            
            # Add data
            for stats in bowling_stats:
                tree.insert("", tk.END, values=(
                    stats['bowler'],
                    stats['overs'],
                    stats['maidens'],
                    stats['runs'],
                    stats['wickets'],
                    f"{stats['economy']:.2f}",
                    stats['dots']
                ))
            
            # Add scrollbars
            v_scrollbar = ttk.Scrollbar(team_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=v_scrollbar.set)
            
            h_scrollbar = ttk.Scrollbar(team_frame, orient=tk.HORIZONTAL, command=tree.xview)
            tree.configure(xscrollcommand=h_scrollbar.set)
            
            tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
            
            team_frame.columnconfigure(0, weight=1)
            team_frame.rowconfigure(0, weight=1)
    
    def populate_team_totals(self):
        """Populate team totals tab"""
        # Clear existing widgets
        for widget in self.totals_frame.winfo_children():
            widget.destroy()
        
        team_totals = self.scoreboard.get_team_totals()
        
        if not team_totals:
            ttk.Label(self.totals_frame, text="No team totals available").pack()
            return
        
        # Create treeview for team totals
        columns = ("Team", "Runs", "Wickets", "Overs", "Extras", "Run Rate")
        tree = ttk.Treeview(self.totals_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        tree.heading("Team", text="Team")
        tree.heading("Runs", text="Runs")
        tree.heading("Wickets", text="Wickets")
        tree.heading("Overs", text="Overs")
        tree.heading("Extras", text="Extras")
        tree.heading("Run Rate", text="Run Rate")
        
        tree.column("Team", width=200)
        tree.column("Runs", width=100, anchor=tk.CENTER)
        tree.column("Wickets", width=100, anchor=tk.CENTER)
        tree.column("Overs", width=100, anchor=tk.CENTER)
        tree.column("Extras", width=100, anchor=tk.CENTER)
        tree.column("Run Rate", width=120, anchor=tk.CENTER)
        
        # Add data
        for team, totals in team_totals.items():
            overs_str = f"{int(totals['overs'])}.{int((totals['overs'] % 1) * 6)}"
            tree.insert("", tk.END, values=(
                team,
                totals['runs'],
                totals['wickets'],
                overs_str,
                totals['extras'],
                f"{totals['run_rate']:.2f}"
            ))
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(self.totals_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(self.totals_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(xscrollcommand=h_scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = CricketScoreboardGUI(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
