



## Init

**Install Homebrew**
```bash
# For cn gamers
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```


**Install python3**
```bash
brew install python3
```

**Install setuptools**
```bash
pip3 install --upgrade build
```

**Install twine**
```bash
pip3 install twine
```

## Build

**Build**
```bash
python3 -m build
```

**Deploy**
```
twine upload dist/*
twine upload --overwrite dist/*
```