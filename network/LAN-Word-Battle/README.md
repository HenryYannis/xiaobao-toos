# LAN-Word-Battle

局域网内与好友进行英语单词记忆和对战的多人联机小游戏，兼顾趣味与学习。

## 打包命令

```bash
pyinstaller --onefile --icon="vs.ico" --version-file="版本信息.txt" --windowed --add-data "words.txt;." 单词对战.py
```
