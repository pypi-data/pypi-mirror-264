from torch.utils.data import Dataset, ConcatDataset
from pycocotools.coco import COCO
from pathlib import Path
from SoiUtils.datasets.base import ImageDetectionSample,Detection
from PIL import Image
import numpy as np
# import fiftyone as fo
import warnings
from typing import Union, List
import yaml


def collate_fn(batch):
    return tuple(zip(*batch))

#TODO: consider writing a prper fiftyone exporter
def export_dataset(collection_datasets, export_dir_path, dataset_name, copy_images=False, move_images=False, tags=None):
        """
        Exports the dataset as a COCO dataset. A folder will be created at export_dir_path:
        export_dir_path/dataset_name
        |
        |-data
            |-img1.ext
            |-img2.ext
            |-...
        |-annotaions_file_name.json
        data is a folder that contains the images, however if copy_images and move_images are both false then 
        the folder will not be created.

        :param export_dir_path: where to save the dataset
        :param dataset_name: the name to give to the fiftyone dataset instance, and the dataset folder
        :param annotations_file_name: the name to give to the annotations file
        :param copy_images: if set to true, the original images will be copied to the exported dataset.
        :param move_images: if set to true, the original images will be cut and moved to the exported dataset
        """
        if copy_images and move_images:
            warnings.warn("Both copy_images and move_images flags are set to true. Defaulting to Copy.")
            move_images = False

        samples = []
        for i, dataset in enumerate(collection_datasets):
            for sub_d in dataset.collection.datasets:
                for j in range(len(sub_d)):
                    image_file_path = Path(sub_d.get_image_file_path(j))
                    video_name = image_file_path.parents._parts[-3]
                    sample = fo.Sample(filepath=image_file_path)

                    orig_image = cv.imread(image_file_path.__str__())
                    _, annotations = sub_d[j]
                    detections = []
                    if len(annotations) > 0:
                    # Convert detections to FiftyOne format
                        for det in annotations:
                            det = Detection.load_generic_mode(
                                bbox=det['bbox'], cl=det['cls'], from_type=sub_d.get_bbox_type(), to_type="fiftyone", image_size=orig_image.shape[:2][::-1])
                            bbox, cls = det.bbox, det.cls

                            detections.append(
                                fo.Detection(label=sub_d.classes[cls]['name'], bounding_box=bbox, extracted_from=video_name)
                            )

                    # Store detections in a field name of your choice
                    sample["ground_truth"] = fo.Detections(detections=detections)
                    if tags is not None:
                        sample.tags.append(tags[i])
                    samples.append(sample)

        # Create dataset
        dataset = fo.Dataset(dataset_name, overwrite=True)
        dataset.add_samples(samples)
        
        export_mode = False
        if copy_images:
            export_mode = True
        elif move_images:
            export_mode = "move"

        if tags is not None:
            for tag in tags:
                dataset_view = dataset.match_tags(tag)
                dataset_view.export(
                    dataset_type=fo.types.COCODetectionDataset,
                    export_dir=f"{export_dir_path}/{tag}",
                    labels_path="annotations.json",
                    label_field="ground_truth",
                    abs_paths=False,
                    export_media=export_mode
                    )
        else:
            dataset.export(
                dataset_type=fo.types.COCODetectionDataset,
                export_dir=f"{export_dir_path}",
                labels_path="annotations.json",
                label_field="ground_truth",
                abs_paths=False,
                export_media=export_mode
            )    

class ImageDetectionDataset(Dataset):
    def __init__(self,
                 dataset_root_dir: str, 
                 annotation_file_path: str,
                 origin_bbox_format: str = 'coco',
                 target_bbox_format: str = 'coco',
                 selected_classes: Union[str, List[str]] = 'all',
                 transforms = None):
        """
        dataset class for our tagged data in the gcp.

        Args:
            dataset_root_dir (str): path to the data directory.
            annotation_file_path (str): path to the annotation .json file .
            origin_bbox_format (str): 
            target_bbox_format (str):
            selected_classes (Union[str, List[str]]): classes that will apper in your dataset.
        
        Returns:
            nn.Dataset
        """
        super().__init__()

        self.origin_bbox_format = origin_bbox_format
        self.target_bbox_format = target_bbox_format

        self.dataset_root_dir = Path(dataset_root_dir)
        all_dataset_info = COCO(annotation_file_path)
        self.images = all_dataset_info.imgs
        self.frames_dir_name = all_dataset_info.dataset['info']['img_dir']
        self.classes = all_dataset_info.cats
        self.imgToAnns = all_dataset_info.imgToAnns

        self.selected_classes = selected_classes
        self.class_mapper = self.create_class_mapper()
        self.transforms = transforms

    def create_class_mapper(self):
        class_mapper = {}
        for _, class_dict in self.classes.items():
            original_class_id, class_name, supercatergory = class_dict['id'] ,class_dict['name'].lower(), class_dict['supercategory'].lower()
            
            if self.selected_classes == 'all':
                class_mapper[original_class_id] = original_class_id

            elif class_name in self.selected_classes:
                class_mapper[original_class_id] = self.selected_classes.index(class_name) + 1
            
            elif supercatergory in self.selected_classes:
                class_mapper[original_class_id] = self.selected_classes.index(supercatergory) + 1
    
            else:
                continue
        
        return class_mapper

    
    def get_image_file_path(self, index: int):
        image_id = self.images[index]['id']
        return str(self.dataset_root_dir/self.frames_dir_name/self.images[image_id]['file_name'])

    def __getitem__(self, index: int) -> ImageDetectionSample:
        image_file_path = self.get_image_file_path(index)
        image = np.asarray(Image.open(image_file_path).convert('RGB'))
        detections = [Detection.load_generic_mode(bbox=detection_annotation['bbox'], 
                                                  cl=self.class_mapper[detection_annotation['category_id']], 
                                                  from_type=self.origin_bbox_format, 
                                                  to_type=self.target_bbox_format, 
                                                  image_size=image.shape[:2][::-1])
                       
                       for detection_annotation in self.imgToAnns[index]]

        image_detection_sample = ImageDetectionSample(image=image, detections=detections)

        telemetry = self.imgToAnns[index][0]['attributes'] if 'attributes' in self.imgToAnns[index][0] else None
        
        if self.transforms is not None:
            item = self.transforms(image_detection_sample)
        else:
            item = image_detection_sample
        
        return item.image, [det.__dict__ for det in item.detections], telemetry

    def __len__(self):
        return len(self.images)
    

class ImageDetectionDatasetCollection(Dataset):
    def __init__(self, datasets_yaml_path) -> None:
        super().__init__()
        with open(datasets_yaml_path, "r") as stream:
            self.datasets_cfg = yaml.load(stream, Loader=yaml.FullLoader)

        self.selected_classes = self.datasets_cfg['selected_classes']
        self.collection = ConcatDataset([ImageDetectionDataset(selected_classes=self.selected_classes, **dataset_cfg) 
                                         for dataset_cfg in self.datasets_cfg['datasets']])
    
    def __getitem__(self, index:int) -> ImageDetectionDataset:
        return self.collection[index]
    
    def __len__(self):
        return len(self.collection)

    def get_sub_dataset(self, index):
        return self.collection.datasets[index]
    
    def num_subsets(self):
        return len(self.datasets_cfg['datasets'])