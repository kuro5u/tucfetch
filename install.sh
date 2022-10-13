#!/usr/bin/env bash

# Check for dependencies
dependencies=(curl wget neofetch chafa)

echo "Checking for dependencies.."
for i in ${dependencies[@]}; do 
	if [ ! -f /usr/bin/$i ] && [ ! -f /usr/local/bin/$i ]; then
		echo "Missing dependecy: $i"
		exit
	fi
done

# Create tucfetch directory
XDG_CACHE_HOME=$HOME/.cache
DIR=$XDG_CACHE_HOME/tucfetch

echo "Creating tucfetch directory at $DIR"

mkdir -p "$DIR"
if [ ! -d "$DIR" ]; then
	echo "Failed to create directory"
	exit
fi

# Download tuc avatars
ids=(4109 4110 4111 6752 15787)

echo "Downloading avatars.."
for i in ${ids[@]}; do
	avatars=$(curl -s "https://www.ece.tuc.gr/index.php?id=$i" | tr '"' '\n' | grep csm)
	wget -q $avatars -P "$DIR" -nc
done

# Install tucfetch
echo "Installing tucfetch.."

chmod 0755 "./tucfetch"

if [ -d "$HOME/.local/bin" ]; then
	cp "./tucfetch" "$HOME/.local/bin"

	if [ ! -f "$HOME/.local/bin/tucfetch" ]; then
		echo "Installation failed."
		exit
	else
		echo "Installed at $HOME/.local/bin/tucfetch"
	fi

else
	echo "Installation failed."
	echo "Trying as root.."

	sudo cp "./tucfetch" "/usr/bin"

	if [ ! -f "/usr/bin/tucfetch" ]; then
		echo "Installation failed."
		exit
	else
		echo "Installed at /usr/bin/tucfetch"
	fi
fi

echo "Finished installation!"
