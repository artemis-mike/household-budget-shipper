import logging, os, requests, json, time, signal, sys
from datetime import datetime

# VARIABLE   = os.environ.get("VARIABLE", None)
LOGLEVEL  = os.environ.get("SHIPPER_LOGLEVEL", "INFO")
INTERVAL        = int(os.environ.get("SHIPPER_INTERVAL", 30))
FORCE_INTERVAL  = os.environ.get("SHIPPER_FORCE_INTERVAL", False)

logging.basicConfig(format='%(asctime)s %(levelname)s\t%(message)s', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.getLogger().setLevel(LOGLEVEL)

def signal_handler(sig, frame):
  logging.info("Recevied signal " + str((signal.Signals(sig).name)) + ". Shutting down.")
  sys.exit(0)

def check_settings():
  error = False
  # Do some checks like
  #  if (VARIABLE is None):
  #    logging.critical("VARIABLE is not set. This is required. Exiting.")
  #    error = True
  if (INTERVAL < 5 and FORCE_INTERVAL == False):
    logging.info("It's not recommended to set SHIPPER_INTERVAL to a value less than 5. Your value is %s. Default value is 30.", INTERVAL)
    logging.info("Set SHIPPER_FORCE_INTERVAL = True to ignore this warning.")
    error = True
  if error is True:
    return 1
  else:
    return 0
  

def main():
  logging.debug("Running with this configuration:")
  # Do some stuff

  while(True):
    # Main control loop goes in here
    logging.info("Nothing to do. Sleeping for %ss.", INTERVAL)
    time.sleep(INTERVAL)



if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGHUP, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

  main()