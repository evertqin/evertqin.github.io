
---
title: Atom and Emacs, how to support Chinese
date: 07/13/2015
tags: 
- Technology
- Editor
- Atom
- Emacs
---

I decided to write a Chinese article in my previous post. However, I had a hard time viewing and typing chinese. In Atom, all the Chinese characters are rendered as blocks. Whereas in Emacs, I can view Chinese without problem but I cannot type in anything in Chinese. After spending sometime on the internet, I finally figured out how to enable Chinese support for both of them.

<!--more-->

* Atom

In the Chinese [Atom community](http://atom-china.org), several people claimed that Chinese stopped working after an update. I started using Atom pretty late so I didn't experience the transition. Here are some steps to enable Chinese:

  1) Add 文泉驿正黑 font to your system, in ubuntu

~~~~
sudo apt-get install ttf-wqy-zenhei
~~~~

  2) In atom, go to preference -> Settings, change Font Family to

~~~~
DejaVu Sans Mono,文泉驿正黑
~~~~

  3) Now you should be able to view and edit Chinese in text editor, however there is still problem with plugins, such as markdown-preview. We need final touch to enable Chinese for all. To do this we need to change the styles.less. To do this hit Ctrl + Shift + p and type in "Open your stylesheet". Past the following code into the text editor:

~~~~.js
/*
替换 sans-serif
*/

@font-face {
  font-family: sans-serif;
  src: local("文泉驿正黑");
  /*no unicode-range; default to all characters */
}
~~~~
If you have any open markdown-preview window, you should see the change immediately!
你好世界！

* Emacs

  1) First need to install language pack:

~~~~
cd /usr/share/locales
sudo ./install-language-pack zh_CN
~~~~
  2) Run emacs with the following command `LC_CTYPE='zh_CN.UTF-8' emacs`. You may want to create an alias for this command in your .bashrc.
