# ChoreDistributor

#Chore Scheduler

This is a Python program that schedules household chores for a group of people over a span of four weeks. It uses the Google OR-Tools library to solve the scheduling problem by assigning chores to individuals while considering their availability and ensuring an equal distribution of chores among all persons.

## Features

- Automatically schedules chores for four weeks based on predefined constraints and preferences.
- Ensures that each person has a fair share of chores over the four-week period.
- Considers each person's availability on specific days for chore assignments.
- Provides flexibility in the total hardness score for each person over the four weeks.

## Constraints

- At least one chore and no more than three chores are assigned to each person per week.
- Each chore must be assigned exactly six times to all persons over the four weeks.
- The total hardness score for each person over the four weeks is between 340 and 380.

