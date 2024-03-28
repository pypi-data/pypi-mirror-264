import logging
import time
from typing import List

from oslo_config import cfg

from aprsd.threads import APRSDThread
from aprsd.utils import objectstore


CONF = cfg.CONF
LOG = logging.getLogger("APRSD")


class APRSDStoreThread(APRSDThread):
    """save object store instances to disk periodically."""

    save_interval = 10

    def __init__(self, obj_list: List[objectstore.ObjectStoreMixin]):
        super().__init__("STORE")
        self.obj_list = obj_list

    def loop(self):
        if self.loop_interval % self.save_interval == 0:
            for obj in self.obj_list:
                LOG.debug(f"Saving {obj.__class__.__name__}")
                obj.save()
        time.sleep(1)
        return True