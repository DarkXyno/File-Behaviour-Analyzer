import psutil

def resolve_process(target_path: str):
    """
    Docstring for resolve_process
    
    Returns (process_name, pid) or (None, None) if not found.
    """
    try:
        for proc in psutil.process_iter(attrs=["pid", "name", "open_files"]):
            try:
                files = proc.info.get("open_files")
                if not files:
                    continue

                for f in files:
                    if f.path == target_path:
                        return proc.info["name"], proc.info["pid"]
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    except Exception:
        pass
    
    return None, None