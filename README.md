# tucfetch
## Dependencies
- curl
- wget
- neofetch
- chafa (or any other backend supported by neofetch)

## Install
Just install dependencies and run the `install.sh` script
```sh
cd tucfetch/
./install.sh
```

## Uninstall
Run the `uninstall.sh` script, or manually:
```sh
rm ~/.local/bin/tucfetch 2>/dev/null
sudo rm /usr/bin/tucfetch 2>/dev/null
rm -rf ~/.cache/tucfetch
```
