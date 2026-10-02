# Running — 安装启动全流程

> 零基础照着做就能跑。全程只用系统自带的 Python 3，不需要装任何第三方包，也不需要 Node.js。

## 一、先确认环境

打开「终端」（Terminal），输入下面这行，看有没有版本号：

```bash
python3 --version
```

只要输出类似 `Python 3.9.x` 或更高的 `Python 3.10 / 3.11 / 3.12` 就行。macOS 一般自带。

> 如果提示 `command not found`，先装 Python 3（官网 python.org 下载安装，安装时勾选「Add to PATH」），装完重开终端再试。

## 二、进入项目目录

```bash
cd /Users/Admin/Knowledge/Coding/daodejing-study
```

（如果你把项目放在别处，改成你自己的路径。）

## 三、构建站点

把 `web/content/` 里的 Markdown 内容，编译成 `web/dist/` 静态网页：

```bash
python3 web/build.py
```

看到下面两行就是成功：

```
解析到 81 章
构建完成：web/dist/
```

## 四、启动本地预览

```bash
python3 web/serve.py
```

看到：

```
已在本地启动：http://localhost:5173  （Ctrl+C 停止）
```

然后用浏览器打开 **http://localhost:5173** 就能看到网站了。

## 五、停止

回到终端，按 `Ctrl + C` 就停了。

## 常见问题

| 现象 | 原因与处理 |
|---|---|
| 提示「还没有构建产物」 | 还没跑第三步 `python3 web/build.py`，先构建再启动。 |
| 提示 `Address already in use` | 端口 5173 被占用：先 `Ctrl+C` 停掉旧服务，或换端口（改 `web/serve.py` 里的 `PORT`）。 |
| 改了内容/样式看不到变化 | 内容或模板改完要重新跑一次 `python3 web/build.py`；纯样式 `assets/` 会随构建自动重拷，同样需重新构建。 |
