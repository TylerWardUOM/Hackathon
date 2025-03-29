from modlib.models import COLOR_FORMAT, MODEL_TYPE, Model
from modlib.models.post_processors import pp_od_bscn
from modlib.apps import Annotator #Will get this working in a bit

class SFace_PT(Model):
    def __init__(self):
        super().__init__(
            model_file="./path/to/onnx",
            model_type=MODEL_TYPE.ONNX,
            color_format=COLOR_FORMAT.RGB,
            preserve_aspect_ratio=True,
        )

        # Optionally define self.labels

    def post_process(self, output_tensors: List[np.ndarray]) -> Detections:
        return pp_od_bscn(output_tensors)
