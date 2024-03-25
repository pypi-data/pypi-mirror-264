import os
from pathlib import Path

class KaggleDownloader:
    def __init__(self, dataset, creds, is_kaggle_env=os.environ.get('KAGGLE_KERNEL_RUN_TYPE', '')):
        self.dataset = dataset
        self.creds = creds
        self.iskaggle_env = is_kaggle_env

    def load_kaggle_creds(self):
        cred_path = Path('~/.kaggle/kaggle.json').expanduser()
        if not cred_path.exists():
            cred_path.parent.mkdir(exist_ok=True)
            cred_path.write_text(self.creds)
            cred_path.chmod(0o600)

    def load_or_fetch_kaggle_dataset(self):
        if self.iskaggle_env:
            path = '/kaggle/input/' + str(self.dataset)
        else:
            path = self.dataset
            self.load_kaggle_creds()
            import zipfile,kaggle
            kaggle.api.competition_download_cli(path)
            zipfile.ZipFile(f'{path}.zip').extractall(path)
        return Path(path)
