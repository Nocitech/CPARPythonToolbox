import xml.etree.ElementTree as ET

class NullResult:
   def __init__(self, data):
      self.id = data.attrib["ID"]

class StimulusResponseResult:
   def __init__(self, data):
      self.id = data.attrib["ID"]

class TemporalSummationResult:
   def __init__(self, data):
      self.id = data.attrib["ID"]

class ConditionedPainModulationResult:
   def __init__(self, data):
      self.id = data.attrib["ID"]

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
         print(" - Result ID:", result.id)

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

