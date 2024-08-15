# tucfetch

## Installation
1. Install `neofetch` and `chafa`

2. Run the following script:
```sh
git clone https://github.com/kuro5u/tucfetch
cd tucfetch/
pip install -r requirements.txt
python3 setup.py
cp ./config.conf ~/.config/tucfetch/
chmod +x ./tucfetch.py
cp ./tucfetch.py ~/.local/bin/tucfetch
```

## Uninstall
```sh
rm -rf ~/.config/tucfetch
rm ~/.local/bin/tucfetch
```
