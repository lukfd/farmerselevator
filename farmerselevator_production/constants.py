from farmerselevator_production import application

# PATHS
databasePath = './farmerselevator_production/database/base.db'

# TOKEN
application.secret_key = b'b[\x0e\x8c\x87\xdb\xa17\x9a\x8d\xdeO\r\xba|\xcd'

# UPLOADS
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER