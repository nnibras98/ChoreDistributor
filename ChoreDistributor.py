from ortools.sat.python import cp_model

class EnhancedChoreScheduler:
    def __init__(self):
        self.model = cp_model.CpModel()
        self.chores = [
            'Vacuuming', 'Broom and Mop Kitchen Floor', 'Broom and Mop Washroom Floor',
            'Clean the Bath Tub', 'Clean the Toilet and the Cabinet', 'Clean Kitchen Cabinets'
        ]
        self.chore_difficulty = {
            'Vacuuming': 60, 'Broom and Mop Kitchen Floor': 80,
            'Broom and Mop Washroom Floor': 20, 'Clean the Bath Tub': 40,
            'Clean the Toilet and the Cabinet': 100, 'Clean Kitchen Cabinets': 60
        }
        self.people = ['Nafi', 'Param', 'Allen', 'Mudit']
        self.weeks = ['Week1', 'Week2', 'Week3', 'Week4']
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.availability = {
            'Nafi': ['Thursday', 'Saturday'],
            'Param': ['Saturday', 'Sunday'],
            'Allen': ['Sunday', 'Tuesday'],
            'Mudit': self.days  # Mudit is available any day
        }
        self.assignments = {
            (chore, person, week, day): self.model.NewBoolVar(f'{chore}_{person}_{week}_{day}')
            for chore in self.chores for person in self.people
            for week in self.weeks for day in self.days
        }

    def setup_constraints(self):
        for week in self.weeks:
            for chore in self.chores:
                self.model.Add(
                    sum(self.assignments[chore, person, week, day] for person in self.people for day in self.days) == 1
                )

        for person in self.people:
            for week in self.weeks:
                chores_per_week = sum(
                    self.assignments[chore, person, week, day] for chore in self.chores for day in self.days
                )
                self.model.Add(chores_per_week >= 1)  # At least one chore per week
                self.model.Add(chores_per_week <= 2)  # No more than two chores per week

                for day in self.days:
                    if day not in self.availability[person]:
                        for chore in self.chores:
                            self.model.Add(self.assignments[chore, person, week, day] == 0)

        # Enforce total hardness score of 360 for each person over 4 weeks
        for person in self.people:
            total_hardness = sum(
                self.assignments[chore, person, week, day] * self.chore_difficulty[chore]
                for chore in self.chores for week in self.weeks for day in self.days
            )
            self.model.Add(total_hardness == 360)

    def solve(self):
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            print("Optimal or feasible solution found:\n")
            for week in self.weeks:
                print(f"{week} Assignments:")
                for person in self.people:
                    print(f"\n{person}:")
                    for day in self.days:
                        chores_for_day = [
                            chore for chore in self.chores if solver.Value(self.assignments[chore, person, week, day])
                        ]
                        if chores_for_day:
                            print(f"  {day}: {', '.join(chores_for_day)}")
            print("\nAll persons have a total hardness score of 360 over 4 weeks.")
        else:
            print("No solution was found. The constraints may be too restrictive.")

if __name__ == '__main__':
    scheduler = EnhancedChoreScheduler()
    scheduler.setup_constraints()
    scheduler.solve()
