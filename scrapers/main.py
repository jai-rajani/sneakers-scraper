import subprocess

process1 = subprocess.Popen(["python", "hypefly.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "superkicks.py"])
#process3 = subprocess.Popen(["python", "pop2.py"])

process1.wait() # Wait for process1 to finish (basically wait for script to finish)
process2.wait()
#process3.wait()