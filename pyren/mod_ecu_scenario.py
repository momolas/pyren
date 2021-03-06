#!/usr/bin/env python

import os
import re

import mod_globals
import mod_db_manager
import mod_utils
import mod_ecu

from mod_utils import pyren_encode

def playScenario(command, ecu, elm):
  
  services = ecu.Services
  
  path = "EcuRenault/Scenarios/"
  scenarioName,scenarioData = command.scenario.split('#')

  scenarioData = scenarioData.upper()[:-4]+'.xml'

  showable = False
  if scenarioName.lower().startswith('scm'):
    showable = True
  
  if showable:
    ecuNumberPattern = re.compile(r'\d{5}')
    ecuNumberIndex = ecuNumberPattern.search(scenarioData)
    if ecuNumberIndex:
      scenarioName = scenarioData[:scenarioData.find(ecuNumberIndex.group(0)) - 1].lower()
  
  if os.path.isfile('./'+scenarioName+'.py'):
    scen = __import__( scenarioName )
    if mod_globals.clip_arc:
      scen.run( elm, ecu, command, '../'+path+scenarioData )
    else:
      scen.run( elm, ecu, command, './'+path+scenarioData )
    return
    
  print "\nThere is scenarium. I do not support them!!!\n"
  if showable:
    ch = raw_input('Press ENTER to exit or type [SHOW]: ')
  else:
    ch = raw_input('Press ENTER to exit')

  if 'show' not in ch.lower():
    return
    
  if not mod_db_manager.file_in_clip(os.path.join(path,scenarioData)):
    return
    
  lines = [line.rstrip('\n') for line in mod_db_manager.get_file_from_clip(os.path.join(path,scenarioData))]
  
  for l in lines:
    pa = re.compile(r'name=\"(\w+)\"\s+value=\"(\w+)\"')
    ma = pa.search( l )
    if ma:
      p_name = ma.group(1)
      p_value = ma.group(2)
      
      if p_value.isdigit() and p_value in mod_globals.language_dict.keys():
        p_value = mod_globals.language_dict[p_value]
        
      print pyren_encode( "  %-20s : %s" % (p_name, p_value) )

    else:
      print pyren_encode( l.decode( 'utf-8', 'replace' ))
  
  ch = raw_input('Press ENTER to exit')

  
  return
