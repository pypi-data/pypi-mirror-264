from pycocotools.coco import COCO
from pathlib import Path
lables_path = Path('test_dataset/test/army_extra_Sayeret_Golani_29122023_Evo_210s_record_29_12_2023_03_57_secondary_segment_6.mp4_annotations_thermal_classifier.json')
labels_obj = COCO(lables_path)
print(labels_obj)