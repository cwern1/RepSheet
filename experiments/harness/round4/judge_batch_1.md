## Case 1
Inputs: style=EMOM, duration=7 min, equipment=['Bodyweight']
### Candidate A
```json
{
 "format_line": "EMOM 6",
 "scheme": "3 stations \u00d7 2 rounds",
 "movements": [
  {
   "reps": "10",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "18",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "16",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight"
 ]
}
```
### Candidate B
```json
{
 "format_line": "EMOM 8",
 "scheme": "2 stations \u00d7 4 rounds",
 "movements": [
  {
   "reps": "10",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "20",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Burpees at a steady pace to leave 10-15 s of rest; squats unbroken. Breathing is the limiter, so keep moving.",
 "equipment_used": [
  "Bodyweight"
 ]
}
```
### Candidate C
```json
{
 "format_line": "EMOM 8",
 "scheme": "2 stations \u00d7 4 rounds",
 "movements": [
  {
   "reps": "10",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "20 m",
   "name": "Bear Crawl",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Keep burpees steady so you start each minute with a few seconds in hand; bear crawl fast but low and controlled.",
 "equipment_used": [
  "Bodyweight"
 ]
}
```

## Case 2
Inputs: style=EMOM, duration=30 min, equipment=['Rower', 'Bike Erg', 'Ski Erg', 'Assault Bike']
### Candidate A
```json
{
 "format_line": "EMOM 28",
 "scheme": "4 stations \u00d7 7 rounds",
 "movements": [
  {
   "reps": "9 cal",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "10 cal",
   "name": "Bike Erg",
   "load_kg": null,
   "equipment": [
    "Bike Erg"
   ]
  },
  {
   "reps": "8 cal",
   "name": "Ski Erg",
   "load_kg": null,
   "equipment": [
    "Ski Erg"
   ]
  },
  {
   "reps": "6 cal",
   "name": "Assault Bike",
   "load_kg": null,
   "equipment": [
    "Assault Bike"
   ]
  }
 ],
 "notes": "Each station takes about 36-42 s, so you get a short breather before the next minute starts. Stay tall, brace your trunk on the ski erg and drive with the hips, and keep the pace steady so every round looks the same.",
 "equipment_used": [
  "Rower",
  "Bike Erg",
  "Ski Erg",
  "Assault Bike"
 ]
}
```
### Candidate B
```json
{
 "format_line": "EMOM 30",
 "scheme": "5 stations \u00d7 6 rounds",
 "movements": [
  {
   "reps": "8 cal",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "10 cal",
   "name": "Bike Erg",
   "load_kg": null,
   "equipment": [
    "Bike Erg"
   ]
  },
  {
   "reps": "8 cal",
   "name": "Ski Erg",
   "load_kg": null,
   "equipment": [
    "Ski Erg"
   ]
  },
  {
   "reps": "7 cal",
   "name": "Assault Bike",
   "load_kg": null,
   "equipment": [
    "Assault Bike"
   ]
  },
  {
   "reps": "1 min",
   "name": "Rest",
   "load_kg": null,
   "equipment": []
  }
 ],
 "notes": "Each station should take about 40 s, so hold a steady pace you can repeat and keep the rest of the minute as a short breather. Brace your trunk and keep your ribs down on every Ski Erg pull.",
 "equipment_used": [
  "Rower",
  "Bike Erg",
  "Ski Erg",
  "Assault Bike"
 ]
}
```
### Candidate C
```json
{
 "format_line": "EMOM 28",
 "scheme": "4 stations \u00d7 7 rounds",
 "movements": [
  {
   "reps": "10 cal",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "10 cal",
   "name": "Bike Erg",
   "load_kg": null,
   "equipment": [
    "Bike Erg"
   ]
  },
  {
   "reps": "8 cal",
   "name": "Ski Erg",
   "load_kg": null,
   "equipment": [
    "Ski Erg"
   ]
  },
  {
   "reps": "6 cal",
   "name": "Assault Bike",
   "load_kg": null,
   "equipment": [
    "Assault Bike"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Rower",
  "Bike Erg",
  "Ski Erg",
  "Assault Bike"
 ]
}
```

## Case 3
Inputs: style=Chipper, duration=30 min, equipment=['Bodyweight', 'Barbell', 'Kettlebell', 'Pull-up Bar', 'Rower']
### Candidate A
```json
{
 "format_line": "Chipper \u00b7 cap 30 min",
 "scheme": null,
 "movements": [
  {
   "reps": "80 cal",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "60",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "50",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "40",
   "name": "Deadlift",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "30",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "25",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "20",
   "name": "Power Clean",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
   ]
  }
 ],
 "notes": "Hold a steady, sustainable pace on the row and never stand still. Break pull-ups and toes-to-bar into small sets early, before your grip fails.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Kettlebell",
  "Pull-up Bar",
  "Rower"
 ]
}
```
### Candidate B
```json
{
 "format_line": "Chipper \u00b7 cap 30 min",
 "scheme": null,
 "movements": [
  {
   "reps": "50",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "40",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "800 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "30",
   "name": "Sumo Deadlift High Pull",
   "load_kg": "30 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "25",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "20",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "15",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "12",
   "name": "Goblet Squat",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Kettlebell",
  "Pull-up Bar",
  "Rower"
 ]
}
```
### Candidate C
```json
{
 "format_line": "Chipper \u00b7 cap 30 min",
 "scheme": null,
 "movements": [
  {
   "reps": "1000 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "40",
   "name": "Kettlebell Swing",
   "load_kg": "16 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "30",
   "name": "Deadlift",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "30",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "24",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "20",
   "name": "Hang Power Clean",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "16",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "10",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Keep moving at a steady pace: break pull-ups and toes-to-bar into small sets early, before failure forces it.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Kettlebell",
  "Pull-up Bar",
  "Rower"
 ]
}
```

## Case 4
Inputs: style=AMRAP, duration=20 min, equipment=['Bodyweight', 'Dumbbells', 'Kettlebell']
### Candidate A
```json
{
 "format_line": "AMRAP 20 min",
 "scheme": null,
 "movements": [
  {
   "reps": "6/arm",
   "name": "Dumbbell Snatch",
   "load_kg": "15 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "8/leg",
   "name": "Goblet Lunge",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "10",
   "name": "Hand-Release Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
   "name": "Kettlebell Clean",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "8",
   "name": "Devil Press",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Dumbbells",
  "Kettlebell"
 ]
}
```
### Candidate B
```json
{
 "format_line": "AMRAP 20 min",
 "scheme": null,
 "movements": [
  {
   "reps": "10",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "8/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "6",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Heavy, grindy pace: swings in two sets, take your breaks during the lunges and keep burpees steady. Aim for about 4 minutes per round.",
 "equipment_used": [
  "Bodyweight",
  "Dumbbells",
  "Kettlebell"
 ]
}
```
### Candidate C
```json
{
 "format_line": "AMRAP 20 min",
 "scheme": null,
 "movements": [
  {
   "reps": "8/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells",
    "Bodyweight"
   ]
  },
  {
   "reps": "8",
   "name": "Hand-Release Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "6",
   "name": "Devil Press",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells"
   ]
  }
 ],
 "notes": "Round takes about 3:15. Hold a steady pace on the lunges and push-ups so the devil presses stay moving.",
 "equipment_used": [
  "Bodyweight",
  "Dumbbells",
  "Kettlebell"
 ]
}
```

## Case 5
Inputs: style=For Time, duration=25 min, equipment=['Bodyweight', 'Barbell', 'Pull-up Bar']
### Candidate A
```json
{
 "format_line": "For Time \u00b7 cap 28 min",
 "scheme": "5 Rounds",
 "movements": [
  {
   "reps": "12",
   "name": "Front-Rack Lunge",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "8",
   "name": "Chest-to-Bar Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "10",
   "name": "Deadlift",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "10",
   "name": "Hand-Release Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Pull-up Bar"
 ]
}
```
### Candidate B
```json
{
 "format_line": "For Time \u00b7 cap 32 min",
 "scheme": "7 Rounds",
 "movements": [
  {
   "reps": "8/leg",
   "name": "Front-Rack Lunge",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "10",
   "name": "Deadlift",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "12",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "12",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Clean the bar to the front rack once per round and lunge in two sets of 8. Break the pull-ups early to stay ahead of the burpees.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Pull-up Bar"
 ]
}
```
### Candidate C
```json
{
 "format_line": "For Time \u00b7 cap 33 min",
 "scheme": "6 Rounds",
 "movements": [
  {
   "reps": "10",
   "name": "Deadlift",
   "load_kg": "90 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "12/leg",
   "name": "Reverse Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "12",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Deadlifts in two sets of 5 with short breaks. Keep lunges steady and the pull-ups in 2\u20133 sets so grip and legs last all six rounds.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Pull-up Bar"
 ]
}
```

## Case 6
Inputs: style=AMRAP, duration=45 min, equipment=['Bodyweight', 'Barbell', 'Dumbbells', 'Kettlebell', 'Pull-up Bar', 'Rings', 'Rower', 'Jump Rope', 'Plyo Box', 'Wall Ball', 'Running']
### Candidate A
```json
{
 "format_line": "AMRAP 45 min",
 "scheme": null,
 "movements": [
  {
   "reps": "250 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "6",
   "name": "Deadlift",
   "load_kg": "80 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "6",
   "name": "Burpee Box Jump-Over",
   "load_kg": null,
   "equipment": [
    "Bodyweight",
    "Plyo Box"
   ]
  },
  {
   "reps": "10",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "6",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "200 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  }
 ],
 "notes": "Steady, grinding pace: hold the same round time for 45 minutes. Break deadlifts and pull-ups early rather than failing late, and use the row and run to recover.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Kettlebell",
  "Pull-up Bar",
  "Rower",
  "Plyo Box",
  "Running"
 ]
}
```
### Candidate B
```json
{
 "format_line": "AMRAP 45 min",
 "scheme": null,
 "movements": [
  {
   "reps": "250 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "6",
   "name": "Deadlift",
   "load_kg": "80 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "6",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "200 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  },
  {
   "reps": "10",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "6",
   "name": "Box Jump",
   "load_kg": null,
   "equipment": [
    "Plyo Box"
   ]
  },
  {
   "reps": "6",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Round is about 4:30. Hold a steady pace on the row and run, and keep the deadlifts as quick singles-to-doubles, not a grind to failure. Break the pull-ups early.",
 "equipment_used": [
  "Rower",
  "Barbell",
  "Pull-up Bar",
  "Running",
  "Kettlebell",
  "Plyo Box",
  "Bodyweight"
 ]
}
```
### Candidate C
```json
{
 "format_line": "AMRAP 45 min",
 "scheme": null,
 "movements": [
  {
   "reps": "250 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "6",
   "name": "Deadlift",
   "load_kg": "80 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "200 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  },
  {
   "reps": "8",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "6",
   "name": "Dumbbell Box Step-Up",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells",
    "Plyo Box"
   ]
  },
  {
   "reps": "30",
   "name": "Double-Under",
   "load_kg": null,
   "equipment": [
    "Jump Rope"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Rower",
  "Barbell",
  "Running",
  "Pull-up Bar",
  "Dumbbells",
  "Plyo Box",
  "Jump Rope"
 ]
}
```

## Case 7
Inputs: style=For Time, duration=15 min, equipment=['Bodyweight', 'Barbell', 'Dumbbells']
Athlete request: 'no overhead today'
### Candidate A
```json
{
 "format_line": "For Time \u00b7 cap 20 min",
 "scheme": "6 Rounds",
 "movements": [
  {
   "reps": "10",
   "name": "Deadlift",
   "load_kg": "70 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "10",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "8/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "2\u00d712.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  }
 ],
 "notes": "Move steadily from the first round and keep the burpees non-stop. Your breathing will fail before your legs do, so don't sprint the early rounds.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Dumbbells"
 ]
}
```
### Candidate B
```json
{
 "format_line": "For Time \u00b7 cap 20 min",
 "scheme": "6 Rounds",
 "movements": [
  {
   "reps": "12",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
   "name": "Deadlift",
   "load_kg": "70 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "8/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "2\u00d712.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  }
 ],
 "notes": "Move steadily on the burpees and keep your breathing under control; the deadlifts should be quick touch-and-go sets of 10 and the lunges unbroken if you can.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Dumbbells"
 ]
}
```
### Candidate C
```json
{
 "format_line": "For Time \u00b7 cap 18 min",
 "scheme": "5 Rounds",
 "movements": [
  {
   "reps": "10",
   "name": "Dumbbell Deadlift",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "8",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "6",
   "name": "Power Clean",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "10",
   "name": "Walking Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Dumbbells"
 ]
}
```

## Case 8
Inputs: style=AMRAP, duration=12 min, equipment=['Bodyweight', 'Kettlebell', 'Pull-up Bar']
Athlete request: 'no overhead'
### Candidate A
```json
{
 "format_line": "AMRAP 12 min",
 "scheme": null,
 "movements": [
  {
   "reps": "6",
   "name": "Chest-to-Bar Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "8",
   "name": "Kettlebell Deadlift",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "10",
   "name": "Hand-Release Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "8",
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "6",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Kettlebell",
  "Pull-up Bar"
 ]
}
```
### Candidate B
```json
{
 "format_line": "AMRAP 12 min",
 "scheme": null,
 "movements": [
  {
   "reps": "6",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "8",
   "name": "Kettlebell Deadlift",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "6",
   "name": "Kettlebell Clean",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "6",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Grindy pace: pull-ups in one or two sets, rest on the bell rather than the bar. Cleans stop at the shoulder, nothing goes overhead.",
 "equipment_used": [
  "Bodyweight",
  "Kettlebell",
  "Pull-up Bar"
 ]
}
```
### Candidate C
```json
{
 "format_line": "AMRAP 12 min",
 "scheme": null,
 "movements": [
  {
   "reps": "5",
   "name": "Chest-to-Bar Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "8",
   "name": "Kettlebell Deadlift",
   "load_kg": "28 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "6",
   "name": "Goblet Squat",
   "load_kg": "28 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "8",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Round takes about 2 minutes. Break the pull-ups into two sets early, keep the deadlifts steady, and settle into a rhythm on the burpees.",
 "equipment_used": [
  "Bodyweight",
  "Kettlebell",
  "Pull-up Bar"
 ]
}
```

## Case 9
Inputs: style=Intervals, duration=15 min, equipment=['Running', 'Bodyweight']
### Candidate A
```json
{
 "format_line": "5 \u00d7 2 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "200 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  },
  {
   "reps": "8",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Steady pace, keep moving through the full window.",
 "equipment_used": [
  "Running",
  "Bodyweight"
 ]
}
```
### Candidate B
```json
{
 "format_line": "5 \u00d7 2 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "150 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  },
  {
   "reps": "12",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "5",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "One pass per interval takes about 1:45: roughly 45 s run, 27 s sit-ups, 20 s burpees, plus transitions. Hold a steady pace and keep moving; use the spare 15 s to reset.",
 "equipment_used": [
  "Running",
  "Bodyweight"
 ]
}
```
### Candidate C
```json
{
 "format_line": "5 \u00d7 2 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "200 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  },
  {
   "reps": "12",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "6",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Steady pace, never stand still. Run 200 m in about 60 s, then move straight into sit-ups and keep burpees smooth. Work takes roughly 1:45, leaving a few seconds of buffer before the rest.",
 "equipment_used": [
  "Running",
  "Bodyweight"
 ]
}
```

## Case 10
Inputs: style=AMRAP, duration=16 min, equipment=['Kettlebell', 'Dumbbells', 'Bodyweight']
### Candidate A
```json
{
 "format_line": "AMRAP 16 min",
 "scheme": null,
 "movements": [
  {
   "reps": "15",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "10",
   "name": "Dumbbell Snatch",
   "load_kg": "15 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "10",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "12",
   "name": "Dumbbell Deadlift",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Kettlebell",
  "Dumbbells",
  "Bodyweight"
 ]
}
```
### Candidate B
```json
{
 "format_line": "AMRAP 16 min",
 "scheme": null,
 "movements": [
  {
   "reps": "12",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "8",
   "name": "Dumbbell Snatch",
   "load_kg": "15 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "6",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Swings unbroken, snatches in two sets, and keep the burpees steady so your breathing never fully redlines. Hold a pace you can repeat for 16 minutes.",
 "equipment_used": [
  "Kettlebell",
  "Dumbbells",
  "Bodyweight"
 ]
}
```
### Candidate C
```json
{
 "format_line": "AMRAP 16 min",
 "scheme": null,
 "movements": [
  {
   "reps": "12",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "8",
   "name": "Devil Press",
   "load_kg": "2\u00d712.5 kg",
   "equipment": [
    "Dumbbells",
    "Bodyweight"
   ]
  },
  {
   "reps": "12",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Swings unbroken, fast hinge. Breathing is the limiter, so keep the devil presses steady and move through the burpees without stopping. Expect about 3 minutes per round.",
 "equipment_used": [
  "Kettlebell",
  "Dumbbells",
  "Bodyweight"
 ]
}
```