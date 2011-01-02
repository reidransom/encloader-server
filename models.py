import os
import sqlite3
from ftplib import FTP

from settings import DB_FILE, ENCODE_DIR, ENCODING_PRESETS, DESTINATION_PRESETS

class DBConnection(object):

    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.c = self.conn.cursor()

    def close(self):
        self.c.close()
    
class Job(object):
    
    def __init__(self, db, encoding_preset, destination_preset, 
        destination_path, input_filename):
        """Creates a new job."""
        self.db = db
        self.id = None
        self.encoding_preset = encoding_preset
        self.destination_preset = destination_preset
        self.destination_path = destination_path
        self.input_filename = input_filename
        self.status = 'pending'
        self.percent = 0
        
    def save(self):
        """Commits the Job to the database.
        
        If the Job's id is None, a new job is inserted into the database and
        the id is assigned.  Otherwise, the database is simply updated.
        """
        values = (
            self.encoding_preset,
            self.destination_preset,
            self.destination_path,
            self.input_filename,
            self.status,
            self.percent,
        )
        
        if self.id is None:
            self.db.c.execute('insert into job (encoding_preset, ' +
                'destination_preset, destination_path, input_filename, ' +
                'status, percent) values (?,?,?,?,?,?)', values)
            self.id = self.db.c.lastrowid
        
        else:
            self.db.c.execute('update job set encoding_preset=?, ' +
                'destination_preset=?, destination_path=?, input_filename=?, ' +
                'status=?, percent=? where id=?', values + (self.id,))
        
        self.db.conn.commit()

    def update_status(self, status, percent=0):
        """Updates the status and percent and commits to the database."""
        self.status = status
        self.percent = percent
        self.db.c.execute('update job set status=?, percent=? where id=?',
            (self.status, self.percent, self.id))
        self.db.conn.commit()

    def update_percent(self, percent):
        """Updates the percent and commits to the database."""
        self.percent = percent
        self.db.c.execute('update job set percent=? where id=?', (percent, 
            self.id))
        self.db.conn.commit()

    def encode(self):
        """Encodes the Job while updating the status along the way."""
        
        self.update_status('encoding')
        
        # get paths
        input_path = self.get_input_path()
        output_path = self.get_encode_path()

        # run the encode
        cmd = self.get_enc('cmd') % locals()
        os.system(cmd)

        # delete the original file
        os.remove(input_path)

        self.update_percent(100)

    def upload(self):
        """Transfers the resulting file to it's destination while updating the 
        status along the way.
        """
        self.update_status('uploading')

        # upload the file
        encode_path = self.get_encode_path()
        fp = open(encode_path, 'rb')
        ftp = FTP(self.get_dest('host'), self.get_dest('user'), 
            self.get_dest('passwd'))
        ftp.storbinary('STOR %s' % self.destination_path, fp)
        ftp.close()
        fp.close()

        # delete the original file
        os.remove(encode_path)

        self.update_percent(100)

    def get_dest(self, key=None):
        """Returns the destination preset for this Job."""
        preset = DESTINATION_PRESETS[self.destination_preset]
        if key:
            return preset[key]
        return preset
    
    def get_enc(self, key=None):
        """Returns the encoding preset for this Job."""
        preset = ENCODING_PRESETS[self.encoding_preset]
        if key:
            return preset[key]
        return preset
    
    def get_encode_path(self):
        """Returns the path of the encoded file for this job."""
        return os.path.join(ENCODE_DIR,
            'encode_' + os.path.splitext(self.input_filename)[0] + 
            self.get_enc('extension'))

    def get_input_path(self):
        """Returns the path of the input file for this job."""
        return os.path.join(ENCODE_DIR, self.input_filename)
    
    @classmethod
    def encload(cls, id):
        """Encodes and uploads a job."""
        db = DBConnection()
        job = cls.get(db, id)
        job.encode()
        job.upload()
        job.update_status('complete')
        db.close()
    
    @classmethod
    def get_status(cls, db, id):
        """Returns a tuple (string status, real percent)."""
        db.c.execute('select status, percent from job where id=?', (id, ))
        row = db.c.fetchone()
        return (row[0], row[1])
    
    @classmethod
    def get(cls, db, id):
        """Returns an instance of Job."""
        db.c.execute('select encoding_preset, destination_preset, ' +
            'destination_path, input_filename, status, percent from job ' +
            'where id=?', (id, ))
        row = db.c.fetchone()
        j = cls(db, row[0], row[1], row[2], row[3])
        j.id = id
        j.status = row[4]
        j.percent = row[5]
        return j
    
    @classmethod
    def create_table(cls):
        db = DBConnection()
        db.c.execute('''create table job (
            id integer primary key asc,
            encoding_preset text,
            destination_preset text,
            destination_path text,
            input_filename text,
            status text,
            percent real
        )''')
        db.conn.commit()
        db.close()

def create_tables():
    Job.create_table()
