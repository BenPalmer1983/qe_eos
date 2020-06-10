
class save_results:


  @staticmethod
  def run(): 
    file = g.dirs['results'] + "/" + "results.txt" 
    fh = open(file, 'w')
    fh.write("################################################################\n")
    fh.write("#                        RESULTS                               #\n")
    fh.write("################################################################\n")
    fh.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    fh.write("\n")
    fh.write("\n")
    fh.close()
    
    save_results.settings(file)
    if(g.eos['complete']):
      save_results.eos(file)
    if(g.ec['complete']):
      save_results.ec(file)
    
    
  def settings(file): 
    ############################################
    # SAVE TO RESULTS
    ############################################
      
    fh = open(file, 'a')
    fh.write("INPUT SETTINGS\n")
    fh.write("################################\n")
    fh.write("\n")
    fh.write("Structure:                    " + str(g.inp['config']['structure']) + "\n")
    fh.write("Size:                         " + str(g.inp['config']['size']) + "\n")
    fh.write("Alat:                         " + str(g.inp['config']['alat']) + "\n")
    fh.write("Alat Units:                   " + str(g.inp['config']['alat_units']) + "\n")
    fh.write("Alat/Bohr:                    " + str(g.data['alat_in_bohr']) + "\n")
    fh.write("\n")
    
    fh.write("Ecutwfc:                      " + str(g.inp['settings']['ecutwfc']) +"\n")
    fh.write("Ecutrho:                      " + str(g.inp['settings']['ecutrho']) +"\n")
    fh.write("Degauss:                      " + str(g.inp['settings']['degauss']) +"\n")
    fh.write("Kpoints:                      " + str(g.inp['settings']['kpoints']) +"\n")
    fh.write("Kpoints Type:                 " + str(g.inp['settings']['kpointstype']) +"\n")
    fh.write("EOS Points:                   " + str(g.inp['eos']['points']) +"\n")
    fh.write("EOS Strain:                   " + str(g.inp['eos']['strain']) +"\n")
    fh.write("EC Points:                    " + str(g.inp['ec']['points']) +"\n")
    fh.write("EC Strain:                    " + str(g.inp['ec']['strain']) +"\n")
    fh.write("\n")
    fh.write("\n")
    fh.close()
    
    
  def eos(file): 
  
    fh = open(file, 'a')
    fh.write("EOS" + "\n")
    fh.write("################################\n")
    fh.write("\n") 
    fh.write("V0 (Bohr^3):                  " + str(g.eos_results['V0']) +"\n")
    fh.write("E0:                           " + str(g.eos_results['E0']) +"\n")
    fh.write("B0 (RY/BOHR3):                " + str(g.eos_results['B0']) +"\n")
    fh.write("B0 (GPA):                     " + str(g.eos_results['B0_gpa']) +"\n")
    fh.write("B0P:                          " + str(g.eos_results['B0P']) +"\n")    
    fh.write("\n")
    fh.write("\n")
    fh.close()
    
  
  def ec(file): 
    fh = open(file, 'a')
    fh.write("EC" + "\n")
    fh.write("################################\n")
    fh.write("\n")
    for i in range(6):
      if(i == 0):        
        fh.write("Stiffness (RY/BOHR3):         " + 
        std.float_padded(g.ec_results['stiffness'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,5], 10) + "\n" )
      else:
        fh.write("                              " + 
        std.float_padded(g.ec_results['stiffness'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['stiffness'][i,5], 10) + "\n" )    
    fh.write("\n")
    for i in range(6):
      if(i == 0):        
        fh.write("Stiffness (GPA):              " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,5], 10) + "\n" )
      else:
        fh.write("                              " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['stiffness_gpa'][i,5], 10) + "\n" )    
    fh.write("\n")
    for i in range(6):
      if(i == 0):        
        fh.write("Compliance (1/GPA):           " + 
        std.float_padded(g.ec_results['compliance'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,5], 10) + "\n" )
      else:
        fh.write("                              " + 
        std.float_padded(g.ec_results['compliance'][i,0], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,1], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,2], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,3], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,4], 10) + " " + 
        std.float_padded(g.ec_results['compliance'][i,5], 10) + "\n" )    
    fh.write("\n")
    
    
    fh.write("Bulk Modulus B (GPA):         " + str(g.material_properties['B']) + "\n")
    fh.write("BR (GPA):                     " + str(g.material_properties['BR']) + "\n")
    fh.write("BV (GPA):                     " + str(g.material_properties['BV']) + "\n")
    fh.write("\n")
    
    fh.write("Shear Modulus G (GPA):        " + str(g.material_properties['G']) + "\n")
    fh.write("GR:                           " + str(g.material_properties['GR']) + "\n")
    fh.write("GV:                           " + str(g.material_properties['GV']) + "\n")
    fh.write("\n")
    
    fh.write("Young's Modulus E (GPA):      " + str(g.material_properties['E']) + "\n")
    fh.write("\n")
    fh.write("Poisson's Ratio v:            " + str(g.material_properties['v']) + "\n")
    fh.write("\n")
    fh.write("\n")    
    
    fh.write("L Elastic Wave V:             " + str(g.material_properties['vl']) + "\n")
    fh.write("T Elastic Wave V:             " + str(g.material_properties['vt']) + "\n")
    fh.write("M Elastic Wave V:             " + str(g.material_properties['vm']) + "\n")
    fh.write("\n")
    fh.write("Debye Temperature:            " + str(g.material_properties['debye']) + "\n")
    fh.write("\n")
    fh.write("Melting Point:                " + str(round(g.material_properties['melting_point'],0)) + "K \n")
    fh.write("\n")
    fh.write("\n")
    fh.write("\n")
    fh.write("\n")    
    fh.close()