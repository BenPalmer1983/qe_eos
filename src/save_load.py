
################################################################
#
#
#
################################################################

# numpy.ndarray
# numpy.float64


import json
import zlib

class save_load:


  def save(d, file_name):
    d_save = save_load.prep_save(d)
    
    dat = json.dumps(d_save)
    cdat = zlib.compress(dat.encode(), level=9)
    fh = open(file_name, 'wb')
    fh.write(cdat)
    fh.close()


  def load(file_name):
    fh = open(file_name, 'rb')
    cdat = ''.encode()
    for r in fh:
      cdat = cdat + r
    d = json.loads(zlib.decompress(cdat).decode())
    d_load = save_load.prep_load(d)

    return d_load




  def prep_save(d):
    d_save = {}    
    for i in d:
      if(type(d[i]) == numpy.ndarray):
        arr = ['__numpyarray__', d[i].shape, None, None]
        if(len(d[i].shape) == 1):
          d_type = type(d[i][0])
        elif(len(d[i].shape) == 2):
          d_type = type(d[i][0,0])
        elif(len(d[i].shape) == 3):
          d_type = type(d[i][0,0,0])
        if(d_type == numpy.float64):
          arr[2] = 'float64'      
        elif(d_type == numpy.int32):
          arr[2] = 'int32'          
        arr[3] = numpy.ndarray.tolist(d[i])
        d_save[i] = arr
      else:
        d_save[i] = d[i]
    return d_save
    
  def prep_load(d):
    d_load = {}   
    for i in d:
      if(type(d[i]) == list):
        if(d[i][0] == '__numpyarray__'):
          d_load[i] = numpy.asarray(d[i][3], dtype=d[i][2])
      else:
        d_load[i] = d[i]
    return d_load
