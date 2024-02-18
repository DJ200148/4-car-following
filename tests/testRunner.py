import sys
import os
current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(parent_directory)

# from tests.detectionModelUnitTests import detection_unit_tests
from test_yolop import test_yolop_model

# detection_unit_tests()
test_yolop_model('images/test.jpg')