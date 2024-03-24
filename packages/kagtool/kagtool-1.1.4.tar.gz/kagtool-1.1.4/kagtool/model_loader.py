from transformers import AutoModelForSequenceClassification, AutoTokenizer
from pathlib import Path
import os

class ModelLoaderSaver:
    def __init__(self, model_name, num_labels):
        self.model_name = model_name
        self.num_labels = num_labels
        self.model = None
        self.tokenizer = None

    def download_model(self):
        if not os.path.exists(self.model_path()):
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=self.num_labels)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.save_model()
    
    def load_model(self):
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path(), num_labels=self.num_labels)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path())

    def save_model(self):
        self.model_path().mkdir(parents=True, exist_ok=True)
        self.model.save_pretrained(self.model_path())
        self.tokenizer.save_pretrained(self.model_path())

    def model_path(self):
        return Path('/kaggle/working/model') / self.model_name