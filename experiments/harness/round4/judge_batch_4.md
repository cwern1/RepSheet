## Case 31
Inputs: style=EMOM, duration=14 min, equipment=['Kettlebell', 'Dumbbells']
### Candidate A
```json
{
 "format_line": "EMOM 14",
 "scheme": "2 stations \u00d7 7 rounds",
 "movements": [
  {
   "reps": "14",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
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
  }
 ],
 "notes": "Odd minutes swings, even minutes snatches (alternate arms each rep). Fast, unbroken sets so you earn 10-15 s of rest; grip will fade, so drop the bell early rather than fight for extra reps.",
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
   "reps": "12",
   "name": "Dumbbell Snatch",
   "load_kg": "15 kg",
   "equipment": [
    "Dumbbells"
   ]
  }
 ],
 "notes": "Dumbbell Snatch: alternate arms every rep.",
 "equipment_used": [
  "Kettlebell",
  "Dumbbells"
 ]
}
```
### Candidate C
```json
{
 "format_line": "EMOM 14",
 "scheme": "2 stations \u00d7 7 rounds",
 "movements": [
  {
   "reps": "14",
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
  }
 ],
 "notes": "Odd minutes swings, even minutes snatches (alternate arms each rep or switch halfway). Move fast and aim to finish in ~35 s so you can shake out your grip before the next minute.",
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
 "scheme": "3 stations \u00d7 8 rounds",
 "movements": [
  {
   "reps": "10",
   "name": "Front Squat",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
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
   "reps": "20",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Clean the bar from the floor to the front rack once, then keep the front squats unbroken. Bike hard for 7 cal (about 42 s) and use the remaining seconds to breathe before the air squats.",
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
 "scheme": "3 stations \u00d7 8 rounds",
 "movements": [
  {
   "reps": "10",
   "name": "Thruster",
   "load_kg": "30 kg",
   "equipment": [
    "Barbell"
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
   "reps": "16",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Thrusters in one or two sets, cleaning the bar from the floor each minute. Push the bike hard for 7 cal, then take your rest. Air squats should be one smooth unbroken set.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Assault Bike"
 ]
}
```
### Candidate C
```json
{
 "format_line": "EMOM 24",
 "scheme": "4 stations \u00d7 6 rounds",
 "movements": [
  {
   "reps": "14",
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
   "reps": "12",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
### Candidate B
```json
{
 "format_line": "Chipper \u00b7 cap 15 min",
 "scheme": null,
 "movements": [
  {
   "reps": "60",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "40",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "30",
   "name": "Goblet Squat",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "24",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "20/leg",
   "name": "Goblet Lunge",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "12/arm",
   "name": "Kettlebell Push Press",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "10/arm",
   "name": "Kettlebell Clean",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  }
 ],
 "notes": "The sit-ups are the big slot: start with sets of 15 and don't let them swallow your legs. Keep the trunk braced through the lunges and presses, and break the burpees before form slips.",
 "equipment_used": [
  "Bodyweight",
  "Kettlebell"
 ]
}
```
### Candidate C
```json
{
 "format_line": "Chipper \u00b7 cap 15 min",
 "scheme": null,
 "movements": [
  {
   "reps": "40",
   "name": "Kettlebell Swing",
   "load_kg": "24 kg",
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
   "reps": "24",
   "name": "Goblet Squat",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "16",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "20",
   "name": "Goblet Lunge",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "12",
   "name": "Kettlebell Push Press",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  }
 ],
 "notes": "Sit-ups are the core slot. Break swings and squats early into sets of 8-10.",
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
   "reps": "40",
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
   "name": "Dumbbell Snatch",
   "load_kg": "22.5 kg",
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
### Candidate B
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
   "reps": "50",
   "name": "Dumbbell Deadlift",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
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
   "reps": "16/arm",
   "name": "Dumbbell Snatch",
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
   "reps": "24",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "12/leg",
   "name": "Dumbbell Front-Rack Lunge",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "20",
   "name": "Chin-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  }
 ],
 "notes": "Pull-ups, toes-to-bar and chin-ups are the grind: break them early into small sets of 4-6 to keep your grip alive. Move steadily through the dumbbell work.",
 "equipment_used": [
  "Bodyweight",
  "Dumbbells",
  "Pull-up Bar",
  "Jump Rope"
 ]
}
```
### Candidate C
```json
{
 "format_line": "Chipper \u00b7 cap 20 min",
 "scheme": null,
 "movements": [
  {
   "reps": "40",
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
   "name": "Dumbbell Snatch",
   "load_kg": "22.5 kg",
   "equipment": [
    "Dumbbells"
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
   "reps": "20",
   "name": "Dumbbell Deadlift",
   "load_kg": "2\u00d722.5 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "16",
   "name": "Chest-to-Bar Pull-up",
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
 "notes": "Break pull-ups early into sets of 5-6 and keep rests short. The snatches and deadlifts are heavy, so use small sets and save your grip for the bar work.",
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
   "reps": "50",
   "name": "Wall Ball",
   "load_kg": "6 kg",
   "equipment": [
    "Wall Ball"
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
   "reps": "40",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
   "name": "Push Press",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
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
   "reps": "2000 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "80",
   "name": "Wall Ball",
   "load_kg": "9 kg",
   "equipment": [
    "Wall Ball"
   ]
  },
  {
   "reps": "60",
   "name": "Deadlift",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
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
   "reps": "30",
   "name": "Sit-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "20",
   "name": "Power Clean",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "20",
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Row at a pace you could hold for 30 minutes, and break wall balls and deadlifts into sets of 10-15 before your breathing spikes. Burpees are where the workout is won or lost.",
 "equipment_used": [
  "Barbell",
  "Bodyweight",
  "Rower",
  "Wall Ball"
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
   "reps": "50 cal",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
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
   "reps": "30",
   "name": "Air Squat",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "24",
   "name": "Power Clean",
   "load_kg": "40 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "18",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
 "notes": "Hold a pace on the rower you can breathe through, then break wall balls and cleans early into small sets. Keep moving through the burpees.",
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
   "reps": "100 cal",
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
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  },
  {
   "reps": "40",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "40",
   "name": "Deadlift",
   "load_kg": "70 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "30",
   "name": "Burpee Box Jump-Over",
   "load_kg": null,
   "equipment": [
    "Bodyweight",
    "Plyo Box"
   ]
  },
  {
   "reps": "30",
   "name": "Ring Row",
   "load_kg": null,
   "equipment": [
    "Rings"
   ]
  },
  {
   "reps": "20",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  }
 ],
 "notes": "Row at a steady pace you could hold for 10 minutes, since the lungs decide this one. Break pull-ups early in sets of 8-10, and settle your breathing before the burpee box jump-overs.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Kettlebell",
  "Pull-up Bar",
  "Rings",
  "Rower",
  "Jump Rope",
  "Plyo Box"
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
   "reps": "2000 m",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "150",
   "name": "Double-Under",
   "load_kg": null,
   "equipment": [
    "Jump Rope"
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
   "name": "Burpee Box Jump-Over",
   "load_kg": null,
   "equipment": [
    "Bodyweight",
    "Plyo Box"
   ]
  },
  {
   "reps": "40",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "30",
   "name": "Ring Row",
   "load_kg": null,
   "equipment": [
    "Rings"
   ]
  },
  {
   "reps": "20",
   "name": "Thruster",
   "load_kg": "35 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "15",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  }
 ],
 "notes": "Row steady at a pace you could hold for 10 more minutes, then pace the burpee box jump-overs so your breathing stays under control. Break pull-ups early into small sets.",
 "equipment_used": [
  "Bodyweight",
  "Barbell",
  "Kettlebell",
  "Pull-up Bar",
  "Rings",
  "Rower",
  "Jump Rope",
  "Plyo Box"
 ]
}
```
### Candidate C
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
   "name": "Double-Under",
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
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
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
  "Pull-up Bar",
  "Plyo Box",
  "Rings",
  "Barbell",
  "Bodyweight"
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
   "reps": "800 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
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
   "reps": "40",
   "name": "Deadlift",
   "load_kg": "50 kg",
   "equipment": [
    "Barbell"
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
   "reps": "30",
   "name": "Dumbbell Snatch",
   "load_kg": "15 kg",
   "equipment": [
    "Dumbbells"
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
   "reps": "20",
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Hinge-heavy: take steady sets of 15\u201320 on the swings and deadlifts, and keep your grip fresh for the pull-ups and snatches. Break the burpees early.",
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
   "reps": "1600 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
   ]
  },
  {
   "reps": "150",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  },
  {
   "reps": "120",
   "name": "Deadlift",
   "load_kg": "70 kg",
   "equipment": [
    "Barbell"
   ]
  },
  {
   "reps": "40/arm",
   "name": "Dumbbell Snatch",
   "load_kg": "15 kg",
   "equipment": [
    "Dumbbells"
   ]
  },
  {
   "reps": "60",
   "name": "Pull-up",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
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
   "reps": "40",
   "name": "Toes-to-Bar",
   "load_kg": null,
   "equipment": [
    "Pull-up Bar"
   ]
  }
 ],
 "notes": "Run the first 1600 m easy. Take swings and deadlifts in planned sets of 15-25 with short breaks. Grip and hamstrings will fade, so keep the pull-ups in small, quick sets.",
 "equipment_used": [
  "Running",
  "Kettlebell",
  "Barbell",
  "Dumbbells",
  "Pull-up Bar",
  "Bodyweight"
 ]
}
```
### Candidate C
```json
{
 "format_line": "Chipper \u00b7 cap 45 min",
 "scheme": null,
 "movements": [
  {
   "reps": "800 m",
   "name": "Run",
   "load_kg": null,
   "equipment": [
    "Running"
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
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
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
   "reps": "45",
   "name": "Dumbbell Snatch",
   "load_kg": "15 kg",
   "equipment": [
    "Dumbbells"
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
   "name": "Toes-to-Bar",
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
   "reps": "40",
   "name": "Walking Lunge",
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
   "name": "Bearhug Squat",
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
   "reps": "50",
   "name": "GHD Sit-up",
   "load_kg": null,
   "equipment": [
    "GHD"
   ]
  },
  {
   "reps": "40",
   "name": "Sandbag Clean",
   "load_kg": "20 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "30",
   "name": "Bearhug Squat",
   "load_kg": "20 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "15/leg",
   "name": "Sandbag Lunge",
   "load_kg": "20 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "24",
   "name": "Shoulder-to-Shoulder Press",
   "load_kg": "20 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "200 m",
   "name": "Sandbag Carry",
   "load_kg": "20 kg",
   "equipment": [
    "Sandbag"
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
   "name": "Push-up",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  }
 ],
 "notes": "Keep moving the whole way: break the GHD sit-ups into sets of 10 early, and take any rest during the carry rather than standing still.",
 "equipment_used": [
  "Sandbag",
  "Bodyweight",
  "GHD"
 ]
}
```
### Candidate C
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
   "reps": "40",
   "name": "Bearhug Squat",
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
   "reps": "100 m",
   "name": "Sandbag Carry",
   "load_kg": "30 kg",
   "equipment": [
    "Sandbag"
   ]
  },
  {
   "reps": "20",
   "name": "Sandbag Clean",
   "load_kg": "30 kg",
   "equipment": [
    "Sandbag"
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
   "reps": "10",
   "name": "Shoulder-to-Shoulder Press",
   "load_kg": "30 kg",
   "equipment": [
    "Sandbag"
   ]
  }
 ],
 "notes": "Break the GHD sit-ups into sets of 10 early and keep moving; never sit down between movements.",
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
  "Bodyweight",
  "Kettlebell"
 ]
}
```
### Candidate B
```json
{
 "format_line": "4 \u00d7 2 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "20",
   "name": "Kettlebell Swing",
   "load_kg": "20 kg",
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
   "reps": "8",
   "name": "Kettlebell Deadlift",
   "load_kg": "20 kg",
   "equipment": [
    "Kettlebell"
   ]
  }
 ],
 "notes": "One pass through all three movements per interval, finishing with about 15 s to spare. Go unbroken on the swings, move steadily through the burpees, and keep the deadlifts crisp when your grip and hamstrings are tired.",
 "equipment_used": [
  "Bodyweight",
  "Kettlebell"
 ]
}
```
### Candidate C
```json
{
 "format_line": "4 \u00d7 2 min on / 1 min rest",
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
   "name": "Burpee",
   "load_kg": null,
   "equipment": [
    "Bodyweight"
   ]
  },
  {
   "reps": "10",
   "name": "Kettlebell Deadlift",
   "load_kg": "24 kg",
   "equipment": [
    "Kettlebell"
   ]
  }
 ],
 "notes": "Do one pass through the list each interval at a sprint pace, then rest for whatever is left of the 2 minutes. Swings unbroken; keep the burpees moving so the deadlifts don't stall.",
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
 "format_line": "5 \u00d7 3 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "15 cal",
   "name": "Row",
   "load_kg": null,
   "equipment": [
    "Rower"
   ]
  },
  {
   "reps": "12",
   "name": "Thruster",
   "load_kg": "30 kg",
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
 "notes": "Do one round per interval, finishing in about 2:45 and resting in the time left. Pull hard on the row, go in quick sets of 6 on the thrusters, and break the burpees early rather than late.",
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
 "format_line": "4 \u00d7 4 min on / 1 min rest",
 "scheme": null,
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
   "reps": "8",
   "name": "Push Press",
   "load_kg": "30 kg",
   "equipment": [
    "Barbell"
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
 "notes": "Each interval is two rounds of the list, about 1:50 per round, finishing with a few seconds to spare. Row hard, do the push press in one or two quick sets, and keep the burpees moving. Start the next round straight away.",
 "equipment_used": [
  "Barbell",
  "Bodyweight",
  "Rower"
 ]
}
```
### Candidate C
```json
{
 "format_line": "4 \u00d7 4 min on / 1 min rest",
 "scheme": null,
 "movements": [
  {
   "reps": "10",
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
 "notes": "Rest 1 min between intervals; move fast and unbroken where possible.",
 "equipment_used": [
  "Barbell",
  "Bodyweight",
  "Rower"
 ]
}
```