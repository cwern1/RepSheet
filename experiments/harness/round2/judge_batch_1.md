## Case 1
Inputs: style=EMOM, duration=7 min, equipment=['Bodyweight']
### Candidate A
```json
{
 "format_line": "EMOM 7",
 "scheme": "7 stations \u00d7 1 round",
 "movements": [
  {
   "reps": "12",
   "name": "Hand-Release Push-up",
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
   "name": "Broad Jump",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
   "reps": "20",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
  "Bodyweight"
 ]
}
```
### Candidate B
```json
{
 "format_line": "EMOM 7",
 "scheme": "7 stations \u00d7 1 round",
 "movements": [
  {
   "reps": "10",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
   "reps": "10",
   "name": "Jumping Lunge",
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
   "reps": "10",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
   "name": "Broad Jump",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
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
### Candidate C
```json
{
 "format_line": "EMOM 7",
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
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "16",
   "name": "Walking Lunge",
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
   "reps": "12",
   "name": "Push-up",
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
  },
  {
   "reps": "1 min",
   "name": "Rest",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "7 stations. Perform each movement once for 1 minute.",
 "equipment_used": [
  "Bodyweight"
 ]
}
```
### Candidate D
GENERATION FAILED: The model kept using equipment the athlete does not have: Chin-up, Ring Dip

## Case 2
Inputs: style=EMOM, duration=30 min, equipment=['Rower', 'Bike Erg', 'Ski Erg', 'Assault Bike']
### Candidate A
```json
{
 "format_line": "EMOM 30",
 "scheme": "4 stations \u00d7 5 rounds",
 "movements": [
  {
   "reps": "200 m",
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
   "reps": "10 cal",
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
### Candidate B
```json
{
 "format_line": "EMOM 30",
 "scheme": "6 stations \u00d7 5 rounds",
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
   "reps": "8 cal",
   "name": "Bike Erg",
   "load_kg": null,
   "equipment": [
    "Bike Erg"
   ]
  },
  {
   "reps": "10 cal",
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
  },
  {
   "reps": "120 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "6 cal",
   "name": "Bike Erg",
   "load_kg": null,
   "equipment": [
    "Bike Erg"
   ]
  }
 ],
 "notes": "The workout consists of 6 stations repeated for 5 rounds. Focus on steady machine output to maintain the EMOM rhythm.",
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
   "reps": "10 cal",
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
### Candidate D
GENERATION FAILED: The model kept using equipment the athlete does not have: Burpee Pull-up

## Case 3
Inputs: style=Chipper, duration=30 min, equipment=['Bodyweight', 'Barbell', 'Kettlebell', 'Pull-up Bar', 'Rower']
### Candidate A
```json
{
 "format_line": "Chipper \u00b7 cap 33 min",
 "scheme": null,
 "movements": [
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
   "name": "Bar-Facing Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight",
    "Barbell"
   ]
  },
  {
   "reps": "30",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "250 m",
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
   "name": "Goblet Squat",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell",
    "Bodyweight"
   ]
  },
  {
   "reps": "15",
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
   "reps": "1000 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
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
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "40",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "35",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "30",
   "name": "Bar-Facing Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight",
    "Barbell"
   ]
  },
  {
   "reps": "25",
   "name": "Deadlift",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "20",
   "name": "Power Clean",
   "load_kg": "60 kg",
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
   "reps": "50",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "40",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "30",
   "name": "Deadlift",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "25",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "15",
   "name": "Chin-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "10/arm",
   "name": "Kettlebell Snatch",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
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
 "notes": "Steady, unrelenting pace. Avoid redlining on the Row or Pull-ups.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Kettlebell",
  "Pull-up Bar",
  "Rower"
 ]
}
```
### Candidate D
```json
{
 "format_line": "Chipper \u00b7 cap 30 min",
 "scheme": null,
 "movements": [
  {
   "reps": "30",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "25",
   "name": "Chin-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "20",
   "name": "Kettlebell Clean",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "15",
   "name": "Kettlebell Snatch",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "12",
   "name": "Deadlift",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "10",
   "name": "Front Squat",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "8",
   "name": "Push Press",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "500 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
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
   "reps": "12/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "10",
   "name": "Kettlebell Snatch",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
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
   "reps": "5/arm",
   "name": "Dumbbell Snatch",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "6/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "22.5 kg",
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
   "reps": "10",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "12",
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
   "reps": "6/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells",
    "Bodyweight"
   ]
  },
  {
   "reps": "6",
   "name": "Goblet Squat",
   "load_kg": "22.5 kg",
   "equipment": [
    "Kettlebell",
    "Bodyweight"
   ]
  },
  {
   "reps": "6",
   "name": "Kettlebell Snatch",
   "load_kg": "22.5 kg",
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
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Dumbbells",
  "Kettlebell"
 ]
}
```
### Candidate D
```json
{
 "format_line": "AMRAP 20 min",
 "scheme": null,
 "movements": [
  {
   "reps": "12/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "12/leg",
   "name": "Goblet Lunge",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
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
   "reps": "21",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "15",
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

## Case 5
Inputs: style=For Time, duration=25 min, equipment=['Bodyweight', 'Barbell', 'Pull-up Bar']
### Candidate A
```json
{
 "format_line": "For Time \u00b7 cap 28 min",
 "scheme": "5 Rounds",
 "movements": [
  {
   "reps": "5",
   "name": "Deadlift",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "12/leg",
   "name": "Walking Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
   "reps": "5",
   "name": "Front Squat",
   "load_kg": "50 kg",
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
   "reps": "8",
   "name": "Chin-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "5",
   "name": "Push Press",
   "load_kg": "50 kg",
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
   "reps": "12/leg",
   "name": "Walking Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "9",
   "name": "Deadlift",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "9",
   "name": "Pull-up",
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
### Candidate C
```json
{
 "format_line": "For Time \u00b7 cap 28 min",
 "scheme": null,
 "movements": [
  {
   "reps": "30",
   "name": "Deadlift",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
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
   "name": "Front Squat",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "40",
   "name": "Walking Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "15",
   "name": "Chin-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "10",
   "name": "Push Press",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Barbell",
  "Bodyweight",
  "Pull-up Bar"
 ]
}
```
### Candidate D
```json
{
 "format_line": "For Time \u00b7 cap 28 min",
 "scheme": "6 Rounds",
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
   "reps": "8/leg",
   "name": "Front-Rack Lunge",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "6",
   "name": "Deadlift",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "6",
   "name": "Bar-Facing Burpee",
   "load_kg": null,
   "equipment": [
    "Barbell",
    "Bodyweight"
   ]
  },
  {
   "reps": "12",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "12",
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
   "reps": "5",
   "name": "Deadlift",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "20",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
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
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "15",
   "name": "Wall Ball",
   "load_kg": "9 kg",
   "equipment": [
    "Wall Ball"
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
   "reps": "50",
   "name": "Double-Under",
   "load_kg": null,
   "equipment": [
    "Jump Rope"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Dumbbells",
  "Kettlebell",
  "Pull-up Bar",
  "Rower",
  "Jump Rope",
  "Wall Ball"
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
   "reps": "100 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  },
  {
   "reps": "3",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "2/arm",
   "name": "Dumbbell Snatch",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "5",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "3",
   "name": "Deadlift",
   "load_kg": "70 kg",
   "equipment": [
    "Barbell"
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
  "Rower",
  "Running",
  "Pull-up Bar",
  "Dumbbells",
  "Kettlebell",
  "Barbell",
  "Jump Rope"
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
   "reps": "10",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
   "name": "Dumbbell Box Step-Up",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells",
    "Plyo Box"
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
   "reps": "15",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
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
 "notes": "Target round duration is 3-4 minutes. Prioritize movement density over sprint speed.",
 "equipment_used": [
  "Rower",
  "Bodyweight",
  "Dumbbells",
  "Plyo Box",
  "Pull-up Bar",
  "Kettlebell",
  "Running"
 ]
}
```
### Candidate D
GENERATION FAILED: Equipment not used: Dumbbells, Rings, Jump Rope, Plyo Box, Wall Ball, Running

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
   "reps": "15",
   "name": "Deadlift",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "12/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "21",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "15",
   "name": "Bar-Facing Burpee",
   "load_kg": "60 kg",
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
   "reps": "15",
   "name": "Sumo Deadlift High Pull",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
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
 "scheme": "3 Rounds",
 "movements": [
  {
   "reps": "12",
   "name": "Deadlift",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "20",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "30",
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
  "Dumbbells"
 ]
}
```
### Candidate C
```json
{
 "format_line": "For Time \u00b7 cap 18 min",
 "scheme": "4 Rounds",
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
   "reps": "8/leg",
   "name": "Front-Rack Lunge",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "12",
   "name": "Push-up",
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
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Dumbbells"
 ]
}
```
### Candidate D
```json
{
 "format_line": "For Time \u00b7 cap 18 min",
 "scheme": null,
 "movements": [
  {
   "reps": "40",
   "name": "Dumbbell Clean",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
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
   "name": "Front Squat",
   "load_kg": "60 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "20/leg",
   "name": "Dumbbell Front-Rack Lunge",
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
   "reps": "10",
   "name": "Kettlebell Deadlift",
   "load_kg": "24 kg",
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
  },
  {
   "reps": "15",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
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
   "name": "Kettlebell Deadlift",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "9",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "12",
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
### Candidate C
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
   "reps": "10",
   "name": "Kettlebell Deadlift",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "12",
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "15",
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
  "Kettlebell",
  "Pull-up Bar"
 ]
}
```
### Candidate D
```json
{
 "format_line": "AMRAP 12 min",
 "scheme": null,
 "movements": [
  {
   "reps": "10",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "6",
   "name": "Kettlebell Deadlift",
   "load_kg": "24 kg",
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
   "reps": "6",
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "10",
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

## Case 9
Inputs: style=Intervals, duration=15 min, equipment=['Running', 'Bodyweight']
### Candidate A
```json
{
 "format_line": "8 \u00d7 2 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "20",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
   "reps": "20",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
 "notes": "Maintain a steady pace throughout each interval. Focus on core engagement during sit-ups and push-ups.",
 "equipment_used": [
  "Running",
  "Bodyweight"
 ]
}
```
### Candidate B
```json
{
 "format_line": "4 x 3 min on / 1 min rest",
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
   "reps": "25",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "The work should take approximately 2:45 per interval. Maintain a steady pace.",
 "equipment_used": [
  "Running",
  "Bodyweight"
 ]
}
```
### Candidate C
```json
{
 "format_line": "3 \u00d7 4 min on / 1 min rest",
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
   "name": "Burpee",
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
### Candidate D
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
  },
  {
   "reps": "12/leg",
   "name": "Walking Lunge",
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
   "reps": "12",
   "name": "Dumbbell Deadlift",
   "load_kg": "22.5 kg",
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
   "reps": "12/leg",
   "name": "Goblet Lunge",
   "load_kg": "20 kg",
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
### Candidate C
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
   "name": "Dumbbell Deadlift",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
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
  "Kettlebell",
  "Dumbbells",
  "Bodyweight"
 ]
}
```
### Candidate D
```json
{
 "format_line": "AMRAP 16 min",
 "scheme": null,
 "movements": [
  {
   "reps": "21",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "12/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
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
   "name": "Kettlebell Deadlift",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "10",
   "name": "Dumbbell Thruster",
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