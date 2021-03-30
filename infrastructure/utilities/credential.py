from decouple import config

class ftpinfo:

    def ftp_Push(self):
        result = {}
        result['host'] = config('ftphost')
        result['username'] = config('ftpusername')
        result['password'] = config('ftppassword')
        result['ftp_path'] = config('ftppath')
        result['ftp_push'] = config('dockerftpfiles')
        result['ftp_pushed'] = config('dockerfilespushed')
        return result

    def ftp_Pull(self):
        result = {}
        result['host'] = config('ftphost')
        result['username'] = config('ftpusername')
        result['password'] = config('ftppassword')
        result['ftp_path'] = config('ftppath')
        result['pulled'] = config('dockerftpfiles')
        result['ftp_move'] = config('ftppathafterpulled')
        return result

    def ftp_logs(self):
        return config('logfilespath')

    def sftp_Push(self):
        result = {}
        result['host'] = config('ftphost')
        result['username'] = config('ftpusername')
        result['password'] = config('ftppassword')
        result['privatekey'] = config('sftpprivatekey')
        result['sftp_path'] = config('ftppath')
        result['sftp_push'] = config('dockerftpfiles')
        result['sftp_pushed'] = config('dockerfilespushed')
        return result

    def sftp_Pull(self):
        result = {}
        result['host'] = config('ftphost')
        result['username'] = config('ftpusername')
        result['password'] = config('ftppassword')
        result['privatekey'] = config('sftpprivatekey')
        result['sftp_path'] = config('ftppath')
        result['sftp_pulled'] = config('dockerftpfiles')
        result['sftp_move'] = config('ftppathafterpulled')
        return result
