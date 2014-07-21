from datetime import datetime
from time import sleep
from rq.job import Job
from models.trial import Trial
from redis import Redis

__author__ = 'daniel'

import threading

class RqResultsProcessor(threading.Thread):
    session = None
    stopped = False

    def stop(self):
        self.stopped = True

    def run(self):
        redis_conn = Redis()
        # get all
        while True:
            incomplete = self.session.query(Trial).filter(Trial.end_date == None).filter(Trial.start_date!=None).all()
            for t in incomplete:
                try:
                    job = Job.fetch(t.job, connection=redis_conn)
                except:
                    print("Exception occurred. Moving on.")
                    sleep(1)
                    continue

                if job.result is not None:
                    print("Result for " + t.name + " found.")
                    t.result = job.result
                    t.end_date = datetime.now()

                    self.session.add(t)
                    self.session.commit()
                    self.session.expire(t)

            if self.stopped:
                self.session.close()
                return

            sleep(1)
