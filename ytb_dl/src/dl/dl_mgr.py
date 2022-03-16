
import threading
from threading import Lock
from subprocess import PIPE, run
from util import *

class DownloadJobProp:
    def __init__(self, url,options,status):
        self.url = url
        self.status = status
        self.progress = ''
        self.id = str(uuid.uuid4())
        #print('gen job id:' + self.id)
        self.TYPE = 0
        
    STATUS_PENDING = 0
    STATUS_PAUSED = 1
    STATUS_COMPLETED = 2
    STATUS_FAILED = 3
    STATUS_REMOVED = 4
    STATUS_DOWNLOADING = 5
    RES_TYPE_BILI = 1

    def __init__(self, mgr,job):
        threading.Thread.__init__(self)
        self.job_id = job.id
        self.options = job.options

    def run(self):
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize = 1,universal_newlines=True)
        #keep_running = True
        while(self.keep_running):
            # returns None while subprocess is running
            retcode = p.poll() 
            line = p.stdout.readline().rstrip()
            if len(line) > 0:
                self.download_manager.parse_cmd_output(self.job_id,line)
            time.sleep(5)
            if retcode is not None:
                break
class DownloadMgr:
    MSG_TYPE_UPDATE_JOB = 1
    #keep_running = True
    def __init__(self, msg_queue):
        self.msg_queue = msg_queue
        #self.urls = urls
        self.job_queue = []
    
    def start_downloading(self,job):
        
        job.options = job.options + ' --paths ' + get_download_dir()
            if task.job_id == job.id:
                if task.is_alive():
        try:
            self.thread_queue.append(download_thread)
        finally:
            self.thread_poll_lock.release()
            if task.job_id == job.id:

            task.stop()
            task.join(10)
            try:
                self.thread_queue.remove(task)
            finally:
                self.thread_poll_lock.release()
            if not cur_job.id == job_id:
            self.job_queue_lock.acquire()
            try:
                cur_job.status = status
            finally:
                self.job_queue_lock.release()

            self.update_job_2_UI(cur_job)
    def add_job(self,url):
        job = DownloadJobProp(url,'',DownloadJobProp.STATUS_PENDING)
        self.job_queue_lock.acquire()
        try:
            self.job_queue.append(job)
            self.add_job_2_UI(job)
        finally:
            self.job_queue_lock.release()
 
        self.start_downloading(job)
    def del_job(self,job):
        for cur_job in self.job_queue:
            if not cur_job.id == job.id:
            cur_job.status = DownloadJobProp.STATUS_REMOVED
                self.job_queue.remove(cur_job)
            finally:
                self.job_queue_lock.release()
        
    def resume_job(self,job):
        for cur_job in self.job_queue:
            if cur_job.id == job.id:
                #job.status = DownloadJobProp.STATUS_DOWNLOADING
                self.start_downloading(cur_job)
        
        
    
    def parse_cmd_output(self, job_id,line):
        print(line)
        
        #update job list
            if cur_job.id == job_id:
                cur_job.progress = line
                
                
    def post_message(self,msg):
        print(msg)
    
    def update_job_2_UI(self,job):
        if self.msg_queue == None:
            print('queue empty')
            return
        m = [DownloadMgr.MSG_TYPE_UPDATE_JOB,job]    
        #print('update_job_2_UI')
        self.msg_queue.put(m)

  
    def add_job_2_UI(self,job):
        if self.msg_queue == None:
            print('queue empty')
            return
        m = [DownloadMgr.MSG_TYPE_ADD_JOB,job]    
        #print('add_job_2_UI')
        self.msg_queue.put(m)
        