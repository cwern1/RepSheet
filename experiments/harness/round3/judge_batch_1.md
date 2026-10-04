## Case 1
Inputs: style=EMOM, duration=7 min, equipment=['Bodyweight']
### Candidate A
GENERATION FAILED: The model kept using equipment the athlete does not have: Pull-up
### Candidate B
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

## Case 2
Inputs: style=EMOM, duration=30 min, equipment=['Rower', 'Bike Erg', 'Ski Erg', 'Assault Bike']
### Candidate A
```json
{
 "format_line": "EMOM 30",
 "scheme": "4 stations \u00d7 7 rounds, plus 2 minutes Rest",
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
 "notes": "Rotate stations each minute for 28 minutes, then take the final 2 minutes easy.",
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
   "reps": "150 m",
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
   "reps": "150 m",
   "name": "Ski Erg",
   "load_kg": null,
   "equipment": [
    "Ski Erg"
   ]
  },
  {
   "reps": "8 cal",
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
   "reps": "2000 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "55",
   "name": "Deadlift",
   "load_kg": "80 kg",
   "equipment": [
    "Barbell"
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
   "reps": "45",
   "name": "Kettlebell Clean",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "44",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "40",
   "name": "Push Press",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
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
   "load_kg": "16 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "40",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "30",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
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
   "reps": "25",
   "name": "Hang Power Clean",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
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
   "name": "Goblet Lunge",
   "load_kg": "16 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "12",
   "name": "Push Press",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
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

## Case 4
Inputs: style=AMRAP, duration=20 min, equipment=['Bodyweight', 'Dumbbells', 'Kettlebell']
### Candidate A
```json
{
 "format_line": "AMRAP 20 min",
 "scheme": null,
 "movements": [
  {
   "reps": "5",
   "name": "Dumbbell Snatch",
   "load_kg": "22.5 kg",
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
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "8",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "8",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
   "reps": "6/arm",
   "name": "Dumbbell Snatch",
   "load_kg": "22.5 kg",
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
   "reps": "12",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "8",
   "name": "Dumbbell Deadlift",
   "load_kg": "2\u00d722.5 kg",
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

## Case 5
Inputs: style=For Time, duration=25 min, equipment=['Bodyweight', 'Barbell', 'Pull-up Bar']
### Candidate A
```json
{
 "format_line": "For Time \u00b7 cap 28 min",
 "scheme": "5 Rounds",
 "movements": [
  {
   "reps": "6",
   "name": "Deadlift",
   "load_kg": "60 kg",
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
   "reps": "6",
   "name": "Front-Rack Lunge",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
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
   "reps": "8",
   "name": "Bar-Facing Burpee",
   "load_kg": null,
   "equipment": [
    "Barbell"
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
 "format_line": "For Time \u00b7 cap 28 min",
 "scheme": "5 Rounds",
 "movements": [
  {
   "reps": "10/leg",
   "name": "Reverse Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "6",
   "name": "Deadlift",
   "load_kg": "60 kg",
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
   "reps": "6",
   "name": "Front Squat",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "10",
   "name": "Push-up",
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
   "name": "Ring Dip",
   "load_kg": null,
   "equipment": [
    "Rings"
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
   "reps": "6",
   "name": "Dumbbell Box Step-Up",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells",
    "Plyo Box"
   ]
  },
  {
   "reps": "6",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Rower",
  "Barbell",
  "Rings",
  "Running",
  "Dumbbells",
  "Plyo Box",
  "Pull-up Bar"
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
   "reps": "150 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
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
   "reps": "3",
   "name": "Deadlift",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "8",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "4",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "2",
   "name": "Ring Dip",
   "load_kg": null,
   "equipment": [
    "Rings"
   ]
  },
  {
   "reps": "20",
   "name": "Double-Under",
   "load_kg": null,
   "equipment": [
    "Jump Rope"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Barbell",
  "Kettlebell",
  "Pull-up Bar",
  "Rings",
  "Rower",
  "Jump Rope",
  "Running"
 ]
}
```

## Case 7
Inputs: style=For Time, duration=15 min, equipment=['Bodyweight', 'Barbell', 'Dumbbells']
Athlete request: 'no overhead today'
### Candidate A
```json
{
 "format_line": "For Time \u00b7 cap 18 min",
 "scheme": "5 Rounds",
 "movements": [
  {
   "reps": "10",
   "name": "Dumbbell Deadlift",
   "load_kg": "2\u00d722.5 kg",
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
   "reps": "8",
   "name": "Hang Power Clean",
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
### Candidate B
```json
{
 "format_line": "For Time \u00b7 cap 18 min",
 "scheme": "5 Rounds",
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
   "reps": "10",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "8",
   "name": "Bar-Facing Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight",
    "Barbell"
   ]
  },
  {
   "reps": "8",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "5",
   "name": "Deadlift",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
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
   "reps": "5",
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
   "reps": "12",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "15",
   "name": "Air Squat",
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
   "name": "Kettlebell Clean",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "10",
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
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
   "reps": "8",
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

## Case 9
Inputs: style=Intervals, duration=15 min, equipment=['Running', 'Bodyweight']
### Candidate A
```json
{
 "format_line": "5 \u00d7 2 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "100 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  },
  {
   "reps": "25 m",
   "name": "Bear Crawl",
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
  }
 ],
 "notes": null,
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
   "reps": "200 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  },
  {
   "reps": "10",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "8",
   "name": "Push-up",
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

## Case 10
Inputs: style=AMRAP, duration=16 min, equipment=['Kettlebell', 'Dumbbells', 'Bodyweight']
### Candidate A
```json
{
 "format_line": "AMRAP 16 min",
 "scheme": null,
 "movements": [
  {
   "reps": "20",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "12",
   "name": "Dumbbell Snatch",
   "load_kg": "15 kg",
   "equipment": [
    "Dumbbells"
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
   "reps": "15",
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
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