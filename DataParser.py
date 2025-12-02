import xml.etree.ElementTree as ET
import numpy as np

class Result:
   def __init__(self, data):
      self.id = data.attrib["ID"]
      self.name = data.attrib["name"]
      self.Completed = False

   def display(self):
      print(f"   [ ID:{self.id}, Type: {type(self).__name__}, Completed: {self.Completed} ] {self.name}")

class NullResult(Result):
   def __init__(self, data):
      super().__init__(data)

class AlgometryResult(Result):
   def __init__(self, data):
      super().__init__(data)
      valueNodes = data.findall(".//p")
      
      values = [(float(p.attrib['s']), float(p.attrib['c']), float(p.attrib['vas'])) for p in valueNodes]
      self.Pressure = np.array([v[0] for v in values])
      self.ConditioningPressure = np.array([v[1] for v in values])
      self.Rating = np.array([v[2] for v in values])
      self.Time = np.array([float(n)/20 for n in range(0, len(self.Pressure))])
      self.Completed = True
      
class TemporalSummationResult(AlgometryResult):
   def __init__(self, data):
      super().__init__(data)

      self.StimulatingPressure = float(data.attrib['nominal-stimulating-pressure'])
      self.NumberOfStimuli = int(data.attrib['number-of-stimuli'])
      self.Ton = float(data.attrib['t-on'])
      self.Toff = float(data.attrib['t-off'])
      self.Pulses = np.array([self.get_response(n) for n in range(0, self.NumberOfStimuli)])

   def get_response(self, n):
      period = int(20*(self.Ton + self.Toff))
      index  = n * period
      return self.Rating[index] if index < len(self.Rating) else self.Rating[-1]

class ThresholdResult(AlgometryResult):
   def __init__(self, data):
      super().__init__(data)

      self.VASPDT = float(data.attrib['vas-pdt'])
      self.PDT = self.FindPDT()
      self.PTT = self.Pressure[-1] if len(self.Pressure) > 0 else float('nan')
      self.PTL = self.Rating[-1] if len(self.Rating) > 0 else float('nan')

   def FindPDT(self):
      index = self.FindIndexDownwards(self.VASPDT)
      return float('nan') if index < 0 else self.Pressure[index]

   def FindIndexDownwards(self, score):
      for n in range(len(self.Rating) - 2, -1, -1):
         if self.Rating[n] <= score and self.Rating[n + 1] >= score:
            return n + 1
                  
      return -1

class StimulusResponseResult(ThresholdResult):
   def __init__(self, data):
      super().__init__(data)


class ConditionedPainModulationResult(ThresholdResult):
   def __init__(self, data):
      super().__init__(data)

      self.ConditioningPressure = data.attrib['nominal-cond-pressure']

def CreateResult(node):
   if node.tag == "null-result":
      return NullResult(node)
   elif node.tag == "stimulus-response":
      return StimulusResponseResult(node)
   elif node.tag == "temporal-summation":
      return TemporalSummationResult(node)
   elif node.tag == "conditioned-pain-modulation":
      return ConditionedPainModulationResult(node)
   else:
      raise Exception("Unknown result type: " + node.tag)

class Session:
   def __init__(self, node):
      self.id = node.attrib["id"]
      self.results = [CreateResult(r) for r in node.find("results")]

   def display(self):
      print("Session ID:", self.id)

      print("Results:")

      for result in self.results:
         result.display()

      print("")

class Subject:
   def __init__(self, data):
      root = data.getroot()
      sessions = data.find("sessions")

      self.id = root.attrib["id"]   

      self.sessions = [Session(session) for session in sessions.findall("session")  ]  

   def display(self):
      print(f"Subject [ ID: {self.id} ]")

      for session in self.sessions:
         session.display()
         print("")

def load(filename):
   return Subject(ET.parse(filename))


def main():
   #data = load(r"C:\Users\KristianHennings\Desktop\TASKS\Karolinska\Pain Data Final\subjects\059_1.subx")
   data = load(r"C:\Users\KristianHennings\Desktop\TASKS\Karolinska\Pain Data Final\subjects\091_3.subx")
   data.display()

if __name__=="__main__":
    main()