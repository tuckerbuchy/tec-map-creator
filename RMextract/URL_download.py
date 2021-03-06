#!/usr/bin/env python
# AGW - Adapted from Albus_RINEX_download.py

import sys
try:
  import pycurl
  HAS_PYCURL = True
except:
  HAS_PYCURL = False
  try:
    import socket
    import urllib
  except:
    import urllib.request

################################################################################
def urlreporthook(block_count, block_size, file_size):
    """show user how far file download has progressed"""
    if(file_size <= 0):
        return
    percent = float(block_count * block_size) / file_size * 100.0
    sys.stdout.write("\b\b\b\b\b\b%5.1f%%"%percent)
    return

################################################################################
def main():
    if(len(sys.argv) != 4):
        print ("Error: correct usage is %s inURL, outfilename timeout"%sys.argv[0])
        sys.exit(-2)
    if HAS_PYCURL:
      print 'using PyCurl'
      try:
        print("URL=",sys.argv[1]," File=",sys.argv[2])
        try:
          with open(sys.argv[2], 'wb') as f:
               c = pycurl.Curl()
               c.setopt(c.URL, sys.argv[1])
               c.setopt(c.WRITEDATA, f)
               print 'curl getting data at ',sys.argv[1]
               c.perform()
               print 'curl closing for ', sys.argv[1]
               c.close()
        except:
          print 'curl failure - ', sys.argv[1], ' probably not found'
#         sys.exit(-3)
      except:
        pass

    if not HAS_PYCURL:
      print 'using urllib'
      try:
        timeout = float(sys.argv[3])
        socket.setdefaulttimeout(timeout)
        print("URL=",sys.argv[1]," File=",sys.argv[2])
        try:
          urllib.urlretrieve(sys.argv[1], sys.argv[2], urlreporthook)
        except:
          urllib.request.urlretrieve(url=sys.argv[1], filename=sys.argv[2], reporthook=urlreporthook)
        urllib.urlcleanup()
      except:
        sys.exit(-3)
    sys.exit(0)

if __name__ == '__main__':
    main()



