
import threading
from threading import Lock
from subprocess import PIPE, runimport subprocessimport uuidfrom PySide2.QtCore import Signalimport timeimport os
from util import *

class DownloadJobProp:
    def __init__(self, url,options,status):
        self.url = url        self.options = options
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
    STATUS_DOWNLOADING = 5    STATUS_STOPPING = 6        RES_TYPE_YTB = 0
    RES_TYPE_BILI = 1
class DownloadThread(threading.Thread):    DOWNLOADER_APP = 'yt-dlp'
    def __init__(self, mgr,job):
        threading.Thread.__init__(self)
        self.job_id = job.id
        self.options = job.options        self.url = job.url        self.keep_running = True        self.download_manager = mgr        print('init thread ' + job.url)        self.app_path = os.path.dirname(os.path.realpath(__file__))

    def run(self):        print('thread running ' + self.url + " " + self.job_id)        cmd = DownloadThread.DOWNLOADER_APP + " " + self.url + " " + self.options
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize = 1,universal_newlines=True)
        #keep_running = True        time.sleep(8)        self.download_manager.update_job_status(self.job_id,DownloadJobProp.STATUS_DOWNLOADING)        
        while(self.keep_running):
            # returns None while subprocess is running
            retcode = p.poll() 
            line = p.stdout.readline().rstrip()
            if len(line) > 0:
                self.download_manager.parse_cmd_output(self.job_id,line)
            time.sleep(5)
            if retcode is not None:                print('download process retcode:' + str(retcode) + ' ' + self.job_id)                self.download_manager.update_job_status(self.job_id,DownloadJobProp.STATUS_FAILED)
                break        try:            p.kill()        finally:            print('download process finished ' + self.job_id)                    if self.keep_running:           print('Mark complete for ' + self.job_id)           self.download_manager.update_job_status(self.job_id,DownloadJobProp.STATUS_COMPLETED)        else:           self.download_manager.update_job_status(self.job_id,DownloadJobProp.STATUS_FAILED)    def stop(self):        print('Stop ' + self.job_id)        self.download_manager.update_job_status(self.job_id,DownloadJobProp.STATUS_STOPPING)        self.keep_running = False    #download_status = Signal(str,int)
class DownloadMgr:
    MSG_TYPE_UPDATE_JOB = 1    MSG_TYPE_ADD_JOB = 2
    #keep_running = True
    def __init__(self, msg_queue):
        self.msg_queue = msg_queue
        #self.urls = urls
        self.job_queue = []        self.job_queue_lock = Lock()        self.thread_queue = []        self.thread_poll_lock = Lock()
        
    def start_downloading(self,job):        self.clear_download_task()
        
        job.options = job.options + ' --paths ' + get_download_dir()        for task in self.thread_queue:
            if task.job_id == job.id:
                if task.is_alive():                    print('already running')                    return        print('Create download thread')        download_thread = DownloadThread(self,job)        self.thread_poll_lock.acquire()
        try:
            self.thread_queue.append(download_thread)
        finally:
            self.thread_poll_lock.release()                download_thread.start()    def stop_downloading(self,job):        print('stop_downloading ' + job.id)        for task in self.thread_queue:            print(task.job_id)
            if task.job_id == job.id:                task.stop()
    def stop_all_download(self):        for task in self.thread_queue:
            task.stop()        for task in self.thread_queue:
            task.join(10)                def clear_download_task(self):        for task in self.thread_queue:            if task.is_alive():                continue            self.thread_poll_lock.acquire()
            try:
                self.thread_queue.remove(task)
            finally:
                self.thread_poll_lock.release()            break    def update_job_status(self,job_id,status):        for cur_job in self.job_queue:
            if not cur_job.id == job_id:                continue
            self.job_queue_lock.acquire()
            try:
                cur_job.status = status
            finally:
                self.job_queue_lock.release()

            self.update_job_2_UI(cur_job)            break
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
            if not cur_job.id == job.id:                continue
            cur_job.status = DownloadJobProp.STATUS_REMOVED            self.update_job_2_UI(cur_job)            self.job_queue_lock.acquire()            try:
                self.job_queue.remove(cur_job)
            finally:
                self.job_queue_lock.release()            self.stop_downloading(cur_job)            break
        
    def resume_job(self,job):
        for cur_job in self.job_queue:
            if cur_job.id == job.id:
                #job.status = DownloadJobProp.STATUS_DOWNLOADING                #self.update_job_2_UI(job)
                self.start_downloading(cur_job)
        
        
    
    def parse_cmd_output(self, job_id,line):
        print(line)
        
        #update job list        for cur_job in self.job_queue:
            if cur_job.id == job_id:
                cur_job.progress = line                #update UI                self.update_job_2_UI(cur_job)
                
                
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
        