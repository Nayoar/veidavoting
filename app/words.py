words = [
  "apple", "river", "brave", "cloud", "crown", "tiger", "dream", "stone", "flame", "frost", "glow", "grape", "honey", "maple", "ivory", "cedar", "jolly", "pearl", "lemon", "magic", "mango", "misty", "novel", "olive", "piano", "quiet", "raven", "rocky", "royal", "ruby", "sage", "shell", "shiny", "smile", "snowy", "solar", "spice", "star", "sunny", "sweet", "ultra", "vivid", "water", "whale", "wild", "windy", "zebra", "acorn", "amber", "angel", "arrow", "baker", "beach", "berry", "bison", "blaze", "bloom", "brass", "brush", "cabin", "camel", "candy", "charm", "chess", "cliff", "cocoa", "coral", "crisp", "daisy", "delta", "eagle", "ember", "fairy", "fancy", "feast", "flock", "flute", "giant", "glade", "globe", "goose", "grace", "green", "hazel", "heart", "horse", "jewel", "koala", "laser", "lilac", "lotus", "lucky", "melon", "metal", "model", "music", "oasis", "ocean", "peach", "plant", "plaza", "pride", "prism", "puppy", "queen", "quick", "quiet", "ranch", "relay", "robin", "rose", "rusty", "salsa", "sandy", "satin", "scout", "sheep", "shine", "skate", "slate", "slope", "snail", "snake", "spark", "spear", "spoon", "sport", "spray", "stack", "stage", "stall", "stamp", "steam", "steel", "storm", "story", "straw", "sugar", "sushi", "swamp", "swing", "sword", "table", "toast", "torch", "trail", "train", "tulip", "valve", "velvet", "video", "villa", "vine", "waltz", "wheat", "wheel", "wolf", "world", "yacht", "yoga", "youth", "zesty", "zonal", "badge", "basin", "beard", "bench", "birth", "blade", "blank", "blend", "blink", "brick", "bride", "brook", "broom", "brown", "buddy", "cable", "cage", "canoe", "carve", "chalk", "chili", "choir", "civil", "clerk", "clock", "coach", "crane", "creek", "curry", "dance", "diary", "diner", "dove", "draft", "drift", "drum", "dwarf", "earth", "elbow", "entry", "equal", "essay", "event", "faith", "fence", "fiber", "finch", "fjord", "fleet", "forge", "frame", "fruit"
]

from random import sample

def random_phrase(used):
  for i in range(1000):
    phrase = "-".join(sample(words, k=2))
    if phrase not in used:
      return phrase
  return None