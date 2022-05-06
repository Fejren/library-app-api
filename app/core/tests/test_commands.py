from unittest.mock import patch
from django.db import OperationalError
from django.test import TestCase
from django.core.management import call_command

class CommandTests(TestCase):
    
    moduleName = 'django.db.utils.ConnectionHandler.__getitem__'

    def test_wait_for_db_ready(self):
        # Test waiting for db, when db is ready
        with patch(self.moduleName) as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)
    
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        
        with patch(self.moduleName) as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
