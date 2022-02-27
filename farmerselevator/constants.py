from farmerselevator import application
import os

# PATHS
databasePath = './farmerselevator/database/sqlite/base.db'

# TOKEN
application.secret_key = b'b[\x0e\x8c\x87\xdb\xa17\x9a\x8d\xdeO\r\xba|\xcd'

# UPLOADS

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'farmerselevator/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER