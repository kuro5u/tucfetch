#!/usr/bin/env bash

if [ -f "$HOME/.local/bin/tucfetch" ]; then
	rm "$HOME/.local/bin/tucfetch"
fi

if [ -f "/usr/bin/tucfetch" ]; then
	sudo rm "/usr/bin/tucfetch"
fi

if [ -d "$HOME/.cache/tucfetch" ]; then
	rm -rf "$HOME/.cache/tucfetch" 
fi

echo "Finished uninstalling tucfetch.. :/"
