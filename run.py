import threading
import app.cgm_app as appCgm
import app.dexcom_clarity_app as appDexcomClarity
import app.dexcom_follow_app as appDexcomFollow
import app.dexcom_platform_app as appDexcomPlatform
import app.pompe_insuline_app as appPompeInsuline
import app.recepteur_dedie_app as appRecepteurDedie
from flask import request

stop_event = threading.Event()

def run_flask_app(app, port):
    server = threading.current_thread()
    app.config['THREAD_NAME'] = server.name
    
    @app.before_request
    def check_stop():
        if stop_event.is_set():
            func = request.environ.get('werkzeug.server.shutdown')
            if func:
                func()
            return 'Shutting down...', 503
    
    app.run(debug=False, host="0.0.0.0", port=port, use_reloader=False)

def runAppCgm():
    run_flask_app(appCgm.app, 5001)

def runAppDexcomClarity():
    run_flask_app(appDexcomClarity.app, 5002)

def runAppDexcomFollow():
    run_flask_app(appDexcomFollow.app, 5003)

def runAppDexcomPlatform():
    run_flask_app(appDexcomPlatform.app, 5004)

def runAppPompeInsuline():
    run_flask_app(appPompeInsuline.app, 5005)

def runAppRecepteurDedie():
    run_flask_app(appRecepteurDedie.app, 5006)

if __name__ == '__main__':
    threads = [
        threading.Thread(target=runAppCgm, name="CGM_App_Thread"),
        threading.Thread(target=runAppDexcomClarity, name="Dexcom_Clarity_Thread"),
        threading.Thread(target=runAppDexcomFollow, name="Dexcom_Follow_Thread"),
        threading.Thread(target=runAppDexcomPlatform, name="Dexcom_Platform_Thread"),
        threading.Thread(target=runAppPompeInsuline, name="Pompe_Insuline_Thread"),
        threading.Thread(target=runAppRecepteurDedie, name="Recepteur_Dedie_Thread"),
    ]
    
    for thread in threads:
        thread.start()

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nShutting down services...")
        stop_event.set()
