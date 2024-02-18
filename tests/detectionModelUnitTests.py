from classes.yolo_model import DetectionModel

def detect_test():
    # Initialize
    model = DetectionModel()
    results = model.detect('.\\tests\\download.jpg')
    # print(results)
    new_image = model.draw_detections(results[0])

    model.save_results(new_image, '.\\tests\\results.jpg')

    print(results)
    
def detection_unit_tests():
    detect_test()