import streamlit as st
import tempfile
import os
import io
from PIL import Image
import imageio
import numpy as np
import time
try:
    import cv2
except Exception:
    cv2 = None

try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except Exception:
    VideoFileClip = None
    MOVIEPY_AVAILABLE = False


def record_webcam(duration_sec=5, fps=20):
    if cv2 is None:
        raise RuntimeError('OpenCV (cv2) 未安装，无法录制')
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    path = tmp.name
    tmp.close()
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
    out = cv2.VideoWriter(path, fourcc, float(fps), (w, h))
    start = time.time()
    while time.time() - start < duration_sec:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    out.release()
    cap.release()
    return path


def get_video_duration(path):
    try:
        if MOVIEPY_AVAILABLE and VideoFileClip is not None:
            c = VideoFileClip(path)
            d = float(c.duration)
            c.close()
            return d
    except Exception:
        pass
    if cv2 is None:
        return None
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS) or 0
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    cap.release()
    if fps:
        return frames / fps
    return None


def recommend_size_dpi(w, h):
    if w >= 1920:
        return 720, 72
    if w >= 1280:
        return 640, 72
    if w >= 800:
        return 480, 72
    return min(480, w), 72


def convert_to_gif(video_path, target_width=None, fps=None, dpi=None, start_sec=None, end_sec=None):
    if MOVIEPY_AVAILABLE and VideoFileClip is not None:
        clip = VideoFileClip(video_path)
        try:
            if start_sec is not None or end_sec is not None:
                s = 0 if start_sec is None else float(start_sec)
                e = clip.duration if end_sec is None else float(end_sec)
                clip = clip.subclip(s, e)
            if target_width:
                clip = clip.resize(width=int(target_width))
            target_fps = float(fps) if fps else max(5, min(15, getattr(clip, 'fps', 10)))
            tmp_gif = tempfile.NamedTemporaryFile(delete=False, suffix='.gif')
            tmp_gif.close()
            clip.write_gif(tmp_gif.name, fps=target_fps, program='imageio')
            with open(tmp_gif.name, 'rb') as f:
                data = f.read()
            try:
                os.remove(tmp_gif.name)
            except Exception:
                pass
            return data
        finally:
            try:
                clip.close()
            except Exception:
                pass

    frames = []
    src_fps = None
    try:
        reader = imageio.get_reader(video_path)
        meta = reader.get_meta_data()
        src_fps = meta.get('fps', None) or meta.get('source_fps', None)
        for im in reader:
            frames.append(Image.fromarray(im))
        try:
            reader.close()
        except Exception:
            pass
    except Exception:
        if cv2 is None:
            raise RuntimeError('无法读取视频：缺少 imageio 和 cv2')
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError('无法打开视频文件')
        src_fps = cap.get(cv2.CAP_PROP_FPS) or None
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(frame))
        cap.release()

    if not frames:
        raise RuntimeError('未读取到任何帧')

    duration_src = len(frames) / (src_fps or (fps or 10))
    start_idx = 0 if not start_sec else int((start_sec / duration_src) * len(frames))
    end_idx = len(frames) if not end_sec else int((end_sec / duration_src) * len(frames))
    frames = frames[start_idx:end_idx]

    if target_width:
        resized = []
        for pil in frames:
            w = int(target_width)
            h = int(pil.height * (w / pil.width))
            resized.append(pil.resize((w, h), Image.LANCZOS).convert('P'))
        frames = resized
    else:
        frames = [p.convert('P') for p in frames]

    target_fps = float(fps) if fps else max(5, min(15, int(src_fps or 10)))
    duration_ms = int(1000.0 / float(target_fps))
    out = io.BytesIO()
    frames[0].save(out, format='GIF', save_all=True, append_images=frames[1:], loop=0, duration=duration_ms)
    return out.getvalue()


def estimate_gif_size(width, height, fps, duration_sec):
    bpf = 0.06
    frames = max(1, int(fps * max(0.1, duration_sec)))
    bytes_est = width * height * frames * bpf
    return bytes_est / (1024 * 1024)


st.markdown(
    """
    <style>
    :root{--card-bg:#ffffff;--muted:#6c757d;--accent:#0d6efd;--accent-contrast:#ffffff;--page-bg:#f4f7fb;--card-border:#e9ecef}
    html, body {background:var(--page-bg)!important}
    .app-container{max-width:1600px;margin:10px auto 28px auto;padding:0 12px}
    .page-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
    .page-title{font-size:20px;margin:0;color:#0b2b4a}
    .page-sub{font-size:13px;color:var(--muted);margin:0}
    .card {background-color:var(--card-bg);border-radius:10px;padding:14px;box-shadow:0 6px 18px rgba(15,23,42,0.04);border:1px solid var(--card-border);margin-bottom:12px}
    .small-title{font-size:16px;margin:0;font-weight:600}
    .stButton>button {white-space:nowrap;border-radius:8px;min-width:110px}
    .stButton>button {font-size:14px;padding:8px 12px;background:var(--accent);color:var(--accent-contrast);border:1px solid rgba(0,0,0,0.06)}
    .toolbar{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:nowrap}
    .toolbar-left{display:flex;align-items:center;gap:12px;color:var(--muted);font-size:14px}
    .estimate-badge{background:#eef6ff;color:#084298;padding:6px 10px;border-radius:8px;font-weight:600}
    /* layout wrapper for responsive columns */
    .layout-grid .stColumns {display:flex;gap:12px;flex-wrap:wrap}
    .layout-grid .stColumns > div {flex:1 1 320px;min-width:300px}
    /* make first column (preview) grow larger on wide screens, second column (actions) stay compact */
    .layout-grid .stColumns > div:nth-child(1) {flex:4 1 900px}
    .layout-grid .stColumns > div:nth-child(2) {flex:1 1 280px;min-width:240px}
    @media (max-width:1100px){
        .layout-grid .stColumns > div {flex-basis:100%!important}
        .toolbar{flex-direction:column;align-items:stretch}
        .stButton>button {width:100%}
    }
    @media (min-width:1600px){
        .app-container{max-width:1400px}
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='app-container'>", unsafe_allow_html=True)
st.markdown("<div class='page-header'><div><h3 class='page-title'>视频 → GIF 转换器</h3><div class='page-sub'>上传或录制视频，设置尺寸/DPI/FPS 后生成 GIF</div></div></div>", unsafe_allow_html=True)


def render_sidebar(container=None):
    if container is None:
        container = st
    # If container is the Streamlit module itself, we cannot use it as a context manager.
    # Use a branch so the same UI works when container is `st` or a column/container object.
    if container is st:
        st.header("输入与录制")
        uploaded = st.file_uploader("上传视频（拖拽或点击）", type=["mp4", "mov", "avi", "mkv"], key="uploader_main")
        st.markdown("---")
        st.write("或使用摄像头录制视频")
        rec_dur = st.number_input("录制时长（秒）", min_value=1, max_value=60, value=5)
        if st.button("开始录制", key="record_main"):
            with st.spinner("正在录制…"):
                try:
                    path = record_webcam(int(rec_dur))
                    st.success("录制完成")
                    uploaded = open(path, 'rb')
                except Exception as e:
                    st.error(f"录制失败：{e}")

        st.markdown("---")
        st.header("输出设置")
        target_width = st.number_input("目标宽度（像素）", min_value=32, max_value=8192, value=480)
        target_fps = st.slider("GIF 帧率（FPS）", min_value=2, max_value=30, value=10)
        dpi = st.number_input("DPI（信息用）", min_value=20, max_value=600, value=72)
        with st.expander("显示与裁剪（展开）", expanded=False):
            preview_width = st.number_input("预览宽度 (px)", min_value=240, max_value=1280, value=720)
            gif_width = st.number_input("生成 GIF 宽度 (px)", min_value=240, max_value=1280, value=720)
            vid_dur = st.session_state.get("__video_duration__", 0.0) or 0.0
            if vid_dur and vid_dur > 0:
                crop_range = st.slider("裁剪范围（秒）", min_value=0.0, max_value=float(vid_dur), value=(0.0, float(min(10.0, vid_dur))), step=0.1)
                crop_start, crop_end = float(crop_range[0]), float(crop_range[1])
            else:
                crop_start, crop_end = 0.0, 0.0

        est_box = st.empty()
        if vid_dur and vid_dur > 0:
            sel = (crop_end - crop_start) if crop_end > crop_start else vid_dur
            est_mb = estimate_gif_size(int(target_width), int(target_width * 0.5625), int(target_fps), sel)
            sugg = "建议：降低 FPS 或分辨率以减小体积" if est_mb > 5 else "文件体积可接受"
            est_box.info(f"估算输出大小：{est_mb:.2f} MB。{sugg}")

        if st.button("推荐尺寸", key="recommend_main"):
            try:
                if uploaded is None:
                    st.warning("请先上传或录制视频")
                else:
                    if isinstance(uploaded, str):
                        sample = uploaded
                    else:
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1])
                        tmp.write(uploaded.read())
                        tmp.close()
                        sample = tmp.name
                    if VideoFileClip is not None:
                        c = VideoFileClip(sample)
                        w, h = c.size
                        c.close()
                        rw, rdpi = recommend_size_dpi(w, h)
                        st.info(f"建议宽度：{rw}px, DPI：{rdpi}")
                    else:
                        st.info("MoviePy 不可用，使用默认建议")
            except Exception as e:
                st.error(f"推荐失败：{e}")
    else:
        with container:
            st.header("输入与录制")
            uploaded = st.file_uploader("上传视频（拖拽或点击）", type=["mp4", "mov", "avi", "mkv"], key="uploader_main")
            st.markdown("---")
            st.write("或使用摄像头录制视频")
            rec_dur = st.number_input("录制时长（秒）", min_value=1, max_value=60, value=5)
            if st.button("开始录制", key="record_main"):
                with st.spinner("正在录制…"):
                    try:
                        path = record_webcam(int(rec_dur))
                        st.success("录制完成")
                        uploaded = open(path, 'rb')
                    except Exception as e:
                        st.error(f"录制失败：{e}")

            st.markdown("---")
            st.header("输出设置")
            target_width = st.number_input("目标宽度（像素）", min_value=32, max_value=8192, value=480)
            target_fps = st.slider("GIF 帧率（FPS）", min_value=2, max_value=30, value=10)
            dpi = st.number_input("DPI（信息用）", min_value=20, max_value=600, value=72)
            with st.expander("显示与裁剪（展开）", expanded=False):
                preview_width = st.number_input("预览宽度 (px)", min_value=240, max_value=1280, value=720)
                gif_width = st.number_input("生成 GIF 宽度 (px)", min_value=240, max_value=1280, value=720)
                vid_dur = st.session_state.get("__video_duration__", 0.0) or 0.0
                if vid_dur and vid_dur > 0:
                    crop_range = st.slider("裁剪范围（秒）", min_value=0.0, max_value=float(vid_dur), value=(0.0, float(min(10.0, vid_dur))), step=0.1)
                    crop_start, crop_end = float(crop_range[0]), float(crop_range[1])
                else:
                    crop_start, crop_end = 0.0, 0.0

            est_box = st.empty()
            if vid_dur and vid_dur > 0:
                sel = (crop_end - crop_start) if crop_end > crop_start else vid_dur
                est_mb = estimate_gif_size(int(target_width), int(target_width * 0.5625), int(target_fps), sel)
                sugg = "建议：降低 FPS 或分辨率以减小体积" if est_mb > 5 else "文件体积可接受"
                est_box.info(f"估算输出大小：{est_mb:.2f} MB。{sugg}")

            if st.button("推荐尺寸", key="recommend_main"):
                try:
                    if uploaded is None:
                        st.warning("请先上传或录制视频")
                    else:
                        if isinstance(uploaded, str):
                            sample = uploaded
                        else:
                            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1])
                            tmp.write(uploaded.read())
                            tmp.close()
                            sample = tmp.name
                        if VideoFileClip is not None:
                            c = VideoFileClip(sample)
                            w, h = c.size
                            c.close()
                            rw, rdpi = recommend_size_dpi(w, h)
                            st.info(f"建议宽度：{rw}px, DPI：{rdpi}")
                        else:
                            st.info("MoviePy 不可用，使用默认建议")
                except Exception as e:
                    st.error(f"推荐失败：{e}")

    return {
        'uploaded': uploaded,
        'target_width': int(target_width),
        'target_fps': int(target_fps),
        'dpi': int(dpi),
        'preview_width': int(locals().get('preview_width', 720)),
        'gif_width': int(locals().get('gif_width', 720)),
        'crop_start': float(locals().get('crop_start', 0.0)),
        'crop_end': float(locals().get('crop_end', 0.0)),
    }


def render_preview_card(uploaded, preview_width):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h4 class='small-title'>预览</h4>", unsafe_allow_html=True)
    if uploaded is None:
        st.info("尚未选择视频")
    else:
        try:
            if isinstance(uploaded, str):
                vpath = uploaded
            else:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1])
                tmp.write(uploaded.read())
                tmp.close()
                vpath = tmp.name
            try:
                st.video(vpath, start_time=0, width=preview_width)
            except Exception:
                st.video(vpath)
            st.session_state['__video_path__'] = vpath
            dur = get_video_duration(vpath)
            if dur:
                st.session_state['__video_duration__'] = float(dur)
        except Exception:
            st.warning('无法预览该视频')
    st.markdown('</div>', unsafe_allow_html=True)


def render_actions_card(uploaded, params):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex;justify-content:space-between;align-items:center'><div class='small-title'>生成与导出</div></div>", unsafe_allow_html=True)
    left, right = st.columns([2, 1])
    vid_dur = st.session_state.get('__video_duration__', None)
    if vid_dur:
        sel = (params['crop_end'] - params['crop_start']) if params['crop_end'] > params['crop_start'] else vid_dur
        est_mb = estimate_gif_size(params['target_width'], int(params['target_width'] * 0.5625), params['target_fps'], sel)
        est_text = f"估算：{est_mb:.2f} MB / {sel:.1f}s"
    else:
        est_text = '估算：时长未知'
    with left:
        st.markdown(f"<div class='toolbar-left'><span class='estimate-badge'>{est_text}</span></div>", unsafe_allow_html=True)
    with right:
        r1, r2 = st.columns([1, 1])
        recommend = r1.button('🎯 推荐', key='toolbar_recommend')
        generate = r2.button('▶ 生成 GIF', key='toolbar_generate')
        status = st.empty()
        dl = st.empty()

    if recommend:
        if uploaded is None:
            status.info('请先上传或录制视频')
        else:
            try:
                if isinstance(uploaded, str):
                    sample = uploaded
                else:
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1])
                    tmp.write(uploaded.read())
                    tmp.close()
                    sample = tmp.name
                if VideoFileClip is not None:
                    c = VideoFileClip(sample)
                    w, h = c.size
                    c.close()
                    rw, rdpi = recommend_size_dpi(w, h)
                    status.info(f'建议宽度：{rw}px, DPI：{rdpi}')
                else:
                    status.info('MoviePy 不可用，使用默认建议')
            except Exception as e:
                status.error(f'推荐失败：{e}')

    if generate:
        if uploaded is None:
            status.warning('请先上传或录制视频')
        else:
            with st.spinner('正在生成 GIF…'):
                try:
                    vpath = st.session_state.get('__video_path__')
                    if not vpath:
                        if isinstance(uploaded, str):
                            vpath = uploaded
                        else:
                            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1])
                            tmp.write(uploaded.read())
                            tmp.close()
                            vpath = tmp.name
                    s = None if params['crop_start'] == 0.0 else float(params['crop_start'])
                    e = None if params['crop_end'] == 0.0 else float(params['crop_end'])
                    gif = convert_to_gif(vpath, target_width=params['target_width'], fps=params['target_fps'], dpi=params['dpi'], start_sec=s, end_sec=e)
                    status.success('GIF 已生成')
                    dl.download_button('⬇ 下载', data=gif, file_name='output.gif', mime='image/gif', key='toolbar_download')
                    st.image(gif, caption='生成的 GIF', width=params['gif_width'])
                except Exception as e:
                    status.error(f'转换失败：{e}')

    st.markdown('</div>', unsafe_allow_html=True)


def main():
    # Render settings in a top expander (full width) to reduce left-column clutter
    with st.expander('输入与录制（点击展开/折叠设置）', expanded=False):
        params = render_sidebar(container=st)

    # Main area wrapper so our responsive CSS can target these columns
    st.markdown("<div class='layout-grid'>", unsafe_allow_html=True)
    col_preview, col_actions = st.columns([7, 1], gap='small')
    with col_preview:
        render_preview_card(params['uploaded'], params['preview_width'])
    with col_actions:
        render_actions_card(params['uploaded'], params)
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
    st.markdown('</div>', unsafe_allow_html=True)
