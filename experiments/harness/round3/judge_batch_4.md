## Case 31
Inputs: style=EMOM, duration=14 min, equipment=['Kettlebell', 'Dumbbells']
### Candidate A
```json
{
 "format_line": "EMOM 14",
 "scheme": "2 stations \u00d7 7 rounds",
 "movements": [
  {
   "reps": "10",
   "name": "Kettlebell Clean",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "50 m",
   "name": "Farmers Carry",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Kettlebell",
  "Dumbbells"
 ]
}
```
### Candidate B
```json
{
 "format_line": "EMOM 14",
 "scheme": "2 stations \u00d7 7 rounds",
 "movements": [
  {
   "reps": "16",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "6/arm",
   "name": "Dumbbell Snatch",
   "load_kg": "15 kg",
   "equipment": [
    "Dumbbells"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Kettlebell",
  "Dumbbells"
 ]
}
```

## Case 32
Inputs: style=EMOM, duration=24 min, equipment=['Bodyweight', 'Barbell', 'Assault Bike']
### Candidate A
```json
{
 "format_line": "EMOM 24",
 "scheme": "4 stations \u00d7 6 rounds",
 "movements": [
  {
   "reps": "16",
   "name": "Front Squat",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
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
   "reps": "10",
   "name": "Hand-Release Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "12",
   "name": "Deadlift",
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
  "Assault Bike"
 ]
}
```
### Candidate B
```json
{
 "format_line": "EMOM 24",
 "scheme": "4 stations \u00d7 6 rounds",
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
   "reps": "8",
   "name": "Deadlift",
   "load_kg": "80 kg",
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
   "reps": "12 cal",
   "name": "Assault Bike",
   "load_kg": null,
   "equipment": [
    "Assault Bike"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Assault Bike"
 ]
}
```

## Case 33
Inputs: style=Chipper, duration=15 min, equipment=['Bodyweight', 'Kettlebell']
### Candidate A
```json
{
 "format_line": "Chipper \u00b7 cap 15 min",
 "scheme": null,
 "movements": [
  {
   "reps": "50",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "45",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "40",
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "35/leg",
   "name": "Goblet Lunge",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "30",
   "name": "Kettlebell Clean",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "25",
   "name": "Kettlebell Push Press",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "20",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "15",
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
 "format_line": "Chipper \u00b7 cap 15 min",
 "scheme": null,
 "movements": [
  {
   "reps": "40",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "30",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "24",
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "20",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "16",
   "name": "Kettlebell Push Press",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
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
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Kettlebell"
 ]
}
```

## Case 34
Inputs: style=Chipper, duration=20 min, equipment=['Bodyweight', 'Dumbbells', 'Pull-up Bar', 'Jump Rope']
### Candidate A
```json
{
 "format_line": "Chipper \u00b7 cap 20 min",
 "scheme": null,
 "movements": [
  {
   "reps": "100",
   "name": "Double-Under",
   "load_kg": null,
   "equipment": [
    "Jump Rope"
   ]
  },
  {
   "reps": "60",
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
   "reps": "20",
   "name": "Dumbbell Push Press",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "12/arm",
   "name": "Dumbbell Snatch",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "10",
   "name": "Hanging Knee Raise",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "8",
   "name": "Burpee Pull-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight",
    "Pull-up Bar"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Bodyweight",
  "Dumbbells",
  "Pull-up Bar",
  "Jump Rope"
 ]
}
```
### Candidate B
```json
{
 "format_line": "Chipper \u00b7 cap 20 min",
 "scheme": null,
 "movements": [
  {
   "reps": "50",
   "name": "Double-Under",
   "load_kg": null,
   "equipment": [
    "Jump Rope"
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
   "reps": "24",
   "name": "Dumbbell Deadlift",
   "load_kg": "2\u00d722.5 kg",
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
   "reps": "16",
   "name": "Dumbbell Hang Clean & Jerk",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "12",
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
  "Dumbbells",
  "Pull-up Bar",
  "Jump Rope"
 ]
}
```

## Case 35
Inputs: style=Chipper, duration=25 min, equipment=['Barbell', 'Bodyweight', 'Rower', 'Wall Ball']
### Candidate A
```json
{
 "format_line": "Chipper \u00b7 cap 25 min",
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
   "reps": "45/leg",
   "name": "Walking Lunge",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "40",
   "name": "Wall Ball",
   "load_kg": "9 kg",
   "equipment": [
    "Wall Ball"
   ]
  },
  {
   "reps": "35",
   "name": "Front Squat",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
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
   "reps": "25",
   "name": "Power Clean",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
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
  "Barbell",
  "Bodyweight",
  "Rower",
  "Wall Ball"
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
   "name": "Wall Ball",
   "load_kg": "6 kg",
   "equipment": [
    "Wall Ball"
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
   "reps": "800 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "30",
   "name": "Hang Power Clean",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "25",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "20",
   "name": "Sumo Deadlift High Pull",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "15",
   "name": "Push Press",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Barbell",
  "Bodyweight",
  "Rower",
  "Wall Ball"
 ]
}
```

## Case 36
Inputs: style=Chipper, duration=35 min, equipment=['Bodyweight', 'Barbell', 'Dumbbells', 'Kettlebell', 'Pull-up Bar', 'Rings', 'Rower', 'Jump Rope', 'Plyo Box']
### Candidate A
```json
{
 "format_line": "Chipper \u00b7 cap 35 min",
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
   "reps": "100",
   "name": "Single-Under",
   "load_kg": null,
   "equipment": [
    "Jump Rope"
   ]
  },
  {
   "reps": "50",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "50",
   "name": "Box Jump-Over",
   "load_kg": null,
   "equipment": [
    "Plyo Box"
   ]
  },
  {
   "reps": "50",
   "name": "Ring Row",
   "load_kg": null,
   "equipment": [
    "Rings"
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
   "reps": "40",
   "name": "Hang Power Clean",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "40",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Rower",
  "Jump Rope",
  "Kettlebell",
  "Plyo Box",
  "Rings",
  "Pull-up Bar",
  "Barbell",
  "Bodyweight"
 ]
}
```
### Candidate B
```json
{
 "format_line": "Chipper \u00b7 cap 35 min",
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
   "reps": "80",
   "name": "Double-Under",
   "load_kg": null,
   "equipment": [
    "Jump Rope"
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
   "name": "Ring Row",
   "load_kg": null,
   "equipment": [
    "Rings"
   ]
  },
  {
   "reps": "35",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "30",
   "name": "Dumbbell Snatch",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "20",
   "name": "Deadlift",
   "load_kg": "80 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "15",
   "name": "Box Jump",
   "load_kg": null,
   "equipment": [
    "Plyo Box"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Rower",
  "Jump Rope",
  "Kettlebell",
  "Rings",
  "Pull-up Bar",
  "Dumbbells",
  "Barbell",
  "Plyo Box"
 ]
}
```

## Case 37
Inputs: style=Chipper, duration=45 min, equipment=['Bodyweight', 'Barbell', 'Kettlebell', 'Dumbbells', 'Pull-up Bar', 'Running']
### Candidate A
```json
{
 "format_line": "Chipper \u00b7 cap 45 min",
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
   "reps": "50",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "50",
   "name": "Deadlift",
   "load_kg": "60 kg",
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
   "reps": "50",
   "name": "Dumbbell Push Press",
   "load_kg": "2\u00d715 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "50",
   "name": "Goblet Lunge",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "800 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  },
  {
   "reps": "40",
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
  "Kettlebell",
  "Dumbbells",
  "Pull-up Bar",
  "Running"
 ]
}
```
### Candidate B
```json
{
 "format_line": "Chipper \u00b7 cap 45 min",
 "scheme": null,
 "movements": [
  {
   "reps": "50",
   "name": "Deadlift",
   "load_kg": "80 kg",
   "equipment": [
    "Barbell"
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
   "reps": "50",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "50",
   "name": "Dumbbell Clean",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "50",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "50",
   "name": "Front-Rack Lunge",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "50",
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "800 m",
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
  "Barbell",
  "Kettlebell",
  "Dumbbells",
  "Pull-up Bar",
  "Running"
 ]
}
```

## Case 38
Inputs: style=Chipper, duration=20 min, equipment=['Sandbag', 'Bodyweight', 'GHD']
### Candidate A
```json
{
 "format_line": "Chipper \u00b7 cap 20 min",
 "scheme": null,
 "movements": [
  {
   "reps": "50",
   "name": "GHD Sit-up",
   "load_kg": null,
   "equipment": [
    "GHD"
   ]
  },
  {
   "reps": "45",
   "name": "Sandbag Clean",
   "load_kg": "30 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "40",
   "name": "Bearhug Squat",
   "load_kg": "30 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "35",
   "name": "Shoulder-to-Shoulder Press",
   "load_kg": "30 kg",
   "equipment": [
    "Sandbag"
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
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "100 m",
   "name": "Sandbag Carry",
   "load_kg": null,
   "equipment": [
    "Sandbag"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Sandbag",
  "Bodyweight",
  "GHD"
 ]
}
```
### Candidate B
```json
{
 "format_line": "Chipper \u00b7 cap 20 min",
 "scheme": null,
 "movements": [
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
   "name": "Sandbag Clean",
   "load_kg": "30 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "25",
   "name": "Sandbag Lunge",
   "load_kg": "30 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "20",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "100 m",
   "name": "Sandbag Carry",
   "load_kg": "30 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "20",
   "name": "Shoulder-to-Shoulder Press",
   "load_kg": "30 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "20",
   "name": "GHD Sit-up",
   "load_kg": null,
   "equipment": [
    "GHD"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Sandbag",
  "Bodyweight",
  "GHD"
 ]
}
```

## Case 39
Inputs: style=Intervals, duration=12 min, equipment=['Bodyweight', 'Kettlebell']
### Candidate A
```json
{
 "format_line": "4 \u00d7 2 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "25",
   "name": "Kettlebell Swing",
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
 "format_line": "3 \u00d7 3 min on / 1 min rest",
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
   "name": "Goblet Lunge",
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
   "reps": "10",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Rest 1 min between intervals.",
 "equipment_used": [
  "Bodyweight",
  "Kettlebell"
 ]
}
```

## Case 40
Inputs: style=Intervals, duration=20 min, equipment=['Barbell', 'Bodyweight', 'Rower']
### Candidate A
```json
{
 "format_line": "4 \u00d7 4 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "12",
   "name": "Push Press",
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
  },
  {
   "reps": "8 cal",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "10",
   "name": "Hang Power Clean",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  }
 ],
 "notes": "Rest 1 min between intervals; repeat the same work every round.",
 "equipment_used": [
  "Barbell",
  "Bodyweight",
  "Rower"
 ]
}
```
### Candidate B
```json
{
 "format_line": "5 \u00d7 3 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "12",
   "name": "Push Press",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
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
   "reps": "200 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  }
 ],
 "notes": null,
 "equipment_used": [
  "Barbell",
  "Bodyweight",
  "Rower"
 ]
}
```