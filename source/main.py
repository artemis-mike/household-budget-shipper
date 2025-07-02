import logging, os, requests, json, time, signal, sys
from datetime import datetime
from requests.auth import HTTPBasicAuth

# VARIABLE   = os.environ.get("VARIABLE", None)
NEXTCLOUD_BASE_URL  = os.environ.get("SHIPPER_NEXTCLOUD_BASE_URL").rstrip("/")
FILEPATH_BUDGET_DIRECTORY = os.environ.get("SHIPPER_FILEPATH_BUDGET_DIRECTORY").rstrip("/").lstrip("/")
NEXTCLOUD_USERNAME  = os.environ.get("SHIPPER_NEXTCLOUD_USERNAME")
NEXTCLOUD_PASSWORD  = os.environ.get("SHIPPER_NEXTCLOUD_PASSWORD")
LOGLEVEL            = os.environ.get("SHIPPER_LOGLEVEL", "INFO")
INTERVAL            = int(os.environ.get("SHIPPER_INTERVAL", 30))
FORCE_INTERVAL      = os.environ.get("SHIPPER_FORCE_INTERVAL", False)

logging.basicConfig(format='%(asctime)s %(levelname)s\t%(message)s', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.getLogger().setLevel(LOGLEVEL)

def signal_handler(sig, frame):
  logging.info("Recevied signal " + str((signal.Signals(sig).name)) + ". Shutting down.")
  sys.exit(0)

def check_settings():
  error = False
  # Do some checks like
  requiredVars = ["NEXTCLOUD_BASE_URL", "FILEPATH_BUDGET_DIRECTORY", "NEXTCLOUD_USERNAME", "NEXTCLOUD_PASSWORD", "LOGLEVEL"]
  for var in requiredVars:
    if (globals().get(var) is None):
        logging.critical(f"SHIPPER_{var} is not set. This is required. Exiting.")
        error = True
  if (INTERVAL < 5 and FORCE_INTERVAL == False):
    logging.info("It's not recommended to set SHIPPER_INTERVAL to a value less than 5. Your value is %s. Default value is 30.", INTERVAL)
    logging.info("Set SHIPPER_FORCE_INTERVAL = True to ignore this warning.")
    error = True
  if error is True:
    return 1
  else:
    return 0
  
def getCurrentYear():
  return datetime.date.today().year

def downloadFile(filename, path="workbench/"):
  remoteFullPath = NEXTCLOUD_BASE_URL +"/remote.php/dav/files/"+ NEXTCLOUD_USERNAME +"/"+ FILEPATH_BUDGET_DIRECTORY +"/"+ filename
  response = requests.get(remoteFullPath, auth=HTTPBasicAuth(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD), stream=True)
  if response.status_code == 200:
    with open(path+filename, "wb") as f:
      for chunk in response.iter_content(chunk_size=8192):
        if chunk:
          f.write(chunk)
    logging.info(f"Downloaded file {filename} successfully.")
  else:
    logging.error(f"Download failed with status code: {response.status_code}")
  

def main():
  logging.debug("Running with this configuration:")
  if (check_settings() != 0):
    logging.error("Failed settings check. Exit.")
    return 1
  # Do some stuff

  while(True):
    # Main control loop goes in here
    downloadFile("template.ods")
    logging.info("Nothing to do. Sleeping for %ss.", INTERVAL)
    time.sleep(INTERVAL)



if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGHUP, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

  main()