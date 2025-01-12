import tensorflow as tf
import os
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format

config = config_util.get_configs_from_pipeline_file("learner/pipeline.config")

pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()

with tf.io.gfile.GFile(os.path.join("learner","pipeline.config"), "r") as f:
    proto_str = f.read()
    text_format.Merge(proto_str, pipeline_config)

pipeline_config.model.ssd.num_classes = 3 # the number of classes
pipeline_config.train_config.batch_size = 5 # the number of images for each class
pipeline_config.train_config.fine_tune_checkpoint = os.path.join("models","ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8","checkpoint/ckpt-0")
pipeline_config.train_config.fine_tune_checkpoint_type = "detection"
pipeline_config.train_input_reader.label_map_path= os.path.join("annotations","label_map.pbtxt")
pipeline_config.train_input_reader.tf_record_input_reader.input_path[:] = [os.path.join("annotations","train.record")]
pipeline_config.eval_input_reader[0].label_map_path = os.path.join("annotations","label_map.pbtxt")
pipeline_config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [os.path.join("annotations","test.record")]

config_text = text_format.MessageToString(pipeline_config)
with tf.io.gfile.GFile("learner/pipeline.config", "wb") as f:
    f.write(config_text)
