## 视频转 GIF 工具 (Streamlit)

这是一个基于 Streamlit 的轻量工具，用于将视频转换为 GIF，支持本地上传、摄像头录制、裁切时间区间、设置输出尺寸/DPI/FPS，并提供导出（下载）功能。

快速运行：

```bash
C:/ProgramData/anaconda3/envs/py313/python.exe -m streamlit run gif_tool/video2gif.py
```

主要功能：
- 本地视频上传或摄像头录像
- 在生成前设置 GIF 宽度、帧率 (FPS) 和 DPI
- 根据视频时长调整裁切区间（滑动条）
- 智能推荐合适的宽度与 DPI
- 预览原视频并在同一界面展示生成的 GIF
- 一键生成并下载 GIF

注意事项：
- 优先使用 MoviePy 提升生成质量和速度；若环境中缺少 MoviePy，程序会自动降级为 OpenCV + Pillow 的备用实现。
- 若生成后的 GIF 体积较大，请尝试降低 `宽度`、`FPS` 或缩短时间区间。
- 推荐在已激活的 Python 环境（例如 `py313`）中运行，上面示例给出完整可执行 Python 路径。

如需帮助，请在运行后把控制台报错或页面行为贴给我，我会继续协助调试。
