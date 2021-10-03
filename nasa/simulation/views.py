from django.shortcuts import render
import subprocess, os
import uuid
from django.http import FileResponse, HttpResponseRedirect


def home(request):
    if 'id' not in request.session:
        request.session['id'] = str(uuid.uuid4())
    return render(request, 'home.html')

def simulate(request):
    rain = float(request.GET['rainfall'])
    leak = float(request.GET['water_leakage'])
    request.session["all"] = max(abs(int(1000 - (min(rain, 1000) / 3) - (min(100, leak) * 4))), 100) / int(request.GET['speed'])
    request.session["speed"] = int(request.GET['speed'])
    subprocess.Popen(['python3', '/home/manwar/blender/simulation.py', request.GET['rainfall'], request.GET['water_leakage'], request.session['id'], request.GET['speed']])
    try:
        os.mkdir('/home/manwar/nasa/simulation/static/output/' + request.session['id'])
    except:
        pass
    return render(request, 'rocket.html')


def output(request):
    try:
        if 'frame' in request.GET:

            img = open('/home/manwar/nasa/simulation/static/output/' + request.session['id'] + '/out_' + '{0:0=4d}'.format(int(request.GET['frame'])) + '.png', 'rb')
            return FileResponse(img)
        if not os.path.exists('/home/manwar/nasa/simulation/static/output/' + request.session['id'] + '/out_' + '{0:0=4d}'.format(int(request.GET['frame_page'])) + '.png'):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        frame = int(request.GET['frame_page'])
        all = int(request.session['all'])
        water = int(min((frame + 10) / all * 100, 100))
        acoustic = int(min((frame + 20) / all * 100, 100))
        fos = int(min((frame + 30) / all * 100, 100))
        if frame % int(request.session["speed"]) == 1:
            return render(request, 'output.html', {'frame': frame, 'frame_next': frame + 1, 'frame_prev': frame-2, 'acoustic': acoustic, 'fos': fos, 'water': water})
        if frame % int(request.session["speed"]) == int(request.session["speed"]) - 1:
            return render(request, 'output.html', {'frame': frame, 'frame_next': frame + 2, 'frame_prev': frame-2, 'acoustic': acoustic, 'fos': fos, 'water': water})
        return render(request, 'output.html', {'frame': frame, 'frame_next': frame + 1, 'frame_prev': frame-1, 'acoustic': acoustic, 'fos': fos, 'water': water})
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

