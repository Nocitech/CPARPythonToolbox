import DataParser as dp
from pathlib import Path
import time
import pandas as pd

folder = Path(r"C:\Users\KristianHennings\Desktop\TASKS\Karolinska\Pain Data Final\subjects")

subjectFiles = list(folder.glob("*.subx"))   # or "*.txt", "*.json", "*.csv", etc.

class SessionData:
    def __init__(self, id, session):
         self.SubjectID = id
         self.SessionID = session.id


def collectData(filename):
   start = time.perf_counter()
   data = dp.load(filename)
   end = time.perf_counter()   
   print(f"Loaded file: {filename.name} [ {end - start:.2f}s] (Number of sessions: {len(data.Sessions)})")
   return SessionData(data.id, data.Sessions[0]) if data.Sessions else None  

tstart = time.perf_counter()
data = [collectData(f) for f in subjectFiles]
data = [d for d in data if d is not None]
tend = time.perf_counter()

print(f"Total time: {tend - tstart:.2f}s")

statistics = pd.DataFrame([
    "SubjectID", [d.SubjectID for d in data ],
    "SessionID", [d.SessionID for d in data ],
])    

statistics.to_csv("statistics.csv", index=False, sep=";", decimal=".")
