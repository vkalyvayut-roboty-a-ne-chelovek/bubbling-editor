# bubbling-editor
Simple Tkinter image bubbling editor
```
<Control-o> - open project
<Control-s> - save project
<Control-n> - import image
<Left-click> - draw bubble
<Right-click> - draw counter bubble
<Mouse-wheel> or KP_Add/KP_Subtract - change bubble size
<Control-k> - change background (no bubble) color
<Control-z> - remove last-bubble
<Control-e> - export project
```

Typical workflow:
```
1. import image or open project
2. add bubbles
3. save project
4. export image
```
Export project from command-line: `bubbling-editor -p <path-to-project> -i <path-to-image>`


![editor screenshot](bubbling_editor/assets/editor.png)
