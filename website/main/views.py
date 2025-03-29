from django.shortcuts import render
import subprocess
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'main/index.html')

def nmap(request):
    return render(request, 'main/nmap.html')

def scanvus(request):
    return render(request, 'main/scanvus.html')

def nuclei(request):
    return render(request, 'main/nuclei.html')

@csrf_exempt
def scan(request):
    if request.method == 'POST':
        try:
            # Получаем данные из запроса
            data = json.loads(request.body)
            target_url = data.get('target')
            templates = data.get('templates', [])

            # Проверяем, что URL задан
            if not target_url:
                return JsonResponse({'error': 'URL не указан'}, status=400)

            # Составляем команду для Nuclei
            nuclei_command = ['/home/nadya/go/bin/nuclei', '-u', target_url]

            # Добавляем выбранные шаблоны в команду
            for template in templates:
                nuclei_command.extend(['-t', f'/home/nadya/nuclei-templates/{template}.yaml'])  # Путь к шаблонам

            # Запуск Nuclei
            result = subprocess.run(
                nuclei_command,
                capture_output=True,
                text=True
            )

            # Если процесс завершился с ошибкой
            if result.returncode != 0:
                return JsonResponse({'error': result.stderr}, status=500)

            # Возвращаем результаты сканирования
            return JsonResponse({'result': result.stdout})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Неверный метод запроса'}, status=400)
