import xml.etree.ElementTree as ET

class Result:
   def __init__(self, data):
      self.id = data.attrib["ID"]
      self.name = data.attrib["name"]

   def display(self):
      print(f"Result [ ID:{self.id} ] {self.name} [ Type: {type(self).__name__}]")

class NullResult(Result):
   def __init__(self, data):
      super().__init__(data)

class AlgometryResult(Result):
   def __init__(self, data):
      super().__init__(data)
      valueNodes = data.findall(".//p")
      
      values = [(float(p.attrib['s']), float(p.attrib['c']), float(p.attrib['vas'])) for p in valueNodes]
      self.Pressure = [v[0] for v in values]
      self.ConditioningPressure = [v[1] for v in values]
      self.Rating = [v[2] for v in values]
      self.Time = [float(n)/20 for n in range(0, len(self.Pressure))]
      
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

   def display(self):
      super().display()
      print("  Number of samples:", len(self.Pressure))
      print("  PDT:", self.PDT)
      print("  PTT:", self.PTT)
      print("  PTL:", self.PTL)


class StimulusResponseResult(AlgometryResult):
   def __init__(self, data):
      super().__init__(data)

class TemporalSummationResult(AlgometryResult):
   def __init__(self, data):
      super().__init__(data)

class ConditionedPainModulationResult(AlgometryResult):
   def __init__(self, data):
      super().__init__(data)

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
      print("Subject ID:", self.id)

      for session in self.sessions:
         session.display()
         print("")

def load(filename):
   data = ET.parse(filename)

   return Subject(data)


def main():
   data = load(r"C:\Users\KristianHennings\Desktop\TASKS\Karolinska\Pain Data Final\subjects\059_1.subx")
   data.display()

if __name__=="__main__":
    main()