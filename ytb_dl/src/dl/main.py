from ui_mainwindow import Ui_MainWindow
from ui_setting import Ui_SettingUI

import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QMessageBox,QTableWidget,QHeaderView,QTableWidgetItem
from PySide2.QtWidgets import QMenu,QPushButton,QAbstractItemView,QAction
from PySide2.QtCore import QFile,QTimer
from PySide2 import QtCore
from ui_mainwindow import Ui_MainWindow
import optparse
from PySide2.QtGui import *
from PySide2.QtWidgets import QFileDialog
from queue import Queue
from PySide2 import QtWidgets,QtGui
from PySide2.QtCore import Qt
from PySide2.QtCore import Slot
from util import *from dl_mgr import *


class Dl_Test():
    def __init__(self,mainwin):
        self.main_win = mainwin
        
    def start_test(self):
        print('test===')
        QTimer.singleShot(800, self.add_job_test)
        
        time.sleep(10)
        
        QTimer.singleShot(800, self.stop_job_test)
   
        time.sleep(10)
        
        QTimer.singleShot(800, self.remove_job_test)


    def add_job_test(self):
        print('add_job_test')
        url = ''
        self.main_win.main_ui.lineEditURL.setText(url)
        self.main_win.btn_addjob_clicked()
        
    def stop_job_test(self):
        print('stop_job_test')
        job = self.main_win.get_job_from_ui(0)
        self.main_win.downloadMgr.stop_downloading(job)
    
    def restart_job_test(self):
        print('restart_job_test')
        job = self.main_win.get_job_from_ui(0)
        self.main_win.downloadMgr.start_downloading(job)
    
    def remove_job_test(self):
        print('remove_job_test')
        job = self.main_win.get_job_from_ui(0)
        self.main_win.downloadMgr.del_job(job)
    


class MainWindow(QMainWindow):
    ID_IDX = 0
    TYPE_IDX = 1
    URL_IDX = 2
    STATUS_IDX = 3
    PROGRESS_IDX = 4

    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        
        self.main_ui.btnAddJob.clicked.connect(self.btn_addjob_clicked)
        self.main_ui.btnAddJob.setIcon(QIcon('icon/add.png'))
        self.main_ui.btnAddJob.setIconSize(QtCore.QSize(32,32))
        
        self.main_ui.btnSetting.clicked.connect(self.btn_settings_clicked)
        self.main_ui.btnSetting.setIcon(QIcon('icon/settings.png'))
        self.main_ui.btnSetting.setIconSize(QtCore.QSize(32,32))
        
        self.init_download_list_ui()       
        
        self.init_settings_ui()
             
        self.msg_queue = Queue()        self.downloadMgr = DownloadMgr(self.msg_queue)        
        #self.downloadMgr.run_process('ab_id','yt-dlp.exe https://www.youtube.com/watch?v=SmOzZLhOps8')
        
        self.start_msg_timer()
        
        self.download_dir = get_download_dir()
        if self.download_dir == None:
            self.btn_settings_clicked()
        
        #self.test = Dl_Test(self)
        #self.test.start_test()
 
    def init_download_list_ui(self):
              
        #self.main_ui.downloadJobList.setFrameShape(QFrame.NoFrame)  ##设置无表格的外框
        #self.main_ui.downloadJobList.horizontalHeader().setFixedHeight(50) ##设置表头高度
        #self.main_ui.downloadJobList.horizontalHeader().setSectionResizeMode(4,QHeaderView.Stretch)#设置第五列宽度自动调整，充满屏幕
        self.main_ui.downloadJobList.horizontalHeader().setStretchLastSection(True) ##设置最后一列拉伸至最大
        
        self.main_ui.downloadJobList.setColumnCount(5)##设置表格一共有五列
        self.main_ui.downloadJobList.setHorizontalHeaderLabels(['ID','TYPE','URL','STATUS','PROGRESS'])#设置表头文字
        self.main_ui.downloadJobList.horizontalHeader().resizeSection(2,500) #设置第一列的宽度为200
        self.main_ui.downloadJobList.horizontalHeader().setSectionsClickable(False) #可以禁止点击表头的列
        #self.main_ui.downloadJobList.sortItems(1,Qt.DescendingOrder) #设置按照第二列自动降序排序
        #self.main_ui.downloadJobList.horizontalHeader().setStyleSheet('QHeaderView::section{background:green}')#设置表头的背景色为绿色
        self.main_ui.downloadJobList.setColumnHidden(0,True)        self.main_ui.downloadJobList.setColumnHidden(1,True)
        self.main_ui.downloadJobList.setEditTriggers(QAbstractItemView.NoEditTriggers) #设置表格不可更改
        #self.main_ui.downloadJobList.setSortingEnabled(True)#设置表头可以自动排序
        
        #self.main_ui.downloadJobList.setItemDelegateForColumn(4, ProgressDelegate(self))
        #self.main_ui.downloadJobList.setItemDelegateForColumn(1, ButtonDelegate(self))        #self.main_ui.downloadJobList.insertRow(0)        #self.main_ui.downloadJobList.insertRow(0)        #self.btn_del = QtWidgets.QPushButton('Del')
        #self.btn_del.clicked.connect(self.onDelJobClicked)
        #self.main_ui.downloadJobList.setCellWidget(1,3,self.btn_del)        #self.btn_change = QtWidgets.QPushButton('Pause')
        #self.btn_change.clicked.connect(self.onChangeJobStatusClicked)
        #self.main_ui.downloadJobList.setCellWidget(1,3,self.btn_change)
 
           

    def onDelJobClicked(self):
        button = self.sender()
        # or button = self.sender()
        index = self.main_ui.downloadJobList.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())     def onChangeJobStatusClicked(self):
        button = self.sender()
        # or button = self.sender()
        index = self.main_ui.downloadJobList.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())        pos = button.mapToGlobal(button.pos())        self._showButtonMenu(None, pos)
    def updateJobStatus(self,job):        #print('updateJobStatus')        #'ID','TYPE','URL','STATUS','PROGRESS'
        for row in range(self.main_ui.downloadJobList.rowCount()):
            elem = self.main_ui.downloadJobList.item(row, 0)
            ID = elem.text() if elem is not None else ""
            if not job.id == ID:
                continue
                            status = self.main_ui.downloadJobList.item(row, self.STATUS_IDX)
            if job.status == DownloadJobProp.STATUS_PENDING:
                self.main_ui.downloadJobList.setItem(row, self.STATUS_IDX, QTableWidgetItem("Pending"))            elif job.status == DownloadJobProp.STATUS_PAUSED:
                self.main_ui.downloadJobList.setItem(row, self.STATUS_IDX, QTableWidgetItem("Paused"))
            elif job.status == DownloadJobProp.STATUS_FAILED:
                self.main_ui.downloadJobList.setItem(row, self.STATUS_IDX, QTableWidgetItem("Failed"))
            elif job.status == DownloadJobProp.STATUS_COMPLETED:
                self.main_ui.downloadJobList.setItem(row, self.STATUS_IDX, QTableWidgetItem("Completed"))
            elif job.status == DownloadJobProp.STATUS_REMOVED:
                self.main_ui.downloadJobList.removeRow(row)
            elif job.status == DownloadJobProp.STATUS_DOWNLOADING:
                self.main_ui.downloadJobList.setItem(row, self.STATUS_IDX, QTableWidgetItem("Downloading"))            elif job.status == DownloadJobProp.STATUS_STOPPING:
                self.main_ui.downloadJobList.setItem(row, self.STATUS_IDX, QTableWidgetItem("Stopping"))
                                     self.main_ui.downloadJobList.setItem(row, self.URL_IDX, QTableWidgetItem(str(job.url)))            self.main_ui.downloadJobList.setItem(row, self.PROGRESS_IDX, QTableWidgetItem(str(job.progress)))

            
    def contextMenuEvent(self, event):
        print('right click')        row = self.get_row_by_pos(event)        if row < 0:            return
        #col = self.main_ui.downloadJobList.columnAt(event.pos().x())        print(row)
        #print(col)
 
        self._showButtonMenu(row,0, event)
        #super(Window, self).contextMenuEvent(event)

    def get_job_from_ui(self,row):
        if self.main_ui.downloadJobList.rowCount() <= row:
            print('No job yet')
            return None
            
        job = DownloadJobProp('','',DownloadJobProp.STATUS_PENDING)
        job.url = self.main_ui.downloadJobList.item(row, self.URL_IDX).text()
        print('get_job_from_ui url ' + job.url)
        status = self.main_ui.downloadJobList.item(row, self.STATUS_IDX).text()
        job.progress = self.main_ui.downloadJobList.item(row, self.PROGRESS_IDX).text()
        job.id = self.main_ui.downloadJobList.item(row, self.ID_IDX).text()
        print('get_job_from_ui ID ' + job.id)
        #job.TYPE = self.main_ui.downloadJobList.item(row, self.TYPE_IDX).text()
                #print('get_job_from_ui:' + status)
        if status == "Pending":
            job.status = DownloadJobProp.STATUS_PENDING
        elif status == "Paused":
            job.status = DownloadJobProp.STATUS_PAUSED
        elif status == "Failed":
            job.status = DownloadJobProp.STATUS_FAILED
        elif status == "Completed":
            job.status = DownloadJobProp.STATUS_COMPLETED
        elif status == "Removed":
            job.status = DownloadJobProp.STATUS_REMOVED
        elif status == "Downloading":
            job.status = DownloadJobProp.STATUS_DOWNLOADING        elif status == "Stopping":
            job.status = DownloadJobProp.STATUS_STOPPING
        return job

    def get_row_by_pos(self,event):        pos = self.main_ui.downloadJobList.viewport().mapFromGlobal(event.globalPos())
        row = self.main_ui.downloadJobList.rowAt(pos.y())        return row
    def on_open_download_folder(self, event):
        os.startfile(self.download_dir)
    def on_start_job(self, event):
        print('on_start_job Action')        
        row = self.get_row_by_pos(event)
        if row < 0:
            return
        
        print(row)        job = self.get_job_from_ui(row)        self.downloadMgr.start_downloading(job.id,job.cmd)


    def on_stop_job(self, event):
        print('on_stop_job Action')        row = self.get_row_by_pos(event)
        if row < 0:
            return
        
        print(row)

        job = self.get_job_from_ui(row)
        self.downloadMgr.stop_downloading(job.id)
        
    def on_resume_job(self, event):
        print('on_resume_job Action')
        row = self.get_row_by_pos(event)
        if row < 0:
            return
        
        print(row)

        job = self.get_job_from_ui(row)
        self.downloadMgr.start_downloading(job.id,job.url)

    def on_remove_job(self, event):
        print('on_remove_job Action')
        row = self.get_row_by_pos(event)
        if row < 0:
            return
        
        print(row)

        job = self.get_job_from_ui(row)
        self.downloadMgr.del_job(job.id)
    def _showButtonMenu(self, row,col, event):
        job = self.get_job_from_ui(row)
        menu = QMenu()
        startJobAction = QAction('Start', self)
        startJobAction.triggered.connect(lambda: self.on_start_job(event))
        
        stopJobAction = QAction('Stop', self)
        stopJobAction.triggered.connect(lambda: self.on_stop_job(event))
        
        removeJobAction = QAction('Remove', self)
        removeJobAction.triggered.connect(lambda: self.on_remove_job(event))
        
        resumeJobAction = QAction('Resume', self)
        resumeJobAction.triggered.connect(lambda: self.on_resume_job(event))
        
        openFolderAction = QAction('Open download folder', self)
        openFolderAction.triggered.connect(lambda: self.on_open_download_folder(event))
        
        if job.status == DownloadJobProp.STATUS_PENDING:
            menu.addAction(startJobAction)
            menu.addAction(stopJobAction)
        elif job.status == DownloadJobProp.STATUS_PAUSED:
            menu.addAction(startJobAction)
            menu.addAction(stopJobAction)
        elif job.status == DownloadJobProp.STATUS_FAILED:
            menu.addAction(startJobAction)
        elif job.status == DownloadJobProp.STATUS_DOWNLOADING:
            menu.addAction(stopJobAction)
        
        menu.addAction(removeJobAction)
        menu.addAction(openFolderAction)
        menu.exec_(event.globalPos())

    def addJob(self,job):        print('add job')        for row in range(self.main_ui.downloadJobList.rowCount()):
            elem = self.main_ui.downloadJobList.item(row, 0)
            ID = elem.text() if elem is not None else ""
            if job.id == ID:                #already exist                print(job.id + ' already exists')                return        self.main_ui.downloadJobList.insertRow(self.main_ui.downloadJobList.rowCount())        row_idx = self.main_ui.downloadJobList.rowCount() - 1        self.main_ui.downloadJobList.setItem(row_idx, 0, QTableWidgetItem(str(job.id)))        #action_button = QtWidgets.QPushButton('...')        #action_button.clicked.connect(self.onChangeJobStatusClicked)
        #self.main_ui.downloadJobList.setCellWidget(row_idx,3,action_button)        self.updateJobStatus(job)        
     
    def update_msg(self):
        #print('update msg')
        if self.msg_queue.empty():
            return
            
        #print('update msg')
        msg = self.msg_queue.get()
        #print(msg)
        #self.main_ui.edit_task_console.moveCursor(QTextCursor::End);        msg_type = msg[0]
        if msg_type == DownloadMgr.MSG_TYPE_UPDATE_JOB:
            job = msg[1]            self.updateJobStatus(job)
        elif msg_type == DownloadMgr.MSG_TYPE_ADD_JOB:            job = msg[1]            self.addJob(job)
    
    def start_msg_timer(self):
        self.msg_timer = QtCore.QTimer()
        self.msg_timer.setInterval(100)
        
        self.msg_timer.timeout.connect(self.update_msg)
        self.msg_timer.start(1000)
        
    
    def btn_addjob_clicked(self):
        url = self.main_ui.lineEditURL.text()        #url = 'https://www.youtube.com/watch?v=SmOzZLhOps8'
        if not is_url_valid(url):            self.main_ui.label_info.setText('Please use a valid url')            return
                self.downloadMgr.add_job(url)



    def init_settings_ui(self):
        self.settings_dlg = QDialog()
        
        self.settings_dlg.setStyleSheet(open('ui.css').read())
        self.settings_ui = Ui_SettingUI()
        self.settings_ui.setupUi(self.settings_dlg)
        
        self.settings_ui.btn_sel_folder.clicked.connect(self.btn_settings_sel_folder_clicked)
        self.settings_ui.btn_sel_folder.setIcon(QIcon('icon/save.png'))
        self.settings_ui.btn_sel_folder.setIconSize(QtCore.QSize(16,16))


    def btn_settings_sel_folder_clicked(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Folder')
        print(fname)
        if not os.path.isdir(fname):
            self.settings_ui.label_info.setText('Please choose a valide download folder')
            return
    
        download_dir = self.settings_ui.lineEditDownloadFolder.text()
        if not os.access(download_dir, os.W_OK):
            self.settings_ui.label_info.setText('The selected folder is not writable')
            return

        self.settings_ui.lineEditDownloadFolder.setText(fname)


    def btn_settings_clicked(self):
        settings = load_global_settings()        print(settings['usr_folder'])
        self.settings_ui.lineEditDownloadFolder.setText(settings['usr_folder'])
        
        if not self.settings_dlg.exec_():
           return        download_dir = self.settings_ui.lineEditDownloadFolder.text()
        if not os.access(download_dir, os.W_OK):            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Please choose a valide download folder')
            msg.setWindowTitle("Error")
            msg.exec_()            exit(0)
        
        self.download_dir = self.settings_ui.lineEditDownloadFolder.text()
        os.chdir(self.download_dir)
        settings['usr_folder'] = self.download_dir        print(settings['usr_folder'])
        save_global_settings(settings)




if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('--profile')
    parser.add_option('--social')
    
    options, args = parser.parse_args()

    profile = options.profile
    social = options.social
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon/download.png.png'))
    
    myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
    #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window = MainWindow()
    window.setWindowIcon(QIcon('icon/download.png.png'))
    window.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint| Qt.WindowMinimizeButtonHint)
    
    window.setStyleSheet(open('ui.css').read())
    
    window.show()

    sys.exit(app.exec_())
