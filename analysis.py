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

         if session.exists("T01"):
             T01 = session.get("T01")
             self.PDT = T01.PDT if T01.Completed else float('nan')
             self.PTT = T01.PTT if T01.Completed else float('nan')
             self.PTL = T01.PTL if T01.Completed else float('nan')
         else:
             self.PDT = float('nan')
             self.PTT = float('nan')
             self.PTL = float('nan')

         if session.exists("T02"):
             T02 = session.get("T02")
             self.R01 = T02.Pulses[0] if T02.Completed else float('nan')
             self.R02 = T02.Pulses[1] if T02.Completed else float('nan')
             self.R03 = T02.Pulses[2] if T02.Completed else float('nan')
             self.R04 = T02.Pulses[3] if T02.Completed else float('nan')
             self.R05 = T02.Pulses[4] if T02.Completed else float('nan')
             self.R06 = T02.Pulses[5] if T02.Completed else float('nan')
             self.R07 = T02.Pulses[6] if T02.Completed else float('nan')
             self.R08 = T02.Pulses[7] if T02.Completed else float('nan')
             self.R09 = T02.Pulses[8] if T02.Completed else float('nan')
             self.R10 = T02.Pulses[9] if T02.Completed else float('nan')
         else:
             self.R01 = float('nan')
             self.R02 = float('nan')
             self.R03 = float('nan')
             self.R04 = float('nan')
             self.R05 = float('nan')
             self.R06 = float('nan')
             self.R07 = float('nan')
             self.R08 = float('nan')
             self.R09 = float('nan')
             self.R10 = float('nan')

         if session.exists("T03"):
             T03 = session.get("T03")
             self.cPDT = T03.PDT if T03.Completed else float('nan')
             self.cPTT = T03.PTT if T03.Completed else float('nan')
             self.cPTL = T03.PTL if T03.Completed else float('nan')
         else:
             self.cPDT = float('nan')
             self.cPTT = float('nan')
             self.cPTL = float('nan')

         if session.exists("T04"):
             T04 = session.get("T04")
             self.cpmPDT = T04.PDT if T04.Completed else float('nan')
             self.cpmPTT = T04.PTT if T04.Completed else float('nan')
             self.cpmPTL = T04.PTL if T04.Completed else float('nan')
         else:
             self.cpmPDT = float('nan')
             self.cpmPTT = float('nan')
             self.cpmPTL = float('nan')


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

statistics = pd.DataFrame({
    "SubjectID": [d.SubjectID for d in data ],
    "SessionID": [d.SessionID for d in data ],
    "PDT": [d.PDT for d in data ],
    "PTT": [d.PTT for d in data ],
    "PTL": [d.PTL for d in data ],
    "cPDT": [d.cPDT for d in data ],
    "cPTT": [d.cPTT for d in data ],
    "cPTL": [d.cPTL for d in data ],
    "cpmPDT": [d.cpmPDT for d in data ],
    "cpmPTT": [d.cpmPTT for d in data ],
    "cpmPTL": [d.cpmPTL for d in data ],
    "R01": [d.R01 for d in data ],
    "R02": [d.R02 for d in data ],
    "R03": [d.R03 for d in data ],
    "R04": [d.R04 for d in data ],
    "R05": [d.R05 for d in data ],
    "R06": [d.R06 for d in data ],
    "R07": [d.R07 for d in data ],
    "R08": [d.R08 for d in data ],
    "R09": [d.R09 for d in data ],
    "R10": [d.R10 for d in data ],
})    

statistics.to_csv("statistics.csv", index=False, sep=";", decimal=".")
