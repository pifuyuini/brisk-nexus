# 用于通过SSH远程登陆服务器时在终端上显示欢迎词

效果如图所示。

![alt text](welcome_example-1.png)

调用时需在shell的配置文件中`~/.zshrc`中加入类似以下内容（**注意路径**）：
```[zsh]
# === Welcome script on SSH login ===
if [ -n "$SSH_CONNECTION" ]; then
    source /home/macuser/miniconda3/etc/profile.d/conda.sh
    conda activate lab
    python ~/.welcome_screen/welcome_screen.py
fi
```