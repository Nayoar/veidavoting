import glob

files = glob.glob(__file__.replace("__init__.py", "*.py"))
files = [item.split("\\")[-1].replace(".py", "") for item in files]
files.remove("__init__")

for f in files:
  __import__("app.routes." + f)