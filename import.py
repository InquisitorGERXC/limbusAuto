import os

template_files = [
    "images/map_choice.png",
    "images/map_normal_1.png"
]

for file in template_files:
    if os.path.exists(file):
        print(f"{file} exists.")
    else:
        print(f"{file} MISSING!")
