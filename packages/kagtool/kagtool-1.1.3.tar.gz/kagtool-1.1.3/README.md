```python
from kagtool.kaggle_downloader import KaggleDownloader
from kagtool.model_loader import ModelLoaderSaver

dataset_name = 'us-patent-phrase-to-phrase-matching'
creds = '{"username":"slashafk","key":"..."}'
model_nm = 'microsoft/deberta-v3-small'
num_labels = 1

downloader = KaggleDownloader(dataset_name, creds)
dataset_path = downloader.download()
model_loader = ModelLoaderSaver(model_nm, num_labels)

if DOWNLOAD_DEPS:
    model_loader.download_model()
model_loader.load_model()
```
