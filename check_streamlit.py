import importlib, streamlit
print('streamlit version:', getattr(streamlit, '__version__', None))
importlib.invalidate_caches()
try:
    mod = importlib.import_module('streamlit.web.cli')
    print('Imported streamlit.web.cli ->', mod)
except Exception as e:
    print('Import error:', type(e).__name__, e)
