import os
os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',GRADIO_ANALYTICS_ENABLED='False')
from pathlib import Path
import numpy as np
REVISION='614241f622f53c4eeff9890bdc4f31cfecc418b3'
MODEL=Path(os.environ.get('ARABIC_POETRY_E5_PATH',str(Path.home()/'.cache/huggingface/hub/models--intfloat--multilingual-e5-small/snapshots'/REVISION)))

class E5:

    def __init__(self, path=MODEL):
        import torch
        from transformers import AutoTokenizer, AutoModel
        self.torch = torch
        torch.set_num_threads(2)
        self.tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
        self.model = AutoModel.from_pretrained(path, local_files_only=True).eval()
        self.path = str(path)

    def encode(self, texts):
        result = []
        for text in texts:
            b = self.tokenizer(text, return_tensors='pt', truncation=False)
            if b['input_ids'].shape[1] > 512:
                raise ValueError('E5 input exceeds512tokens; no truncation')
            with self.torch.inference_mode():
                h = self.model(**b).last_hidden_state
                m = b['attention_mask'].unsqueeze(-1)
                v = (h * m).sum(1) / m.sum(1)
                result.append(self.torch.nn.functional.normalize(v, p=2, dim=1).numpy()[0])
        return np.asarray(result, dtype='float32')
