python3 convert_to_yolo_format.py -j /home/ohwada/KeyPointsDetectionData/JSON/20231115-13.json -o /home/ohwada/KeyPointsDetectionData/labels/20231115

python3 create_dataset.py -i /home/ohwada/KeyPointsDetectionData/images/20231115/ -l /home/ohwada/KeyPointsDetectionData/labels/20231115/ -o /home/ohwada/KeyPointsDetectionData/20231115 -t 1.0

python3 create_dataset.py -i /home/ohwada/KeyPointsDetectionData/images/20231115/ -l /home/ohwada/KeyPointsDetectionData/labels/20231115/ -o /home/ohwada/KeyPointsDetectionData/dataset_all -t 1.0

scp ohwada@172.16.200.1:/home/ohwada/golf_analysis/coco-annotator/datasets/20231115/*.jpg .