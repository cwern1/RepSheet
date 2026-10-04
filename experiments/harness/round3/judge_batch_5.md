## Case 41
Inputs: style=Intervals, duration=24 min, equipment=['Dumbbells', 'Ski Erg', 'Bodyweight']
### Candidate A
```json
{
 "format_line": "6 \u00d7 3 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "8",
   "name": "Dumbbell Deadlift",
   "load_kg": "2\u00d720 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "10/leg",
   "name": "Reverse Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "12 cal",
   "name": "Ski Erg",
   "load_kg": null,
   "equipment": [
    "Ski Erg"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Dumbbells",
  "Ski Erg",
  "Bodyweight"
 ]
}
```
### Candidate B
```json
{
 "format_line": "4 \u00d7 5 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "10 cal",
   "name": "Ski Erg",
   "load_kg": null,
   "equipment": [
    "Ski Erg"
   ]
  },
  {
   "reps": "15",
   "name": "Dumbbell Deadlift",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "20",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
 "notes": "Rest 1 min after each 5 min window. Move steadily and keep every round the same.",
 "equipment_used": [
  "Dumbbells",
  "Ski Erg",
  "Bodyweight"
 ]
}
```

## Case 42
Inputs: style=Intervals, duration=30 min, equipment=['Bodyweight', 'Running', 'Pull-up Bar']
### Candidate A
```json
{
 "format_line": "6 \u00d7 4 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "30",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "20/leg",
   "name": "Walking Lunge",
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
   "reps": "200 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Pull-up Bar",
  "Running"
 ]
}
```
### Candidate B
```json
{
 "format_line": "6 \u00d7 4 min on / 1 min rest",
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
   "reps": "15",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
   "reps": "10/leg",
   "name": "Reverse Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Steady pace, keep moving through each window and rest the full minute between intervals.",
 "equipment_used": [
  "Bodyweight",
  "Running",
  "Pull-up Bar"
 ]
}
```

## Case 43
Inputs: style=Intervals, duration=16 min, equipment=['Assault Bike', 'Wall Ball', 'Bodyweight']
### Candidate A
```json
{
 "format_line": "4 \u00d7 3 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "8 cal",
   "name": "Assault Bike",
   "load_kg": null,
   "equipment": [
    "Assault Bike"
   ]
  },
  {
   "reps": "12",
   "name": "Wall Ball",
   "load_kg": "6 kg",
   "equipment": [
    "Wall Ball"
   ]
  },
  {
   "reps": "10",
   "name": "Walking Lunge",
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
 "notes": "Rest 1 min between rounds.",
 "equipment_used": [
  "Assault Bike",
  "Wall Ball",
  "Bodyweight"
 ]
}
```
### Candidate B
```json
{
 "format_line": "4 \u00d7 3 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "15",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "15",
   "name": "Wall Ball",
   "load_kg": "6 kg",
   "equipment": [
    "Wall Ball"
   ]
  },
  {
   "reps": "25 cal",
   "name": "Assault Bike",
   "load_kg": null,
   "equipment": [
    "Assault Bike"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Assault Bike",
  "Wall Ball",
  "Bodyweight"
 ]
}
```

## Case 44
Inputs: style=AMRAP, duration=15 min, equipment=['Bodyweight', 'Barbell', 'Dumbbells']
Athlete request: 'bad knee - nothing that loads a deep bend'
### Candidate A
```json
{
 "format_line": "AMRAP 15 min",
 "scheme": null,
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
   "reps": "12",
   "name": "Dumbbell Snatch",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "15",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "12",
   "name": "Dumbbell Push Press",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "20",
   "name": "Sit-up",
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
### Candidate B
```json
{
 "format_line": "AMRAP 15 min",
 "scheme": null,
 "movements": [
  {
   "reps": "10",
   "name": "Dumbbell Snatch",
   "load_kg": "15 kg",
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
   "reps": "10",
   "name": "Sumo Deadlift High Pull",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "12",
   "name": "Sit-up",
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

## Case 45
Inputs: style=For Time, duration=12 min, equipment=['Bodyweight', 'Kettlebell']
Athlete request: 'easy recovery day please'
### Candidate A
```json
{
 "format_line": "For Time \u00b7 cap 15 min",
 "scheme": "4 Rounds",
 "movements": [
  {
   "reps": "8",
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "12",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
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
   "reps": "12",
   "name": "Kettlebell Deadlift",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Kettlebell"
 ]
}
```
### Candidate B
```json
{
 "format_line": "For Time \u00b7 cap 15 min",
 "scheme": "4 Rounds",
 "movements": [
  {
   "reps": "8",
   "name": "Goblet Squat",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "10",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "12",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
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
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Kettlebell"
 ]
}
```

## Case 46
Inputs: style=EMOM, duration=12 min, equipment=['Bodyweight', 'Dumbbells']
Athlete request: 'I want devil press in there'
### Candidate A
```json
{
 "format_line": "EMOM 12",
 "scheme": "6 stations \u00d7 2 rounds",
 "movements": [
  {
   "reps": "5",
   "name": "Devil Press",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "5",
   "name": "Dumbbell Deadlift",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "6/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
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
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "12",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Dumbbells"
 ]
}
```
### Candidate B
```json
{
 "format_line": "EMOM 12",
 "scheme": "3 stations \u00d7 4 rounds",
 "movements": [
  {
   "reps": "8",
   "name": "Devil Press",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells"
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
   "reps": "12",
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
  "Dumbbells"
 ]
}
```

## Case 47
Inputs: style=Chipper, duration=25 min, equipment=['Bodyweight', 'Kettlebell', 'Pull-up Bar']
Athlete request: 'use the rower a lot'
### Candidate A
```json
{
 "format_line": "Chipper \u00b7 cap 25 min",
 "scheme": null,
 "movements": [
  {
   "reps": "50",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "45",
   "name": "Walking Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "40",
   "name": "Hanging Knee Raise",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "35",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "30",
   "name": "Kettlebell Snatch",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "6/arm",
   "name": "Turkish Get-Up",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "15",
   "name": "Hand-Release Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
 "format_line": "Chipper \u00b7 cap 25 min",
 "scheme": null,
 "movements": [
  {
   "reps": "50",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "25",
   "name": "Kettlebell Clean",
   "load_kg": "16 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "20",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "20",
   "name": "Goblet Lunge",
   "load_kg": "16 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "15",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "12",
   "name": "Chin-up",
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

## Case 48
Inputs: style=Intervals, duration=18 min, equipment=['Bodyweight']
Athlete request: 'no jumping, downstairs neighbours'
### Candidate A
```json
{
 "format_line": "3 \u00d7 5 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "20",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
   "reps": "20",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "12/leg",
   "name": "Reverse Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Repeat the same circuit as many times as the 5-minute window allows, then rest 1 minute.",
 "equipment_used": [
  "Bodyweight"
 ]
}
```
### Candidate B
```json
{
 "format_line": "3 \u00d7 5 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "30",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "20",
   "name": "Walking Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "25",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "30",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "25 m",
   "name": "Bear Crawl",
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

## Case 49
Inputs: style=AMRAP, duration=12 min, equipment=['Kettlebell', 'Bodyweight']
Avoid (recently used): ['Kettlebell Swing', 'Goblet Squat', 'Burpee', 'Push-up', 'Sit-up']
### Candidate A
```json
{
 "format_line": "AMRAP 12 min",
 "scheme": null,
 "movements": [
  {
   "reps": "12/leg",
   "name": "Goblet Lunge",
   "load_kg": "16 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "10",
   "name": "Kettlebell Push Press",
   "load_kg": "16 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "20",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
   "name": "Hand-Release Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Kettlebell",
  "Bodyweight"
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
   "reps": "15",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "8",
   "name": "Kettlebell Clean",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "6/leg",
   "name": "Goblet Lunge",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "8",
   "name": "Kettlebell Snatch",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Kettlebell",
  "Bodyweight"
 ]
}
```

## Case 50
Inputs: style=For Time, duration=15 min, equipment=['Bodyweight', 'Barbell', 'Pull-up Bar']
Avoid (recently used): ['Deadlift', 'Pull-up', 'Thruster', 'Push-up', 'Air Squat', 'Run']
### Candidate A
```json
{
 "format_line": "For Time \u00b7 cap 18 min",
 "scheme": "4 Rounds",
 "movements": [
  {
   "reps": "15",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "10",
   "name": "Front Squat",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "10",
   "name": "Hang Power Clean",
   "load_kg": "40 kg",
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
 "format_line": "For Time \u00b7 cap 18 min",
 "scheme": "3 Rounds",
 "movements": [
  {
   "reps": "12",
   "name": "Front Squat",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "12/leg",
   "name": "Front-Rack Lunge",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "12",
   "name": "Push Press",
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
   "reps": "30",
   "name": "Sit-up",
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
  "Pull-up Bar"
 ]
}
```